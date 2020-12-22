from img_upload import ImgUpload
from pathlib import Path

# obj = None


# def setup_module():
#     global obj
#     obj = ImgUpload()


def test_upload():
    with ImgUpload() as obj:
        obj.uploadImage("nihao", Path("./test.png"))
