import sys
sys.path.append("..")
from img_url_replace.img_upload import ImgUpload
from datetime import datetime

def test_upload():
    obj = ImgUpload()
    obj.uploadImage(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}上传.png","./综合画像.png")