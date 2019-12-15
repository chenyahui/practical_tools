import os
import math
import argparse

from PIL import Image, ImageDraw, ImageFont

ALLOW_EXTENSION = ('png', 'jpg', 'jpeg')


class Positions(object):
    class Position(object):
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __or__(self, other):
            return self.__class__(self.x + other.x, self.y + other.y)

    CENTER = Position(0, 0)
    TOP = Position(0, -1)
    BOTTOM = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)


def batch_add_watermark(input_dir, output_dir, watermarks, font_path, width_rate, rgba):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if extension_of(file) not in ALLOW_EXTENSION:
                continue

            out_root = output_dir + os.sep + root[len(input_dir):]
            if not os.path.exists(out_root):
                print("Create directory:", out_root)
                os.makedirs(out_root)

            input_path = os.path.join(root, file)
            out_path = os.path.join(out_root, file)
            add_watermark(input_path, out_path, watermarks, font_path, width_rate, rgba)


def add_watermark(image_path, out_path, watermarks, font_path, width_rate, rgba):
    base_img = Image.open(image_path).convert('RGBA')
    txt_img = Image.new('RGBA', base_img.size, (255, 255, 255, 0))
    drawer = ImageDraw.Draw(txt_img)

    font = calc_font(drawer, watermarks, font_path, width_rate)

    pos = calc_coordinates(drawer, font, watermarks)

    for index, xy in enumerate(pos):
        drawer.text(xy=xy, text=watermarks[index], font=font, fill=rgba)

    out = Image.alpha_composite(base_img, txt_img)
    if os.path.isdir(out_path):
        out_path = os.path.join(out_path, name_of(image_path))
    out.save(out_path, extension_of(image_path))
    print('OK. Save to', out_path)


def calc_font(drawer, watermarks, font_path, width_rate):
    """
    按指定的水印宽度比例计算合适的字号
    :param drawer: ImageDrawer
    :param watermarks: 水印文本列表
    :param font_path: 字体文件路径
    :param width_rate: 水印宽度与图片宽度之比
    :return: ImageFont
    """
    text_font = ImageFont.truetype(font_path, size=50)
    max_width = 0
    for item in watermarks:
        w, _ = (drawer.textsize(item, font=text_font))
        max_width = max(max_width, w)
    font_size = math.floor(drawer.im.size[0] * width_rate * 50 / max_width)
    return ImageFont.truetype(font_path, size=font_size)


def calc_coordinates(drawer, font, watermarks, position=Positions.BOTTOM | Positions.RIGHT):
    """
    按指定位置计算水印在图片中的坐标
    :param drawer: ImageDrawer
    :param font: ImageFont
    :param watermarks: 水印文本列表
    :param position: 水印的位置
    :return: list or coordinates
    """
    total_height = 0
    sizes = []
    for item in watermarks:
        w, h = (drawer.textsize(item, font=font))
        sizes.append((w, h))
        total_height += h

    top_margin = 0
    if position.y < 0:
        top_margin = 0
    if position.y == 0:
        top_margin = (drawer.im.size[1] - total_height) / 2
    if position.y > 0:
        top_margin = (drawer.im.size[1] - total_height)

    result = []
    for item in sizes:
        if position.x < 0:
            result.append((0, top_margin))
        elif position.x == 0:
            result.append(((drawer.im.size[0] - item[0]) / 2, top_margin))
        elif position.x > 0:
            result.append(((drawer.im.size[0] - item[0]), top_margin))
        top_margin += item[1]

    return result


def extension_of(file):
    return os.path.splitext(file)[1].lstrip('.').lower()


def name_of(file):
    return file.split(os.path.sep)[-1]


def hex_to_rgb(hex_color):
    if not (len(hex_color) == 7 and hex_color.startswith('#')):
        raise Exception('Invalid color code: %s.' % hex_color)

    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
    except Exception:
        raise Exception('Invalid color code: %s.' % hex_color)
    return r, g, b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str, required=True, action='append', dest='texts', default=[], help="The watermark text.")
    parser.add_argument('-o', '--output', type=str, help="The path of the output file or directory")
    parser.add_argument('-w', '--width', type=float, default=0.5, help="The width rate of watermark and image.")
    parser.add_argument('-p', '--position', default='bottomright', choices=('center', 'left', 'right', 'top', 'bottom', 'topleft', 'topright', 'bottomleft', 'bottomright'))
    parser.add_argument('-F', '--font', required=True, help="The font type of watermark text.")
    parser.add_argument('-c', '--color', default='#c8c8c8', help="The hex color of watermark.")
    parser.add_argument('-a', '--opacity', type=int, default=100, help="The opacity of watermark.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', type=str, help="File path of the image you want to add watermark")
    group.add_argument('-d', '--dir', type=str, help="The image directory which you want to batch add watermark")

    results = parser.parse_args()

    if not 0 < results.width < 1:
        print('error: argument -w/--width: value should be in range (0, 1)')
        return

    if not 0 <= results.opacity <= 255:
        print('error: argument -a/--opacity: value should be in range [0, 255]')
        return

    if not results.file and not results.dir:
        print('error: arguments -f/--file and -d/--dir should not all be None')
        return

    if not os.path.exists(results.file or results.dir):
        print('error: argument -f/--file or -d/--dir path does not exists.')
        return

    r, g, b = hex_to_rgb(results.color)

    if results.file:
        # 给单个图片加水印
        add_watermark(
            image_path=results.file,
            out_path=results.output,
            watermarks=results.texts,
            font_path=results.font,
            width_rate=results.width,
            rgba=(r, g, b, results.opacity)
        )
    if results.dir:
        # 批量加水印
        batch_add_watermark(
            input_dir=results.dir,
            output_dir=results.output,
            watermarks=results.texts,
            font_path=results.font,
            width_rate=results.width,
            rgba=(r, g, b, results.opacity)
        )


if __name__ == '__main__':
    main()
