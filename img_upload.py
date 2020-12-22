import requests
import re
from datetime import datetime
from tqdm import tqdm
from typing import Tuple, List


def time_stp():
    return int(datetime.now().timestamp()*1000)


class ImgUpload(object):
    token_re = 'PF.obj.config.auth_token = "(.*?)"'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    images_url = "https://imgchr.com/i/%s"

    @property
    def data_dict(self):
        return {
            "type": "file",
            "action": "upload",
            "timestamp": str(time_stp()),
            "auth_token": self.token,
            "nsfw": "0",
        }

    def __login(self):
        print("login....")
        wel_page = self.sess.get("https://imgchr.com/")
        item = re.search(self.token_re, wel_page.text)
        assert item is not None, "查询token出现问题"
        self.token = item.group(1)
        # todo 从本地读取账号和密码，如果读不到的话 就弹出提示
        login_dict = {
            'login-subject': "ggq",
            "password": "5515225gg5",
            'auth_token': self.token,
        }
        res = self.sess.post("https://imgchr.com/login",
                             data=login_dict, headers=self.headers)

    def __init__(self) -> None:
        self.sess = requests.Session()
        # 获取原始的token，与账号关联
        self.__login()

    def uploadImage(self, name, path) -> Tuple[str, str, str]:
        with open(path, 'rb') as f:
            file_dict = {'source': (name, f)}

            res = self.sess.post("https://imgchr.com/json",
                                 data=self.data_dict, files=file_dict)
            this_json = res.json()
            return (name, this_json['image']['url'], self.images_url % this_json['image']['name'])

    def uploadMulImages(self, names, paths) -> List[Tuple[str, str, str]]:
        assert len(names) == len(paths), "name和path长度不相同"
        res_list = list()
        for name, path in tqdm(zip(names, paths), total=len(names), desc="uploading..."):
            res_list.append(self.uploadImage(name, path))
        return res_list

    def __login_out(self):
        print("logout....")
        self.sess.get("https://imgchr.com/logout/?auth_token=%s" % self.token)

    def close(self):
        print("closeing...")
        self.__login_out()
        self.sess.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
