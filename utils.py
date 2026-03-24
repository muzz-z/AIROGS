import cv2
import numpy as np


def preprocess_image(image_path):
    """
    Preprocess fundus image for CNN model.

    Steps:
    1. Load image
    2. Validate image
    3. Convert BGR → RGB
    4. Resize to 224x224
    5. Normalize to [0, 1]

    Returns:
    - Preprocessed image (224, 224, 3)
    - None if image is invalid/unreadable
    """

    # 1️⃣ Load image
    img = cv2.imread(image_path)

    # 2️⃣ Validate image
    if img is None:
        print("❌ Image could not be read:", image_path)
        return None

    try:
        # 3️⃣ Convert BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 4️⃣ Resize (CNN input size)
        img = cv2.resize(img, (224, 224))

        # 5️⃣ Normalize
        img = img.astype(np.float32) / 255.0

        return img

    except Exception as e:
        print("❌ Preprocessing failed:", e)
        return None

