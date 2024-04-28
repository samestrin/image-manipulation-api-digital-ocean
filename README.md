# image-manipulation-api

The image-manipulation-api is a Flask-based web service designed to perform various image processing tasks. It provides endpoints for resizing, cropping, rotating, converting to grayscale, adjusting brightness and contrast, flipping, applying filters, converting formats, adding text, and listing available fonts.

## **Endpoints**

### **Resize Image**

**Endpoint:** `/api/resize` **Method:** POST

Resize an image to the specified width and height.

#### **Parameters**

- `image`: Image file
- `width`: Target width (integer)
- `height`: Target height (integer)

### **Crop Image**

**Endpoint:** `/api/crop` **Method:** POST

Crop an image to the specified coordinates.

#### **Parameters**

- `image`: Image file
- `x1`: Starting x-coordinate of the crop area (integer)
- `y1`: Starting y-coordinate of the crop area (integer)
- `x2`: Ending x-coordinate of the crop area (integer)
- `y2`: Ending y-coordinate of the crop area (integer)

### **Rotate Image**

**Endpoint:** `/api/rotate` **Method:** POST

Rotate an image by the specified angle.

#### **Parameters**

- `image`: Image file
- `angle`: Rotation angle in degrees (float)

### **Convert to Grayscale**

**Endpoint:** `/api/grayscale` **Method:** POST

Convert an image to grayscale.

#### **Parameters**

- `image`: Image file

### **Adjust Brightness**

**Endpoint:** `/api/brightness` **Method:** POST

Adjust the brightness of an image.

#### **Parameters**

- `image`: Image file
- `factor`: Brightness adjustment factor (float)

### **Adjust Contrast**

**Endpoint:** `/api/contrast` **Method:** POST

Adjust the contrast of an image.

#### **Parameters**

- `image`: Image file
- `factor`: Contrast adjustment factor (float)

### **Flip Image**

**Endpoint:** `/api/flip` **Method:** POST

Flip an image horizontally or vertically.

#### **Parameters**

- `image`: Image file
- `axis`: Flip axis (`horizontal` or `vertical`)

### **Apply Filter**

**Endpoint:** `/api/filter` **Method:** POST

Apply a filter to an image.

#### **Parameters**

- `image`: Image file
- `filter_type`: Filter type (`blur`, `sharpen`, or `edge_detect`)

### **Convert Image Format**

**Endpoint:** `/api/convert` **Method:** POST

Convert the format of an image.

#### **Parameters**

- `image`: Image file
- `output_format`: Output format (e.g., `png`, `jpeg`)

### **List Fonts**

**Endpoint:** `/api/list_fonts` **Method:** GET

List available fonts for adding text to images.

### **Add Text to Image**

**Endpoint:** `/api/add_text` **Method:** POST

Add text to an image.

#### **Parameters**

- `image`: Image file
- `text`: Text to add
- `font`: Font type (integer)
- `font_size`: Font size (integer)
- `left`: Left position of the text (integer)
- `top`: Top position of the text (integer)
- `color`: Text color in RGB format (optional)

## **Error Handling**

The API handles errors gracefully and returns appropriate error responses.

- **400 Bad Request**: Invalid request parameters.
- **500 Internal Server Error**: Unexpected server error.
