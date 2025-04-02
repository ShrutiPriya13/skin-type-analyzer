import os
from PIL import Image

# Define dataset path
dataset_path = r"C:\Users\KIIT\Downloads\Skin types.v2i.multiclass"

# Allowed image extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.tiff')

# Recursively find images in all subfolders
image_files = []
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.lower().endswith(valid_extensions):
            image_files.append(os.path.join(root, file))

print(f"Total images found: {len(image_files)}")

# Display first image if available
if image_files:
    img = Image.open(image_files[0])
    img.show()
else:
    print("No valid images found!")


