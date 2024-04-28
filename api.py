from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/api/resize', methods=['POST'])
def resize_image():
    # Get image data from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get width and height parameters
    width = int(request.form['width'])
    height = int(request.form['height'])

    # Resize the image
    resized_image = cv2.resize(image, (width, height))

    # Encode resized image to bytes
    _, encoded_image = cv2.imencode('.jpg', resized_image)

    return encoded_image.tobytes()

# Define other API endpoints in a similar manner

if __name__ == '__main__':
    app.run(debug=True)
