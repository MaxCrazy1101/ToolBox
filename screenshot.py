import time

# import pyautogui

import numpy as np
from PIL import ImageGrab
import cv2
import win32gui, win32ui, win32con, win32api


def screenshot_PIL():
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    # img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    return img


def screenshot_win32(win_title, bbox=None):
    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    hwnd = win32gui.FindWindow(None, win_title)
    if hwnd == 0:
        print(f"没有找到窗口:{win_title},请检查窗口名称是否正确!")
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()

    # 指定截图区域
    if bbox is None:
        # 获取监控器信息
        x, y = 0, 0
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
    else:
        x, y, w, h = bbox
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)

    img = np.frombuffer(signedIntsArray, dtype="uint8")
    img.shape = (h, w, 4)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # 释放内存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    mfcDC.DeleteDC()
    saveDC.DeleteDC()

    return img
    # saveBitMap.SaveBitmapFile(saveDC, filename)


def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # hwnd = win32gui.FindWindow(None, "ck-auto")
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


def screenshot_pg():
    img = pyautogui.screenshot(region=[0, 0, 1920, 1080])  # x,y,w,h
    return img


# img.save('screenshot.png')
# img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


def show_all_hwnd_title():
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if (
            win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)
        ):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t is not None:
            print(h, t)


# def screenshot_pyqt5():
#     from PyQt5.QtWidgets import QApplication
#     from PyQt5.QtGui import *
#     import win32gui
#     import sys

#     hwnd = win32gui.FindWindow(None, 'C:\Windows\system32\cmd.exe')
#     app = QApplication(sys.argv)
#     screen = QApplication.primaryScreen()
#     img = screen.grabWindow(hwnd).toImage()
#     img.save("screenshot.jpg")


def branch_screenshot():
    time_begin = time.time()
    for _ in range(10):
        screenshot_PIL()
    time_end = time.time()
    print(f"PIL 截图10次耗时{time_end-time_begin} FPS:{1/((time_end-time_begin)/10.0)}")


def test_screenshot():
    while True:
        img = screenshot_win32(win_title="none_bot_test – E:\Datastruct\\none_bot_test\\ayaka_setting.json",bbox=(100,100,200,200))
        cv2.imshow("grab_win32", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    test_screenshot()
    # window_capture("test.png")
    show_all_hwnd_title()
