import ctypes
from typing import Any
import colorsys
import math
import time
import random

dll=ctypes.windll
user=dll.user32
gdi=dll.gdi32


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


def GetWorkerW():
    WorkerW=0
    def callback(hwnd, lparam):
        nonlocal WorkerW

        shell = user.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", 0)
        if (shell != 0):
            WorkerW = user.FindWindowExW(0, hwnd, "WorkerW", 0)
        return True

    Proc=ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_void_p)
    user.EnumWindows(Proc(callback), None)

    return WorkerW


def GetWindowSize(hwnd):
    # (width,height)
    rect=RECT()
    ptr=ctypes.pointer(rect)
    user.GetWindowRect(hwnd,ptr)
    return (
        rect.right-rect.left,
        rect.bottom-rect.top,
    )


def hsv2rgb(h,s,v):
    color=colorsys.hsv_to_rgb(math.fmod(h,1),s,v)
    return \
        (int(color[0]*255)<<16)|\
        (int(color[1]*255)<<8)| \
        (int(color[0]*255))
def main():
    workerW=GetWorkerW()
    size=GetWindowSize(workerW)

    hdc=user.GetDC(workerW)
    dc=1/32
    try:
        h=0.00; sh=1
        while True:
            newbrush=gdi.CreateSolidBrush(hsv2rgb(h,1,1))
            gdi.SelectObject(hdc , newbrush)
        
            gdi.Rectangle(hdc , 0 , 0 , size[0] , size[1])
            
            gdi.DeleteObject(newbrush)

            if user.GetAsyncKeyState(0x1b)>>15:
                raise Exception("escape pressed")
            
            h+=dc*sh
            if h-(sh)*0.5==0.5:
                sh=-sh
            
            time.sleep(1/32)
    except Exception as ex:
        print(ex)
        user.ReleaseDC(hdc)


if __name__== "__main__":
    main()