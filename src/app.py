from flask import Flask, request, jsonify
import cv2
import numpy as np
from flask_cors import CORS 
import asyncio

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
            'name': f.lower(),  # Extract and lowercase name
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

# Async function to process image manipulations
async def process_image(image_data, process_func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, process_func, image_data, *args, **kwargs)
    return result

def decode_image(image_file):
    image_data = np.frombuffer(image_file.read(), dtype=np.uint8)
    return cv2.imdecode(image_data, cv2.IMREAD_COLOR)

def encode_image(image, output_format):
    _, encoded_image = cv2.imencode('.' + output_format, image)
    return encoded_image.tobytes()

def handle_image_request(process_func, request):
    image_file = request.files['image']
    output_format = get_file_extension(image_file)
    image = decode_image(image_file)
    processed_image = process_func(image, **request.form.to_dict(flat=True))
    encoded_image = encode_image(processed_image, output_format)
    content_type = get_content_type(output_format)
    return encoded_image, 200, {'Content-Type': content_type}


@app.route('/', methods=['GET'])
def home():
    return jsonify({'error': 'Method not allowed'}), 405

# Endpoint functions refactored to use handle_image_request
@app.route('/api/resize', methods=['POST'])
def resize_image():
    """Resizes an image to specified dimensions.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def resize_func(image, width, height):
        return cv2.resize(image, (int(width), int(height)))
    return handle_image_request(resize_func, request)

@app.route('/api/crop', methods=['POST'])
def crop_image():
    """Crops an image based on coordinates provided in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def crop_func(image, x1, y1, x2, y2):
        return image[int(y1):int(y2), int(x1):int(x2)]
    return handle_image_request(crop_func, request)

@app.route('/api/rotate', methods=['POST'])
def rotate_image():
    """Rotates an image by a specified angle around the center.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def rotate_func(image, angle):
        height, width = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        return cv2.warpAffine(image, rotation_matrix, (width, height))
    return handle_image_request(rotate_func, request)

# Endpoint functions refactored to use handle_image_request
@app.route('/api/grayscale', methods=['POST'])
def convert_to_grayscale():
    """Converts an image to grayscale.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def grayscale_func(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return handle_image_request(grayscale_func, request)

@app.route('/api/brightness', methods=['POST'])
def adjust_brightness():
    """Adjusts the brightness of an image based on a factor.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def brightness_func(image, factor):
        return cv2.convertScaleAbs(image, alpha=float(factor), beta=0)
    return handle_image_request(brightness_func, request)

@app.route('/api/contrast', methods=['POST'])
def adjust_contrast():
    """Adjusts the contrast of an image based on a factor.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def contrast_func(image, factor):
        return cv2.convertScaleAbs(image, alpha=float(factor), beta=0)
    return handle_image_request(contrast_func, request)

@app.route('/api/flip', methods=['POST'])
def flip_image():
    """Flips an image either horizontally or vertically based on the axis specified in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def flip_func(image, axis):
        if axis == 'horizontal':
            return cv2.flip(image, 1)
        elif axis == 'vertical':
            return cv2.flip(image, 0)
        else:
            return None
    return handle_image_request(flip_func, request)

@app.route('/api/filter', methods=['POST'])
def apply_filter():
    """Applies a specified filter (blur, sharpen, or edge detection) to an image.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def filter_func(image, filter_type):
        if filter_type == 'blur':
            return cv2.GaussianBlur(image, (5, 5), 0)
        elif filter_type == 'sharpen':
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            return cv2.filter2D(image, -1, kernel)
        elif filter_type == 'edge_detect':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.Canny(gray_image, 100, 200)
        else:
            return None
    return handle_image_request(filter_func, request)

@app.route('/api/convert', methods=['POST'])
def convert_image_format():
    """Converts an image to a different format based on the desired output format specified in the form.

    Returns:
        tuple: A tuple containing the binary image data, response code, and content type header.
    """
    def convert_func(image, output_format):
        _, encoded_image = cv2.imencode('.' + output_format, image)
        content_type = get_content_type(output_format)
        return encoded_image.tobytes(), 200, {'Content-Type': content_type}
    return handle_image_request(convert_func, request)

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
    def add_text(image, text, font, font_size, left, top, color):
        """Adds text to the image.

        Args:
            image (numpy.ndarray): The input image.
            text (str): The text to be added.
            font (int): The font ID.
            font_size (float): The font size.
            left (int): The left position of the text.
            top (int): The top position of the text.
            color (tuple): The color of the text.

        Returns:
            numpy.ndarray: The image with the text added.
        """
        cv2.putText(image, text, (left, top), font, font_size, color, 2, cv2.LINE_AA)
        return image

    return handle_image_request(add_text, request)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

