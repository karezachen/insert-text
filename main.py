from PIL import Image, ImageDraw, ImageFont
import os

INPUT_PATH = 'input'
OUTPUT_PATH = 'output'
RED_BOX_PATH = 'red_box'

text_positions = {
    'Smile.png': (268, 20),
    'Dear.png': (200, 100),
    'Baby.png': (200, 100),
}

def get_red_box_coordinate(image_name):
    """"""

    image_path = os.path.join(RED_BOX_PATH, image_name)
    image = Image.open(image_path)

    rgb_image = image.convert('RGB')

    width, height = image.size

    red_boxes = []

    for x in range(width):
        for y in range(height):
            r, g, b = rgb_image.getpixel((x, y))

            if r > 200 and g < 100 and b < 100:
                red_boxes.append((x, y))

    min_x = min(red_boxes, key=lambda x: x[0])[0]
    min_y = min(red_boxes, key=lambda x: x[1])[1]
    max_x = max(red_boxes, key=lambda x: x[0])[0]
    max_y = max(red_boxes, key=lambda x: x[1])[1]

    return min_x, min_y, max_x, max_y

def insert_text(image_name, text):
    """Insert text into image"""

    image_path = os.path.join(INPUT_PATH, image_name)
    image = Image.open(image_path)

    width, height = image.size
    print(f'width: {width}px, height: {height}px')
   
    min_x, min_y, max_x, max_y = get_red_box_coordinate(image_name)
    print(f'The coordinates of the red box are ({min_x}, {min_y}, {max_x}, {max_y}).')

    draw = ImageDraw.Draw(image)

    font_path = 'fonts/LongCang-Regular.ttf'
    max_width = max_x - min_x
    max_height = max_y - min_y
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)
    print(f'font.get name {font.getname()}')
    while (font.getbbox(text)[2] - font.getbbox(text)[0]) < max_width and (font.getbbox(text)[3] - font.getbbox(text)[1]) < max_height:
        font_size += 10
        font = ImageFont.truetype(font_path, size=font_size)


    text_position = (min_x, min_y)

    text_color = 'black'

    draw.text(text_position, text, font=font, fill=text_color)

    image.save(os.path.join(OUTPUT_PATH, image_name))

def batch_insert_text(text):

    """Traverse the INPUT directory and insert text into all pictures, relying on the red box mark."""
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    for filename in os.listdir(INPUT_PATH):
        if filename.endswith('.png'):
            print(f'===== Replacing file {filename} =====')
            insert_text(filename, text)
            print()


if __name__ == '__main__':
    text = '娇'
    batch_insert_text(text)
