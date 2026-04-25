import os
import yaml
import numpy as np
from PIL import Image

def generate_mock_dataset():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")

    os.makedirs(os.path.join(dataset_dir, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "labels", "val"), exist_ok=True)

    # 0: minor_damage, 1: moderate_damage, 2: major_damage, 3: front_bumper
    classes = ["minor_damage", "moderate_damage", "major_damage", "front_bumper"]

    # Generate mock images and labels
    for i in range(10): # 10 train images
        img_arr = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_arr)
        img.save(os.path.join(dataset_dir, "images", "train", f"mock_{i}.jpg"))

        with open(os.path.join(dataset_dir, "labels", "train", f"mock_{i}.txt"), "w") as f:
            f.write("0 0.5 0.5 0.2 0.2\n") # class_id x_center y_center width height

    for i in range(2): # 2 val images
        img_arr = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_arr)
        img.save(os.path.join(dataset_dir, "images", "val", f"mock_val_{i}.jpg"))

        with open(os.path.join(dataset_dir, "labels", "val", f"mock_val_{i}.txt"), "w") as f:
            f.write("1 0.5 0.5 0.3 0.3\n")

    # Create dataset config
    data_yaml = {
        "path": dataset_dir,
        "train": "images/train",
        "val": "images/val",
        "names": {i: name for i, name in enumerate(classes)}
    }

    config_path = os.path.join(dataset_dir, "damage_dataset.yaml")
    with open(config_path, "w") as f:
        yaml.dump(data_yaml, f)

    return config_path

if __name__ == "__main__":
    generate_mock_dataset()
    print("Mock dataset generated successfully.")
