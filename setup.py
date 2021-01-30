import setuptools

with open("README.md", "r",encoding="utf-8") as f:
    long_desc = f.read()

setuptools.setup(
    name="replace_md_img",
    version="0.0.13",
    author="ggq",
    author_email="ggq18663278150@gmail.com",
    description='一个python脚本，用来将markdown中的图片上传到图床上，并替换文档中的链接',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['replace_img = img_url_replace.parse_md:main']
    },
    url="https://github.com/ggqshr/replace_img_md",
    install_requires=[
        'tqdm',
        'requests',
        'click',
    ],
)
