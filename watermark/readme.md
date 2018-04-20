# 为图片加文字水印

## 特性
* 支持批量添加
* 支持多行水印的添加
* 可定制的水印的字体、颜色和大小

##  使用
批量为一个文件夹中所有图片添加水印
```python
 batch_add_waterwalk("input_dir/","output_dir/", ["测试水印"]) 
```
为单个图片添加水印
```
add_watermark("input.jpg","output.jpg",["测试水印"])
```

## 配置项
```python
config = {
    "font": 'C:/windows/fonts/simsun.ttc', # 字体位置
    'font-size': 50, # 水印大小
    'rgba': (0, 0, 255, 100), # rgba
    'allow_ext': ['png', 'jpg', 'jpeg'] # 允许的后缀
}
```
## 依赖
PIL
