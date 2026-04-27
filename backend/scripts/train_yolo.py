import os

from ultralytics import YOLO


def train_model():
    """
    Train or fine-tune a YOLOv8 model for auto insurance damage assessment.
    """
    print("Starting YOLOv8 training for Damage Assessment...")

    # Load a pre-trained YOLOv8 model
    model = YOLO("yolov8n.pt")  # nano model for speed, can use yolov8s.pt or others

    # Define dataset path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_yaml_path = os.path.join(base_dir, "dataset", "damage_dataset.yaml")

    if not os.path.exists(data_yaml_path):
        print(f"Error: Dataset configuration not found at {data_yaml_path}")
        print("Run `python generate_mock_dataset.py` first to generate mock data.")
        return

    # Train the model
    # We use very few epochs and a tiny image size for demonstration/mocking purposes
    results = model.train(
        data=data_yaml_path,
        epochs=1,
        imgsz=224,
        batch=2,
        project=os.path.join(base_dir, "runs"),
        name="damage_assessment",
        device="cpu" # Force CPU for local execution where GPU isn't guaranteed
    )

    print("Training complete!")
    print(f"Best model weights saved to: {results.save_dir}/weights/best.pt")

if __name__ == "__main__":
    train_model()
