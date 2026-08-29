"""
Evaluation & Confidence Module — Team 3
Skin Disease Classification (HAM10000, 7 classes)

Loads the trained model (saved by Team 4 as "skin_disease_model.keras")
and computes performance metrics + per-image confidence scores.

Assumes `test_gen` exists (e.g. from ImageDataGenerator.flow_from_dataframe
/ flow_from_directory), same as cnn_model.py.
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support,
)

# HAM10000 class order — must match the label order used by test_gen
CLASS_NAMES = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]

FULL_NAMES = {
    "akiec": "Actinic Keratoses",
    "bcc": "Basal Cell Carcinoma",
    "bkl": "Benign Keratosis",
    "df": "Dermatofibroma",
    "mel": "Melanoma",
    "nv": "Melanocytic Nevi",
    "vasc": "Vascular Lesion",
}


# ---------------------------------------------------------
# 1. Load model
# ---------------------------------------------------------
def load_trained_model(model_path="skin_disease_model.keras"):
    return tf.keras.models.load_model(model_path)


# ---------------------------------------------------------
# 2. Run predictions on the test set
# ---------------------------------------------------------
def get_predictions(model, test_gen):
    """
    Returns:
        y_true: true class indices
        y_pred: predicted class indices
        y_probs: full softmax probability array (for confidence scores)
    """
    test_gen.reset()
    y_probs = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(y_probs, axis=1)
    y_true = test_gen.classes  # true labels from the generator
    return y_true, y_pred, y_probs


# ---------------------------------------------------------
# 3. Core metrics: accuracy, precision, recall, F1
# ---------------------------------------------------------
def compute_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=range(len(CLASS_NAMES))
    )

    print(f"\nOverall Accuracy: {acc:.4f}\n")
    print(classification_report(y_true, y_pred, target_names=CLASS_NAMES, digits=4))

    per_class = {
        CLASS_NAMES[i]: {
            "precision": round(float(precision[i]), 4),
            "recall": round(float(recall[i]), 4),
            "f1_score": round(float(f1[i]), 4),
            "support": int(support[i]),
        }
        for i in range(len(CLASS_NAMES))
    }

    return {"accuracy": round(float(acc), 4), "per_class": per_class}


# ---------------------------------------------------------
# 4. Confusion matrix plot
# ---------------------------------------------------------
def plot_confusion_matrix(y_true, y_pred, save_path="confusion_matrix.png"):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix — Skin Disease Classification")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Confusion matrix saved to {save_path}")


# ---------------------------------------------------------
# 5. Training curves (loss/accuracy) — pass in Team 4's `history`
# ---------------------------------------------------------
def plot_training_curves(history, save_path="training_curves.png"):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history.history["accuracy"], label="train")
    axes[0].plot(history.history["val_accuracy"], label="val")
    axes[0].set_title("Accuracy")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(history.history["loss"], label="train")
    axes[1].plot(history.history["val_loss"], label="val")
    axes[1].set_title("Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Training curves saved to {save_path}")


# ---------------------------------------------------------
# 6. Confidence score for a single prediction
#    -> This is what gets handed to Team 2 (Backend/API)
# ---------------------------------------------------------
def predict_with_confidence(model, image_array):
    """
    image_array: preprocessed image, shape (1, 224, 224, 3)
    Returns a dict ready to be sent to the API / frontend.
    """
    probs = model.predict(image_array, verbose=0)[0]
    top_idx = int(np.argmax(probs))
    result = {
        "disease_code": CLASS_NAMES[top_idx],
        "disease_name": FULL_NAMES[CLASS_NAMES[top_idx]],
        "confidence": round(float(probs[top_idx]) * 100, 2),
        "all_probabilities": {
            CLASS_NAMES[i]: round(float(probs[i]) * 100, 2)
            for i in range(len(CLASS_NAMES))
        },
    }
    return result


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------
if __name__ == "__main__":
    # model = load_trained_model("skin_disease_model.keras")
    # y_true, y_pred, y_probs = get_predictions(model, test_gen)
    # metrics = compute_metrics(y_true, y_pred)
    # plot_confusion_matrix(y_true, y_pred)
    # single_result = predict_with_confidence(model, some_preprocessed_image)
    # print(single_result)
    print("Import this module and call the functions once Team 4 delivers the trained model + test_gen.")