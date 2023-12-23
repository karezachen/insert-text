# import cProfile
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT_PATH = os.path.split(os.path.realpath(__file__))[0]
INPUT_PATH = os.path.join(ROOT_PATH, 'third_words_input')
OUTPUT_PATH = os.path.join(ROOT_PATH, '../insert-text-web/public/third_words_output')
RED_BOX_PATH = os.path.join(ROOT_PATH, 'third_words_red_box')
RED_BOX_TMP_FILE = os.path.join(RED_BOX_PATH, 'tmp.json')

def get_red_box_coordinate(image_name, tmp_red_box_data):
    min_x, min_y, max_x, max_y = tmp_red_box_data.get(image_name, (0, 0, 0, 0))
    if min_x != 0:
        return min_x, min_y, max_x, max_y

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

    tmp_red_box_data[image_name] = (min_x, min_y, max_x, max_y)
    with open(RED_BOX_TMP_FILE, 'w') as json_file:
        json.dump(tmp_red_box_data, json_file, indent=2)

    return min_x, min_y, max_x, max_y

def insert_text(image_name, text, tmp_red_box_data):
    """Insert text into image"""

    image_path = os.path.join(INPUT_PATH, image_name)
    print(f'image_path: {image_path}')
    image = Image.open(image_path)

    width, height = image.size
    print(f'width: {width}px, height: {height}px')

    for index in range(len(text)):
        tmp_text = text[index]
        tmp_image_name = image_name.split('.')[0] + f'_{index + 1}.' + image_name.split('.')[1]
        print(f'Get the red box coordinates of file {tmp_image_name}.')
        min_x, min_y, max_x, max_y = get_red_box_coordinate(tmp_image_name, tmp_red_box_data)
        print(f'The coordinates of the red box are ({min_x}, {min_y}, {max_x}, {max_y}).')

        draw = ImageDraw.Draw(image)

        # font_path = os.path.join(ROOT_PATH, 'fonts/LongCang-Regular.ttf')
        font_path = os.path.join(ROOT_PATH, 'fonts/方正行楷简体.TTF')
        max_width = max_x - min_x
        max_height = max_y - min_y
        font_size = 50
        font = ImageFont.truetype(font_path, font_size)
        f_min_x, f_min_y, f_max_x, f_max_y = font.getbbox(tmp_text)
        while (f_max_x - f_min_x) < max_width and (f_max_y - f_min_y) < max_height:
            font_size += 10
            font = ImageFont.truetype(font_path, size=font_size)
            f_min_x, f_min_y, f_max_x, f_max_y = font.getbbox(tmp_text)

        text_position = (min_x, min_y)

        text_color = 'black'

        draw.text(text_position, tmp_text, font=font, fill=text_color)

    image.save(os.path.join(OUTPUT_PATH, image_name))

def batch_insert_text(text):
    """Traverse the INPUT directory and insert text into all pictures, relying on the red box mark."""
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    with open(RED_BOX_TMP_FILE, 'r') as json_file:
        tmp_red_box_data = json.load(json_file)

    for filename in os.listdir(INPUT_PATH):
        if filename.endswith('.png'):
            print(f'===== Replacing file {filename} =====')
            insert_text(filename, text, tmp_red_box_data)
            print()


if __name__ == '__main__':
    text = '张卓然'
    if len(sys.argv) > 1:
        text = sys.argv[1]
    batch_insert_text(text)
    print('Finish.')

# cProfile.run('batch_insert_text("悦")')
