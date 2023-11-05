# import cv2
# import numpy as np
# from flask import Flask, render_template, Response, jsonify

# app = Flask(__name__)

# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# cap = cv2.VideoCapture(0)


# def detect_objects(frame):
#     boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
#     count = 0
#     for x, y, w, h in boxes:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         count += 1
#     return count


# def gen_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             count = detect_objects(frame)
#             ret, buffer = cv2.imencode(".jpg", frame)
#             frame = buffer.tobytes()
#             yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/detect")
# def detect():
#     success, frame = cap.read()
#     count = detect_objects(frame)
#     return jsonify(count=count)


# @app.route("/video_feed")
# def video_feed():
#     return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


# if __name__ == "__main__":
#     app.run(debug=True)
import cv2
import base64
import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

cap = cv2.VideoCapture(0)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_objects(frame):
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
    count = 0
    for x, y, w, h in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1
    return count


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    dataURL = request.json["image"]
    image_data = base64.b64decode(dataURL.split(",")[1])
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    count = detect_objects(img)
    return jsonify(count=count)


@socketio.on("image")
def handle_image(image):
    image_data = base64.b64decode(image.split(",")[1])
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    count = detect_objects(img)
    emit("count", count)


if __name__ == "__main__":
    socketio.run(app, debug=True)
