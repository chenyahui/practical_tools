from PIL import Image, ImageDraw, ImageFont
import os

config = {
    "font": 'C:/windows/fonts/simsun.ttc',
    'font-size': 50,
    'rgba': (0, 0, 255, 100),
    'allow_ext': ['png', 'jpg', 'jpeg']
}


def batch_add_waterwalk(input_dir, output_dir, watermarks):

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if extension_of(file) in config['allow_ext']:
                out_root = output_dir + os.sep + root[len(input_dir):]
                if not os.path.exists(out_root):
                    print("create directory:", out_root)
                    os.makedirs(out_root)
                input_path = os.path.join(root, file)
                out_path = os.path.join(out_root, file)
                add_watermark(input_path, out_path, watermarks)
                


def add_watermark(image_path, out_path, watermarks):
    base_img = Image.open(image_path).convert('RGBA')
    txt_img = Image.new('RGBA', base_img.size, (255, 255, 255, 0))
    drawer = ImageDraw.Draw(txt_img)
    text_font = ImageFont.truetype(config["font"], size=config["font-size"])
    pos = calc_position(drawer, text_font, base_img.size, watermarks)

    for index, xy in enumerate(pos):
        drawer.text(
            xy=xy, text=watermarks[index], font=text_font, fill=config['rgba'])

    out = Image.alpha_composite(base_img, txt_img)
    out.save(out_path, "jpeg")
    print("success! add watermark to ", image_path)


# 计算水印所在的位置
def calc_position(drawer, font, image_size, watermarks):
    total_height = 0
    size_infos = []
    for item in watermarks:
        w, h = (drawer.textsize(item, font=font))
        size_infos.append((w, h))
        total_height += h

    margin = (image_size[1] - total_height) / 2
    result = []

    for item in size_infos:
        result.append(((image_size[0] - item[0]) / 2, margin))
        margin += item[1]

    return result


def extension_of(file):
    return os.path.splitext(file)[1][1:]

if __name__ == '__main__':
    # 批量加水印
    batch_add_waterwalk("input_dir/","output_dir/", ["测试水印"]) 

    # 给单个图片加水印
    add_watermark("input.jpg","output.jpg",["测试水印"])
