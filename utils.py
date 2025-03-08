import cv2

def checkAvailiableCams(n):
    for index in range(n):
        cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera work on index: {index}")
    else:
        print(f"No camera at index: {index}")


if __name__ == "__main__":
    checkAvailiableCams(6)
