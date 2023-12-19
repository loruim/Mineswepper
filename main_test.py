import pytest
import math
import pygame as pg
import pyautogui
import main

def test_cell_size():
    for div in range(40, 1600, 40):
        assert main.Cell_quantity(div) == div//40    

def test_Windows_size():
    for div in range(1, 101):
        result1, result2 = main.Windows(div, div)
        assert result1 == (div, div)
        assert result2.get_width() == div
        assert result2.get_height() == div