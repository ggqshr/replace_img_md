# 用来将markdown中的图片上传到图床，并将图片替换成对应的url

目前仅支持路过图床

## 使用

```bash

replace_img store # 将登陆的信息缓存下来

replace_img process -o test.md # 将test.md中的图片替换成对应图床上的url。覆盖源文件

replace_img process -no test.md # 不覆盖源文件，而是生成一个process_前缀的文件

```
