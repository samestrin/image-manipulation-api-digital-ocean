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

@app.route('/api/grayscale', methods=['POST'])
def convert_to_grayscale():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Encode grayscale image to bytes
    _, encoded_image = cv2.imencode('.jpg', grayscale_image)

    return encoded_image.tobytes()

@app.route('/api/brightness', methods=['POST'])
def adjust_brightness():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get brightness factor parameter
    factor = float(request.form['factor'])

    # Adjust brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)

    # Encode adjusted image to bytes
    _, encoded_image = cv2.imencode('.jpg', adjusted_image)

    return encoded_image.tobytes()

@app.route('/api/contrast', methods=['POST'])
def adjust_contrast():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get contrast factor parameter
    factor = float(request.form['factor'])

    # Adjust contrast
    adjusted_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)

    # Encode adjusted image to bytes
    _, encoded_image = cv2.imencode('.jpg', adjusted_image)

    return encoded_image.tobytes()

@app.route('/api/flip', methods=['POST'])
def flip_image():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get flip axis parameter
    axis = request.form['axis']

    # Flip the image
    if axis == 'horizontal':
        flipped_image = cv2.flip(image, 1)
    elif axis == 'vertical':
        flipped_image = cv2.flip(image, 0)
    else:
        return jsonify({'error': 'Invalid axis parameter'})

    # Encode flipped image to bytes
    _, encoded_image = cv2.imencode('.jpg', flipped_image)

    return encoded_image.tobytes()

# Define other API endpoints in a similar manner

if __name__ == '__main__':
    app.run(debug=True)
