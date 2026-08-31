import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from cnn_model import build_transfer_model

# -----------------------------
# SETTINGS
# -----------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30

TRAIN_DIR = r"PATH_TO_TRAIN_FOLDER"
VAL_DIR = r"PATH_TO_VALIDATION_FOLDER"

# -----------------------------
# DATA GENERATORS
# -----------------------------
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)

val_datagen = ImageDataGenerator(
    rescale=1.0 / 255
)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=True
)

val_gen = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# -----------------------------
# BUILD MODEL
# -----------------------------
model, base_model = build_transfer_model(
    num_classes=train_gen.num_classes
)

model.summary()

# -----------------------------
# CALLBACKS
# -----------------------------
callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=6,
        restore_best_weights=True
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-6
    ),

    ModelCheckpoint(
        "skin_disease_model.keras",
        monitor="val_accuracy",
        save_best_only=True
    )
]

# -----------------------------
# TRAIN
# -----------------------------
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks
)

# -----------------------------
# SAVE FINAL MODEL
# -----------------------------
model.save("skin_disease_final.keras")

print("Training completed!")
print("Model saved successfully.")
