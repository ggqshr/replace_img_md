import re
from img_upload import ImgUpload
from pathlib import Path
import click
from pprint import pprint
from base64 import b16encode

img_re = r"\!\[(?P<name>.*)\]\((?P<path>.*)\)"


@click.command()
@click.option("--overwrite/--no-overwrite", "-o/-no", type=bool, default=True, help="是否直接将原来的文件重写，默认为True")
@click.argument("file_path", type=str, required=True)
def process(overwrite, file_path):
    """
    处理md文件的主题逻辑，包括查找替换的部分，和上传图片的逻辑。
    """
    prefix = ""
    if not overwrite:
        prefix = "processed_"

    file = Path(file_path)
    this_aub_path = file.absolute().parent
    names, paths = [], []
    origin_content = []
    file_content = file.read_text(encoding='utf-8')
    for index, item in enumerate(re.finditer(img_re, file_content)):
        gorup_dict = item.groupdict()
        name = "%s_%s" % (file.stem, index)
        temp_path = gorup_dict.get("path")
        if temp_path.startswith("http"):
            continue
        path = this_aub_path.joinpath(temp_path)
        names.append(name)
        paths.append(path)
        origin_content.append(item.group())

    print("从%s共找到%d处需要替换:" % (file.name, len(names)))
    if len(names) == 0:
        return
    pprint(origin_content)

    with ImgUpload() as obj:
        final_item = obj.uploadMulImages(names, paths)

    for item, origin_c in zip(final_item, origin_content):
        name, url, show_url = item
        new_content = "[![%s](%s)](%s)" % (name, url, show_url)
        file_content = re.sub(re.escape(origin_c),
                              new_content, file_content, count=1)

    with open("%s%s" % (prefix, file.name), "w", encoding="utf-8") as f:
        f.write(file_content)


@click.command()
@click.option("--name", prompt="请输入用户名")
@click.option("--password", prompt="请输入密码", hide_input=True, confirmation_prompt="请再次输入密码")
def store(name, password):
    """
    存储密码的使用的逻辑，因为要上传到网络上，无法直接把密码写成明文放到代码里，则需要每次存在本地
    """
    info_str = "%s\1%s" % (name, password)
    info = b16encode(info_str.encode("utf-8"))
    this_path = Path(__file__).parent
    with this_path.joinpath(".info").open("wb") as f:
        f.write(info)


@click.group()
def cli():
    pass


cli.add_command(store)
cli.add_command(process)

if __name__ == "__main__":
    cli()
