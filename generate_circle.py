import cv2

with open("circle.txt", "w") as f:
    for i, row in enumerate(cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))):
        for j, val in enumerate(row):
            if val:
                f.write(f"[{i + 460}, {j + 460}],\n")
