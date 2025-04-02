import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

# Load preprocessed training data
X_train = np.load("image_data.npy")
y_train = np.load("labels.npy")

# Load validation data dynamically from folder
valid_dir = "valid"
img_size = (224, 224)
valid_datagen = ImageDataGenerator(rescale=1.0 / 255)
val_generator = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=img_size,
    batch_size=32,
    class_mode="sparse",
    shuffle=False
)

# Data Augmentation
train_datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)
train_datagen.fit(X_train)

# Load MobileNetV2 with pre-trained weights
base_model = MobileNetV2(input_shape=(X_train.shape[1], X_train.shape[2], X_train.shape[3]), 
                         include_top=False, weights="imagenet")

# Unfreeze last few layers for fine-tuning
for layer in base_model.layers[-30:]:
    layer.trainable = True

# Define model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(4, activation="softmax")
])

# Compute class weights to handle class imbalance
class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y_train), y=y_train)
class_weights_dict = dict(enumerate(class_weights))

# Learning rate scheduler
lr_scheduler = ReduceLROnPlateau(monitor="val_accuracy", patience=3, factor=0.5, min_lr=1e-6, verbose=1)

# Compile model
model.compile(optimizer=Adam(learning_rate=1e-4), loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model
history = model.fit(
    train_datagen.flow(X_train, y_train, batch_size=32), 
    epochs=14, 
    validation_data=val_generator, 
    class_weight=class_weights_dict, 
    callbacks=[lr_scheduler]
)

# Save the trained model
model.save("skin_type_model.h5")
print("Model training complete and saved as 'skin_type_model.h5'")
