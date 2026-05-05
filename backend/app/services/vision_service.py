import os
import logging
from typing import List, Dict, Any

try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

logger = logging.getLogger(__name__)

class YoloVisionService:
    def __init__(self):
        self.model = None
        self.classes = {0: "minor_damage", 1: "moderate_damage", 2: "major_damage", 3: "front_bumper"}

        # Load the best weights if they exist (produced by train_yolo.py)
        # Fall back to base yolov8n.pt if not available
        if HAS_YOLO:
            try:
                # __file__ is in backend/app/services
                # We need to go up to backend/
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                best_weights_path = os.path.join(base_dir, "scripts", "runs", "damage_assessment", "weights", "best.pt")

                if os.path.exists(best_weights_path):
                    logger.info(f"Loading fine-tuned YOLO model from {best_weights_path}")
                    self.model = YOLO(best_weights_path)
                else:
                    logger.info("Fine-tuned weights not found, using base yolov8n.pt")
                    self.model = YOLO("yolov8n.pt")
            except Exception as e:
                logger.error(f"Failed to load YOLO model: {e}")

    def detect_damage(self, photo_urls: List[str]) -> Dict[str, Any]:
        """
        Run the YOLO model on a list of images to detect damage and parts.
        """
        if not self.model:
            return {
                "status": "error",
                "message": "YOLO model not loaded or ultralytics not installed",
                "detections": []
            }

        all_detections = []
        highest_severity_detected = "minor"
        severity_levels = {"minor": 1, "moderate": 2, "major": 3, "total_loss": 4}

        damaged_parts = set()

        for url in photo_urls:
            local_path = url.lstrip("/")
            if not os.path.exists(local_path):
                continue

            try:
                results = self.model(local_path)

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        cls_id = int(box.cls[0].item())
                        conf = float(box.conf[0].item())

                        # Map custom dataset class ID if possible, otherwise use model's names
                        class_name = self.classes.get(cls_id)
                        if not class_name and hasattr(self.model, "names"):
                            class_name = self.model.names.get(cls_id, f"class_{cls_id}")

                        # Extremely basic heuristic mapping for the mock model
                        if "minor" in class_name:
                            severity = "minor"
                        elif "moderate" in class_name:
                            severity = "moderate"
                        elif "major" in class_name:
                            severity = "major"
                        else:
                            # Might be a part like "front_bumper"
                            damaged_parts.add(class_name)
                            severity = "minor"

                        if severity_levels[severity] > severity_levels[highest_severity_detected]:
                            highest_severity_detected = severity

                        all_detections.append({
                            "class": class_name,
                            "confidence": round(conf, 2),
                            "box": box.xyxy[0].tolist()
                        })
            except Exception as e:
                logger.error(f"Error during YOLO inference on {local_path}: {e}")

        return {
            "status": "success",
            "highest_severity": highest_severity_detected,
            "damaged_parts": list(damaged_parts),
            "detections": all_detections
        }

yolo_vision_service = YoloVisionService()
