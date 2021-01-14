import requests
import re
from datetime import datetime
from tqdm import tqdm
from typing import Tuple, List, Union
from pathlib import Path
from base64 import b16decode


def time_stp():
    return int(datetime.now().timestamp()*1000)


class ImgUpload(object):
    token_re = 'PF.obj.config.auth_token = "(.*?)"'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer":"https://imgtu.com/login"
    }

    images_url = "https://imgtu.com/i/%s"

    is_login = False

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
        wel_page = self.sess.get("https://imgtu.com/login")
        item = re.search(self.token_re, wel_page.text)
        assert item is not None, "查询token出现问题"
        self.token = item.group(1)
        self.__load_username_password_from_local()
        # 将数据改成下面的形式，使发送的Content-type为form-data
        login_dict = {
            'login-subject': (None,self.username),
            "password": (None,self.passwd),
            'auth_token': (None,self.token),
        }
        self.sess.post("https://imgtu.com/login",
                       files=login_dict, headers=self.headers)
        self.is_login = True

    def __load_username_password_from_local(self) -> Union[str, str]:
        this_file_path = Path(__file__).parent
        this_file = this_file_path.joinpath(".info")
        assert this_file.exists(), "未保存登陆信息，请使用replace_img store，按照提示输入用户名和密码"
        with this_file.open("rb") as f:
            content = f.read()
        decode_content = b16decode(content).decode("utf-8")
        username, passwd = decode_content.split("\1")
        self.username = username
        self.passwd = passwd

    def __init__(self) -> None:
        self.sess = requests.Session()
        # 获取原始的token，与账号关联

    def uploadImage(self, name, path) -> Tuple[str, str, str]:
        if not self.is_login:
            self.__login()
        with open(path, 'rb') as f:
            file_dict = {'source': (name, f)}

            res = self.sess.post("https://imgtu.com/json",
                                 data=self.data_dict, files=file_dict)
            return_res = None
            try:
                this_json = res.json()
                return_res = (
                    name, this_json['image']['url'], self.images_url % this_json['image']['name'])
            except:
                print("###### %s % s" % (str(path), res.text))
                import traceback
                traceback.print_exc()
            return return_res

    def uploadMulImages(self, names, paths) -> List[Tuple[str, str, str]]:
        if not self.is_login:
            self.__login()
        assert len(names) == len(paths), "name和path长度不相同"
        res_list = list()
        for name, path in tqdm(zip(names, paths), total=len(names), desc="uploading..."):
            res_list.append(self.uploadImage(name, path))
        return res_list

    def __login_out(self):
        print("logout....")
        if hasattr(self,"token"):
            self.sess.get("https://imgtu.com/logout/?auth_token=%s" % self.token)

    def close(self):
        print("closeing...")
        self.__login_out()
        self.sess.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
