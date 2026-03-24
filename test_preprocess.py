from preprocessing.utils import preprocess_image

img = preprocess_image("media/fundus/sample.jpg")

if img is None:
    print("Ungradable image")
else:
    print("Image ready for model", img.shape)
