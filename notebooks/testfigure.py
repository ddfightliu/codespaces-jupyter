'''
Author: dzs-liulinpeng ddfightliu@hotmail.com
Date: 2023-06-13 13:50:52
LastEditors: dzs-liulinpeng ddfightliu@hotmail.com
LastEditTime: 2023-06-13 14:01:43
FilePath: \codespaces-jupyter\notebooks\testfigure.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import win32gui
import win32api
dc=win32gui.GetDC(0)
red=win32api.RGB(255,0,0)

win32gui.