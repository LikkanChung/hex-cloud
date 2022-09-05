import drawSvg as draw
from PIL import Image
import numpy as np
import math
import uuid
import os

###############################################################

GRID_WIDTH = 60
GRID_HEIGHT = 40

IMAGE_WIDTH = 1000

SCALAR_SIZE = True
MIN_SIZE = 0.05
MAX_SIZE = 0.975
SIZE_GENERATOR_SEED_IMAGE = 'square_gradient_2.jpeg'  # assumed greyscale image
# white pixels = larger hex

SCALAR_COLOR = True
INVERSE_COLOR = True  
COLOR_GENERATOR_SEED_IMAGE = 'square_gradient_2.jpeg'  # assumed greyscale image

###############################################################

HEX_SIDE_LENGTH = IMAGE_WIDTH / (((GRID_WIDTH - 1) * 1.5) + 2)
HEX_HALF_HEIGHT = (math.sin(math.radians(60)) * HEX_SIDE_LENGTH) 
IMAGE_HEIGHT = ((GRID_HEIGHT + 1) * HEX_HALF_HEIGHT)

def load_seed_image(filepath, target_width, target_height): 
    image = Image.open(filepath)
    resized_image = image.resize((target_width, target_height), resample=Image.Resampling.BILINEAR)
    # pixelate image to target size
    return np.array(resized_image)

INPUT_PATH = 'input'
SIZE_GENERATOR_FILE_PATH = os.path.join(INPUT_PATH, SIZE_GENERATOR_SEED_IMAGE)
SIZE_SCALAR_SEED = load_seed_image(SIZE_GENERATOR_FILE_PATH, GRID_WIDTH, GRID_HEIGHT)
COLOR_GENERATOR_FILE_PATH = os.path.join(INPUT_PATH, COLOR_GENERATOR_SEED_IMAGE)
COLOR_SCALAR_SEED = load_seed_image(COLOR_GENERATOR_FILE_PATH, GRID_WIDTH, GRID_HEIGHT)

OUTPUT_PATH = 'output'

def create_grid_from_seed():
    grid = draw.Drawing(IMAGE_WIDTH, IMAGE_HEIGHT)

    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):            
            cx = HEX_SIDE_LENGTH + (gx * 1.5 * HEX_SIDE_LENGTH)
            cy = HEX_HALF_HEIGHT + (gy * HEX_HALF_HEIGHT)

            draw_hex = (gx % 2 == 0 and gy % 2 == 0) or (gx % 2 == 1 and gy % 2 == 1)
            if draw_hex:
                side_length = HEX_SIDE_LENGTH * ( get_seed_scalar(SIZE_SCALAR_SEED ,gx, gy, MIN_SIZE, MAX_SIZE) if SCALAR_SIZE else 1 )

                points = list(sum(hexagon(cx, cy, side_length), ()))
                hex_color_scalar = get_seed_scalar(COLOR_SCALAR_SEED,gx, gy)
                
                hex = draw.Lines(*points, close=True, fill=generate_color(hex_color_scalar))
                grid.append(hex)

    grid.setPixelScale(2)
    output_file_name = str(uuid.uuid4())[:8]
    output_file_path = f'{os.path.join(OUTPUT_PATH, output_file_name)}.svg'
    grid.saveSvg(output_file_path)
    print(output_file_path)

def get_seed_scalar(seed, x, y, min_value=0, max_value=1) :
    size_range = max_value - min_value
    # inverse y axis
    normalised_scalar = (seed[GRID_HEIGHT - y - 1][x] / 255)
    return min_value + (normalised_scalar * size_range)


def generate_color(scalar):
    scalar = 1 - scalar if INVERSE_COLOR else scalar
    r = '%02x' % int(scalar * 255)  # todo refactor to generatre col on scalar
    g = '%02x' % int(scalar * 255)
    b = '%02x' % int(scalar * 255)
    return f'#{r}{g}{b}'


def hexagon(x, y, side_length, height_ratio=1):
    angles = [0, 60, 120, 180, 240, 300]
    points = [(
        x + (side_length * math.cos(math.radians(angle))), 
        height_ratio * (y + (side_length * math.sin(math.radians(angle))))
        ) for angle in angles]
    return points


create_grid_from_seed()