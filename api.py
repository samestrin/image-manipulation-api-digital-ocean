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

@app.route('/api/crop', methods=['POST'])
def crop_image():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get crop parameters
    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    x2 = int(request.form['x2'])
    y2 = int(request.form['y2'])

    # Crop the image
    cropped_image = image[y1:y2, x1:x2]

    # Encode cropped image to bytes
    _, encoded_image = cv2.imencode('.jpg', cropped_image)

    return encoded_image.tobytes()

@app.route('/api/rotate', methods=['POST'])
def rotate_image():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get rotation angle parameter
    angle = float(request.form['angle'])

    # Get image dimensions
    height, width = image.shape[:2]

    # Rotate the image around its center
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Encode rotated image to bytes
    _, encoded_image = cv2.imencode('.jpg', rotated_image)

    return encoded_image.tobytes()


# Define other API endpoints in a similar manner

if __name__ == '__main__':
    app.run(debug=True)
