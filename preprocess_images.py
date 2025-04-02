import os
import numpy as np
import pandas as pd
from PIL import Image

# Define dataset path
dataset_path = r"C:\Users\KIIT\Downloads\Skin types.v2i.multiclass"

# Target image size
IMAGE_SIZE = (224, 224)

# Allowed image extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.tiff')

# Initialize lists for image data and labels
image_data = []
labels = []
label_map = {"combination": 0, "dry": 1, "normal": 2, "oily": 3}  # Assign numbers to skin types

for subfolder in ["train", "test", "valid"]:
    subfolder_path = os.path.join(dataset_path, subfolder)

    print(f"\n📂 Checking folder: {subfolder_path}")

    if not os.path.exists(subfolder_path):
        print(f"❌ Folder not found: {subfolder_path}")
        continue

    for label in os.listdir(subfolder_path):  # Folder names = labels
        label_path = os.path.join(subfolder_path, label)

        if os.path.isdir(label_path):  # Ensure it's a folder
            print(f"✅ Found category: {label}")

            for file in os.listdir(label_path):
                if file.lower().endswith(valid_extensions):
                    file_path = os.path.join(label_path, file)

                    try:
                        img = Image.open(file_path).convert("RGB")  # Ensure RGB format
                        img = img.resize(IMAGE_SIZE)  # Resize to (224, 224)
                        img_array = np.array(img) / 255.0  # Normalize

                        image_data.append(img_array)
                        labels.append(label_map[label])  # Store the label (0-3)

                    except Exception as e:
                        print(f"⚠️ Error processing {file}: {e}")

# Convert to NumPy arrays
image_data = np.array(image_data)
labels = np.array(labels)

print(f"\n📊 Total processed images: {len(image_data)}")

# Save preprocessed data
np.save("image_data.npy", image_data)
np.save("labels.npy", labels)

# Save labels to a CSV file for reference (FAST method)
df = pd.DataFrame({"skin_type": labels})
df.to_csv("image_labels.csv", index=False)

print("✅ Preprocessed images saved as NumPy arrays and labels stored in CSV!")
