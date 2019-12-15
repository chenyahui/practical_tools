# 为图片加文字水印

## 特性
* 支持批量添加
* 支持多行水印的添加
* 可指定的水印的字体、颜色和大小
* 可指定水印在图片中的位置（center, top, bottom, left, right, topleft, topright, bottomleft, bottomright）
* 文字自适应图片分辨率大小

##  使用
```shell
$python ./watermark.py -h
usage: watermark.py [-h] -t TEXTS [-o OUTPUT] [-w WIDTH]
                    [-p {center,left,right,top,bottom,topleft,topright,bottomleft,bottomright}]
                    -F FONT [-c COLOR] [-a OPACITY] [-f FILE | -d DIR]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXTS, --text TEXTS
                        The watermark text.
  -o OUTPUT, --output OUTPUT
                        The path of the output file or directory
  -w WIDTH, --width WIDTH
                        The width rate of watermark and image.
  -p {center,left,right,top,bottom,topleft,topright,bottomleft,bottomright}, --position {center,left,right,top,bottom,topleft,topright,bottomleft,bottomright}
  -F FONT, --font FONT  The font type of watermark text.
  -c COLOR, --color COLOR
                        The hex color of watermark.
  -a OPACITY, --opacity OPACITY
                        The opacity of watermark.
  -f FILE, --file FILE  File path of the image you want to add watermark
  -d DIR, --dir DIR     The image directory which you want to batch add
                        watermark
```

批量为一个文件夹中所有图片添加水印
```shell
python watermark.py --text ”测试水印第一行“ --text "测试水印第二行” --font “/Library/Fonts/Songti.ttc” --color "#c8c8c8" --opacity 100 -width 0.8 --dir "./input_dir" --output "./output_dir"
```

为单个图片添加水印
```
python watermark.py --text ”测试水印第一行“ --text "测试水印第二行” --font “/Library/Fonts/Songti.ttc” --color "#c8c8c8" --opacity 100 -width 0.8 --file "./image.png" --output "./output.png"
```


## 依赖
pillow
