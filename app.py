import cv2
from flask import Flask, render_template, Response, jsonify
from PIL import Image
from flask_socketio import SocketIO, emit

# ASCII_CHARS = "@%#+=-:. "
ASCII_CHARS = " .:-=+*%@#@#&$@B8"
# ASCII_CHARS = ASCII_CHARS[::-1]

app = Flask(__name__)
socketio = SocketIO(app)

def frameToAscii(frame, newWidth=400):
    # Start resizing frame
    height, width, _ = frame.shape
    aspectRatio = height / width * 0.55
    newHeight = int(aspectRatio * newWidth)
    resizedFrame = cv2.resize(frame, (newWidth, newHeight))

    # Make it gray
    grayFrame = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)

    # Try to map pixels to ASCII_CHARS
    # asciiArt = "".join([ASCII_CHARS[pixel // 25] for pixel in grayFrame.flatten()])
    asciiArt = "".join([ASCII_CHARS[int(pixel / 255 * (len(ASCII_CHARS) - 1))] for pixel in grayFrame.flatten()])
    asciiLine = [asciiArt[i:i+newWidth] for i in range(0, len(asciiArt), newWidth)]

    return "\n".join(asciiLine)

def checkAvailiableCams(n=10):
    # print availiable capture devices
    devices = []
    for i in range(n):
        # cv2.CAP_DSHOW is required for Windows or not?
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            devices.append(i)
            cap.release()
    print(devices)
    return devices

def generateAsciiFrames():
    capture = cv2.VideoCapture(1)

    print(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        asciiFrame = frameToAscii(frame)
        yield f"{asciiFrame}"
    capture.release()


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("videoflow")
def videoFeed(data):
    for frame in generateAsciiFrames():
        emit("frame", frame)

if __name__ == "__main__":
    # checkAvailiableCams()
    socketio.run(app, debug=True)
