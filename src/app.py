from flask import Flask, request, jsonify
import cv2
import numpy as np
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Function to list available fonts
def list_fonts():
    """Lists available fonts that start with 'FONT_HERSHEY' in OpenCV.

    Returns:
        list: A list of dictionaries containing font names and their respective ids.
    """    
    font_data = [
        {
            'name': f.split('_')[-1].lower(),  # Extract and lowercase name
            'id': getattr(cv2, f)
        }
        for f in dir(cv2) if f.startswith('FONT_HERSHEY')
    ]
    return font_data

# Function to get the file extension from the uploaded file
def get_file_extension(file_storage):
    """Extracts the file extension from a filename.

    Args:
        file_storage (werkzeug.datastructures.FileStorage): The file storage object.

    Returns:
        str: The file extension in lowercase or 'jpg' if no extension is found.
    """    
    filename = file_storage.filename
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'

# Utility to determine content type based on file extension
def get_content_type(extension):
    """Determines the content type based on the file extension.

    Args:
        extension (str): The file extension.

    Returns:
        str: The MIME type corresponding to the extension.
    """    
    if extension in ['jpg', 'jpeg']:
        return 'image/jpeg'
    elif extension == 'gif':
        return 'image/gif'        
    elif extension == 'png':
        return 'image/png'
    return 'application/octet-stream'

@app.route('/', methods=['GET'])
def home():
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/api/resize', methods=['POST'])
def resize_image():
    """Resizes an image to specified dimensions.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    width = int(request.form['width'])
    height = int(request.form['height'])

    resized_image = cv2.resize(image, (width, height))

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, resized_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/crop', methods=['POST'])
def crop_image():
    """Crops an image based on coordinates provided in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    x2 = int(request.form['x2'])
    y2 = int(request.form['y2'])

    cropped_image = image[y1:y2, x1:x2]

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, cropped_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/rotate', methods=['POST'])
def rotate_image():
    """Rotates an image by a specified angle around the center.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    angle = float(request.form['angle'])
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, rotated_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

    return encoded_image.tobytes()

@app.route('/api/grayscale', methods=['POST'])
def convert_to_grayscale():
    """Converts an image to grayscale.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, grayscale_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/brightness', methods=['POST'])
def adjust_brightness():
    """Adjusts the brightness of an image based on a factor.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    factor = float(request.form['factor'])
    adjusted_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, adjusted_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/contrast', methods=['POST'])
def adjust_contrast():
    """Adjusts the contrast of an image based on a factor.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    factor = float(request.form['factor'])
    adjusted_image = cv2.convertScaleAbs(image, alpha=factor, beta=0)

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, adjusted_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/flip', methods=['POST'])
def flip_image():
    """Flips an image either horizontally or vertically based on the axis specified in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    axis = request.form['axis']
    if axis == 'horizontal':
        flipped_image = cv2.flip(image, 1)
    elif axis == 'vertical':
        flipped_image = cv2.flip(image, 0)
    else:
        return jsonify({'error': 'Invalid axis parameter'}), 400

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, flipped_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/filter', methods=['POST'])
def apply_filter():
    """Applies a specified filter (blur, sharpen, or edge detection) to an image.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    filter_type = request.form['filter_type']
    if filter_type == 'blur':
        filtered_image = cv2.GaussianBlur(image, (5, 5), 0)
    elif filter_type == 'sharpen':
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        filtered_image = cv2.filter2D(image, -1, kernel)
    elif filter_type == 'edge_detect':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered_image = cv2.Canny(gray_image, 100, 200)
    else:
        return jsonify({'error': 'Invalid filter type'}), 400

    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, filtered_image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/convert', methods=['POST'])
def convert_image_format():
    """Converts an image to a different format based on the desired output format specified in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    output_format = request.form['output_format']
    _, encoded_image = cv2.imencode('.' + output_format, image)
    content_type = get_content_type(output_format)
    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.route('/api/list_fonts', methods=['GET'])
def get_fonts():
    """List fonts

    Returns:
        json: List of fonts and IDs
    """    
    fonts = list_fonts()
    return jsonify(fonts)

@app.route('/api/add_text', methods=['POST'])
def add_text_to_image():
    """Adds text to an image based on parameters provided in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """    
    image_file = request.files['image']
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Retrieve text and formatting details from the form
    text = request.form['text']
    font = int(request.form['font'])  # Convert font ID to integer
    font_size = float(request.form['font_size'])
    left = int(request.form['left'])
    top = int(request.form['top'])
    color = tuple(map(int, request.form['color'].split(','))) if 'color' in request.form else (255, 255, 255)  # Default color is white

    # Put text on the image
    cv2.putText(image, text, (left, top), font, font_size, color, 2, cv2.LINE_AA)

    # Determine the output format from the uploaded file
    output_format = get_file_extension(image_file)
    _, encoded_image = cv2.imencode('.' + output_format, image)
    content_type = get_content_type(output_format)

    return encoded_image.tobytes(), 200, {'Content-Type': content_type}

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

