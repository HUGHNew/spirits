# spirits

制作和拼接精灵图

> `pipx install spirits`

> `uvx spirits ...`

```bash
# 制作精灵图
spirits scatter example/pypi_logo.png 3 3 # 默认output路径是 ./output
spirits scatter example/pypi_logo.png 3 3 --flex-range 15 # 拆分图片 像素级别检测边界 得到不完全等高等宽的小图
spirits scatter example/pypi_logo.png 3 3 --output-dir example/output

# 拼接精灵图
spirits gather example/compose-4.png example/output/0-0.png example/output/0-1.png example/output/1-0.png example/output/1-1.png  --row 2 --column 2
spirits gather example/compose.png --file example/images.list --row 3 --column  3
```



