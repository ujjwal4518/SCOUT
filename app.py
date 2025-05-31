from flask import Flask, render_template, Response
from fire import detect_fire
from fall import detect_falls


app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/fire')
def video_feed_fire():
    """Streams the video feed with fire detection."""
    return Response(detect_fire(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/fall')
def video_feed_fall():
    """Stream video from the fall detection system."""
    return Response(detect_falls(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug = True)
