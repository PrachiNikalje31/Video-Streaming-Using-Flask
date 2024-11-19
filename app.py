from flask import Flask,render_template,Response

import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0) # used to access the webcam  and by default it is 0

def genearte_frames():
    while True:
        # read the camera frames and it take the two parameters
        success,frame = camera.read()
        if not success:
            break
        else:
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
        # yield is because continuously we get the frame nd display it through return we can not come back to this generate function at that time we used the yield 
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(genearte_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)