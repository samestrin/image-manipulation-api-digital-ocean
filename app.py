from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Function to list available fonts
def list_fonts():
    fonts = [getattr(cv2, f) for f in dir(cv2) if f.startswith('FONT_HERSHEY')]
    return fonts

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

@app.route('/api/filter', methods=['POST'])
def apply_filter():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get filter type parameter
    filter_type = request.form['filter_type']

    # Apply filter
    if filter_type == 'blur':
        filtered_image = cv2.GaussianBlur(image, (5, 5), 0)
    elif filter_type == 'sharpen':
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        filtered_image = cv2.filter2D(image, -1, kernel)
    elif filter_type == 'edge_detect':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered_image = cv2.Canny(gray_image, 100, 200)
    else:
        return jsonify({'error': 'Invalid filter_type parameter'})

    # Encode filtered image to bytes
    _, encoded_image = cv2.imencode('.jpg', filtered_image)

    return encoded_image.tobytes()

@app.route('/api/convert', methods=['POST'])
def convert_image_format():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get output format parameter
    output_format = request.form['output_format']

    # Encode image to the specified output format
    _, encoded_image = cv2.imencode('.' + output_format, image)

    return encoded_image.tobytes()

@app.route('/api/list_fonts', methods=['GET'])
def get_fonts():
    fonts = list_fonts()
    return jsonify(fonts)

@app.route('/api/add_text', methods=['POST'])
def add_text_to_image():
    # Read image from request
    image_data = np.fromstring(request.files['image'].read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Get text and font parameters
    text = request.form['text']
    font = int(request.form['font'])  # Convert font to int
    font_size = int(request.form['font_size'])
    left = int(request.form['left'])
    top = int(request.form['top'])
    color = tuple(map(int, request.form['color'].split(','))) if 'color' in request.form else (0, 0, 255)  # Default: Red

    # Add text to the image
    cv2.putText(image, text, (left, top), font, font_size, color, 2, cv2.LINE_AA)

    # Encode image to bytes
    _, encoded_image = cv2.imencode('.jpg', image)

    return encoded_image.tobytes(), 200, {'Content-Type': 'image/jpeg'}


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

