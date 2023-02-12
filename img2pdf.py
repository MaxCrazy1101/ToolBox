# 将img文件夹下的图片转为pdf，一张图片占用一个a4大小纸张，等比例缩放，其余地方填充白色
# author: Alex Newton
from PIL import Image
import os

a4_size_mm = (595, 842)


def image_resize(img, width, height):
    """
    图片缩放
    :param img: 图片
    :param width: 宽
    :param height: 高
    :return: 修改后的图片
    """
    return img.resize((width, height), Image.Resampling.LANCZOS)


def image2pdf(img_path, pdf_path=None, resize=True):
    """
    图片转PDF
    :param img: 图片路径
    :param pdf_path: 生成的PDF路径
    :param resize: 是否缩放图片至A4大小
    :return: None
    """
    file_list = sorted(os.listdir(img_path))
    images = []
    for x in file_list:
        img = Image.open("./img/" + x)
        img = img.convert("RGB")
        # img.show()
        images.append(img)
        # a4_bottom.show()
    images.pop(0).save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images)


if __name__ == "__main__":
    image2pdf("./img", "./1.pdf")
