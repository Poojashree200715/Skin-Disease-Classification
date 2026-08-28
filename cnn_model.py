"""
Deep Learning Model — Skin Disease Classification (CNN)
Assumes train_gen, val_gen, test_gen already exist (e.g. from
ImageDataGenerator.flow_from_dataframe / flow_from_directory).
"""

import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB0

IMG_SIZE = (224, 224)
NUM_CLASSES = 7  # akiec, bcc, bkl, df, mel, nv, vasc


# ---------------------------------------------------------
# Option A: Transfer Learning (recommended — higher accuracy)
# ---------------------------------------------------------
def build_transfer_model(num_classes=NUM_CLASSES):
    base_model = EfficientNetB0(
        include_top=False, weights="imagenet", input_shape=(*IMG_SIZE, 3)
    )
    base_model.trainable = False  # freeze backbone initially

    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base_model


# ---------------------------------------------------------
# Option B: Custom CNN from scratch
# ---------------------------------------------------------
def build_custom_cnn(num_classes=NUM_CLASSES):
    model = models.Sequential([
        layers.Input(shape=(*IMG_SIZE, 3)),

        layers.Conv2D(32, 3, activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Conv2D(256, 3, activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ---------------------------------------------------------
# Training
# ---------------------------------------------------------
def train(model, train_gen, val_gen, class_weight=None, epochs=30):
    cb_list = [
        callbacks.EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True),
        callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6),
        callbacks.ModelCheckpoint("skin_disease_model.keras", monitor="val_accuracy", save_best_only=True),
    ]
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        class_weight=class_weight,
        callbacks=cb_list,
    )
    return history


# ---------------------------------------------------------
# Optional fine-tuning pass (unfreeze top layers of backbone)
# ---------------------------------------------------------
def fine_tune(model, base_model, train_gen, val_gen, epochs=10):
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return train(model, train_gen, val_gen, epochs=epochs)


if __name__ == "__main__":
    # Example usage (train_gen / val_gen must be defined beforehand):
    model, base_model = build_transfer_model()
    model.summary()
    # history = train(model, train_gen, val_gen)
    # fine_tune(model, base_model, train_gen, val_gen)
