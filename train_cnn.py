import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from pathlib import Path

# ======================
# CONFIG
# ======================
DATA_DIR = "Dataset/train"  # Match actual folder name (capital D)
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 30

MODEL_DIR = Path("ml_models")
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "glaucoma_mobilenet.h5"  # Use H5 format for compatibility

print("=" * 70)
print("GLAUCOMA DETECTION MODEL TRAINING")
print("=" * 70)
print(f"Training Data: {DATA_DIR}")
print(f"Image Size: {IMG_SIZE}x{IMG_SIZE}")
print(f"Batch Size: {BATCH_SIZE}")
print(f"Epochs: {EPOCHS}")
print("=" * 70)
print()

# ======================
# LOAD DATA
# ======================
print("Loading training data...")
try:
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=True,
        validation_split=0.2,
        subset="training",
        seed=42,
        class_names=["normal", "glaucoma"]
    )
    print(f"[OK] Training dataset loaded: {len(train_ds)} batches")

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=True,
        validation_split=0.2,
        subset="validation",
        seed=42,
        class_names=["normal", "glaucoma"]
    )
    print(f"[OK] Validation dataset loaded: {len(val_ds)} batches")
except Exception as e:
    print(f"[ERROR] Error loading data: {e}")
    print(f"Make sure {DATA_DIR} exists with subdirectories: normal/ and glaucoma/")
    exit(1)

train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
val_ds = val_ds.map(lambda x, y: (x / 255.0, y))
print("[OK] Data normalized (0-1 range)")
print()

# ======================
# CLASS WEIGHTS
# ======================
print("Computing class weights for balanced training...")
# Since we verified the dataset is perfectly balanced (352 glaucoma + 352 normal)
# We can compute weights directly from directory counts instead of iterating dataset
try:
    glaucoma_count = len(list(Path(DATA_DIR, "glaucoma").glob("*.jpg")) + 
                         list(Path(DATA_DIR, "glaucoma").glob("*.png")))
    normal_count = len(list(Path(DATA_DIR, "normal").glob("*.jpg")) + 
                       list(Path(DATA_DIR, "normal").glob("*.png")))
    print(f"Found {glaucoma_count} glaucoma and {normal_count} normal images")
    
    # Compute weights - balanced means equal weight per class
    total = glaucoma_count + normal_count
    weights = compute_class_weight("balanced", 
                                   classes=np.array([0, 1]), 
                                   y=np.array([0]*glaucoma_count + [1]*normal_count))
    class_weights = dict(enumerate(weights))
    print(f"Class weights: {class_weights}")
except Exception as e:
    print(f"Warning: Could not compute class weights: {e}")
    print("Using equal class weights (1.0 for both classes)")
    class_weights = {0: 1.0, 1: 1.0}
print()

# ======================
# AUGMENTATION
# ======================
augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# ======================
# MODEL
# ======================
print("Building MobileNetV2 model...")
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)
base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
    augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(1, activation="sigmoid")
])

print("[OK] Model architecture created")
print()

# ======================
# COMPILE
# ======================
print("Compiling model...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
print("[OK] Model compiled")
print()

# ======================
# CALLBACKS
# ======================
# Create model directory if it doesn't exist
checkpoint_dir = Path("glaucoma_detection/model")
checkpoint_dir.mkdir(parents=True, exist_ok=True)
checkpoint_path = str(checkpoint_dir / "glaucoma_cnn_model.h5")  # Use H5 format

callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint(
        filepath=checkpoint_path,
        monitor="val_loss",
        save_best_only=True,
        verbose=0  # Reduce verbose output to avoid issues
    )
]


# ======================
# TRAIN
# ======================
print("=" * 70)
print("STARTING TRAINING...")
print("=" * 70)
print()

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks,
    verbose=1
)

print()
print("=" * 70)
print("TRAINING COMPLETED")
print("=" * 70)
print()

# ======================
# FINAL SAVE
# ======================
print("Saving final model...")
model.save(MODEL_PATH)
print(f"[OK] Model saved to: {MODEL_PATH}")
print()

# Print training summary
print("=" * 70)
print("TRAINING SUMMARY")
print("=" * 70)
print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
print(f"Final Training Loss: {history.history['loss'][-1]:.4f}")
print(f"Final Validation Loss: {history.history['val_loss'][-1]:.4f}")
print("=" * 70)
print()
print("[SUCCESS] Model training complete! Ready for inference.")
print()
print("To use this model in your application:")
print(f"1. Set USE_MOCK_MODEL = False in glaucoma_detection/utils.py")
print(f"2. Restart the Django server")
print(f"3. Upload fundus images for predictions")

