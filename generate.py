import drawSvg as draw
import math

INPUT_PATH = 'input'

GRID_WIDTH = 50
GRID_HEIGHT = 50

IMAGE_WIDTH = 2000

HEX_SIDE_LENGTH = IMAGE_WIDTH / (((GRID_WIDTH - 1) * 1.5) + 2)
HEX_HALF_HEIGHT = (math.sin(math.radians(60)) * HEX_SIDE_LENGTH) 
IMAGE_HEIGHT = ((GRID_HEIGHT + 1) * HEX_HALF_HEIGHT)

def create_grid_from_seed():
    grid = draw.Drawing(IMAGE_WIDTH, IMAGE_HEIGHT)
    
    # r = draw.Rectangle(-80,0,40,50, fill='#1248ff')
    # grid.append(r)

    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):
            hex_scalar = get_seed_scalar(gx, gy)
            
            cx = HEX_SIDE_LENGTH + (gx * 1.5 * HEX_SIDE_LENGTH)
            cy = HEX_HALF_HEIGHT + (gy * HEX_HALF_HEIGHT)

            draw_hex = (gx % 2 == 0 and gy % 2 == 0) or (gx % 2 == 1 and gy % 2 == 1)
            if draw_hex:
                side_length = HEX_SIDE_LENGTH * get_seed_scalar() #TODO do this properly

                points = list(sum(hexagon(cx, cy, side_length), ()))
                hex = draw.Lines(*points, close=True, fill=generate_color(hex_scalar))
                grid.append(hex)

    grid.setPixelScale(2)
    grid.saveSvg('out.svg')


def get_seed_scalar(x=0, y=0) :
    import random
    return 0.95 #random.random()


def generate_color(scalar):
    import random
    r = '%02x' % random.randrange(255)  # todo refactor to generatre col on scalar
    g = '%02x' % random.randrange(255)
    b = '%02x' % random.randrange(255)
    return f'#{r}{g}{b}'


def hexagon(x, y, side_length, height_ratio=1):
    angles = [0, 60, 120, 180, 240, 300]
    points = [(
        x + (side_length * math.cos(math.radians(angle))), 
        height_ratio * (y + (side_length * math.sin(math.radians(angle))))
        ) for angle in angles]
    return points


create_grid_from_seed()