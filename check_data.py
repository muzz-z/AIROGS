import os

base = "dataset/train"

for cls in ["normal", "glaucoma"]:
    path = os.path.join(base, cls)
    print(cls, ":", len(os.listdir(path)))
