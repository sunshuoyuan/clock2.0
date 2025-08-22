import network
import urequests
import json
import time
import machine
from framebuf import FrameBuffer as FB
import ssd1306
import ntptime
import dhtx
import neopixel
import random

# WiFi配置
WIFI_SSID = "CU_v3Je"
WIFI_PASSWORD = "n35967hs"
page = 0
# 心知天气配置
API_KEY = "SNvT9_a96JhbZrA4F"  # 心知天气API密钥
UNIT = "c"  # 温度单位
language = "zh-Hans"
today = []
tomorrow = []
after_tomorrow = []
# IP定位服务配置（使用ip-api.com，免费且无需密钥）
IP_LOCATION_URL = "http://ip-api.com/json/?fields=status,message,city,countryCode,lat,lon"
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=300000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.show_fill(0)
rgb = neopixel.NeoPixel(machine.Pin(4), 12, timing=True)
adc36 = machine.ADC(machine.Pin(36))
adc36.atten(machine.ADC.ATTN_11DB)
uart = machine.UART(2, baudrate=9600 ,rx=18 ,tx=17, timeout=10)
day_num = 0
夹 = '0x01,0x00,0x01,0x00,0x01,0x00,0x7F,0xFC,0x01,0x00,0x11,0x10,0x09,0x20,0x01,0x00,0xFF,0xFE,0x01,0x00,0x02,0x80,0x02,0x80,0x04,0x40,0x08,0x20,0x30,0x18,0xC0,0x06,'.replace(
    " ", "")
夹 = FB(bytearray([int('0x' + 夹[i + 2:i + 4]) for i in range(0, len(夹), 5)]), 16, 16, 3)
特 = '0x10,0x20,0x10,0x20,0x50,0x20,0x51,0xFC,0x7C,0x20,0x50,0x20,0x93,0xFE,0x10,0x08, 0x1C,0x08,0xF1,0xFE,0x50,0x08,0x10,0x88,0x10,0x48,0x10,0x08,0x10,0x28,0x10,0x10,'.replace(
    " ", "")
特 = FB(bytearray([int('0x' + 特[i + 2:i + 4]) for i in range(0, len(特), 5)]), 16, 16, 3)
晴 = '0x00,0x20,0x00,0x20,0x7B,0xFE,0x48,0x20,0x49,0xFC,0x48,0x20,0x4B,0xFE,0x78,0x00, 0x49,0xFC,0x49,0x04,0x49,0xFC,0x49,0x04,0x79,0xFC,0x49,0x04,0x01,0x14,0x01,0x08'.replace(
    " ", "")
晴 = FB(bytearray([int('0x' + 晴[i + 2:i + 4]) for i in range(0, len(晴), 5)]), 16, 16, 3)
多 = '0x02,0x00,0x02,0x00,0x07,0xF0,0x08,0x20,0x38,0x40,0x04,0x80,0x03,0x40,0x0C,0x80, 0x71,0xF8,0x02,0x08,0x0C,0x10,0x32,0x20,0x01,0x40,0x01,0x80,0x0E,0x00,0x70,0x00'.replace(
    " ", "")
多 = FB(bytearray([int('0x' + 多[i + 2:i + 4]) for i in range(0, len(多), 5)]), 16, 16, 3)
云 = '0x00,0x00,0x3F,0xF8,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFE,0x02,0x00, 0x04,0x00,0x04,0x00,0x08,0x40,0x10,0x20,0x20,0x10,0x7F,0xF8,0x20,0x08,0x00,0x08'.replace(
    " ", "")
云 = FB(bytearray([int('0x' + 云[i + 2:i + 4]) for i in range(0, len(云), 5)]), 16, 16, 3)
阴 = '0x00,0x00,0x7D,0xFC,0x45,0x04,0x49,0x04,0x49,0x04,0x51,0xFC,0x49,0x04,0x49,0x04, 0x45,0x04,0x45,0xFC,0x45,0x04,0x69,0x04,0x52,0x04,0x42,0x04,0x44,0x14,0x48,0x08'.replace(
    " ", "")
阴 = FB(bytearray([int('0x' + 阴[i + 2:i + 4]) for i in range(0, len(阴), 5)]), 16, 16, 3)
阵 = '0x00,0x40,0x7C,0x40,0x44,0x40,0x4B,0xFE,0x48,0x80,0x50,0xA0,0x49,0x20,0x49,0xFC, 0x44,0x20,0x44,0x20,0x44,0x20,0x6B,0xFE,0x50,0x20,0x40,0x20,0x40,0x20,0x40,0x20'.replace(
    " ", "")
阵 = FB(bytearray([int('0x' + 阵[i + 2:i + 4]) for i in range(0, len(阵), 5)]), 16, 16, 3)
雨 = '0x00,0x00,0xFF,0xFE,0x01,0x00,0x01,0x00,0x01,0x00,0x7F,0xFC,0x41,0x04,0x41,0x04, 0x49,0x44,0x45,0x24,0x41,0x04,0x49,0x44,0x45,0x24,0x41,0x04,0x41,0x14,0x40,0x08'.replace(
    " ", "")
雨 = FB(bytearray([int('0x' + 雨[i + 2:i + 4]) for i in range(0, len(雨), 5)]), 16, 16, 3)
雷 = '0x00,0x00,0x3F,0xF8,0x01,0x00,0x7F,0xFE,0x41,0x02,0x9D,0x74,0x01,0x00,0x1D,0x70, 0x00,0x00,0x3F,0xF8,0x21,0x08,0x21,0x08,0x3F,0xF8,0x21,0x08,0x21,0x08,0x3F,0xF8'.replace(
    " ", "")
雷 = FB(bytearray([int('0x' + 雷[i + 2:i + 4]) for i in range(0, len(雷), 5)]), 16, 16, 3)
冰 = '0x00,0x40,0x40,0x40,0x20,0x40,0x20,0x44,0x00,0x68,0x07,0x70,0x11,0x60,0x11,0x50, 0x21,0x50,0xE2,0x48,0x22,0x48,0x24,0x44,0x28,0x42,0x20,0x40,0x21,0x40,0x00,0x80'.replace(
    " ", "")
冰 = FB(bytearray([int('0x' + 冰[i + 2:i + 4]) for i in range(0, len(冰), 5)]), 16, 16, 3)
雹 = '0x3F,0xF8,0x01,0x00,0x7F,0xFE,0x41,0x02,0x9D,0x74,0x01,0x00,0x1D,0x70,0x08,0x00, 0x1F,0xF0,0x20,0x10,0x5F,0x90,0x10,0x90,0x1F,0xD0,0x10,0x20,0x10,0x04,0x0F,0xFC'.replace(
    " ", "")
雹 = FB(bytearray([int('0x' + 雹[i + 2:i + 4]) for i in range(0, len(雹), 5)]), 16, 16, 3)
小 = '0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x11,0x10,0x11,0x08,0x11,0x04, 0x21,0x04,0x21,0x02,0x41,0x02,0x81,0x02,0x01,0x00,0x01,0x00,0x05,0x00,0x02,0x00'.replace(
    " ", "")
小 = FB(bytearray([int('0x' + 小[i + 2:i + 4]) for i in range(0, len(小), 5)]), 16, 16, 3)
中 = '0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x3F,0xF8,0x21,0x08,0x21,0x08,0x21,0x08, 0x21,0x08,0x21,0x08,0x3F,0xF8,0x21,0x08,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00'.replace(
    " ", "")
中 = FB(bytearray([int('0x' + 中[i + 2:i + 4]) for i in range(0, len(中), 5)]), 16, 16, 3)
大 = '0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0xFF,0xFE,0x01,0x00,0x01,0x00, 0x02,0x80,0x02,0x80,0x04,0x40,0x04,0x40,0x08,0x20,0x10,0x10,0x20,0x08,0xC0,0x06'.replace(
    " ", "")
大 = FB(bytearray([int('0x' + 大[i + 2:i + 4]) for i in range(0, len(大), 5)]), 16, 16, 3)
暴 = '0x1F,0xF0,0x10,0x10,0x1F,0xF0,0x10,0x10,0x1F,0xF0,0x08,0x20,0x7F,0xFC,0x08,0x20, 0xFF,0xFE,0x08,0x20,0x31,0x18,0xC9,0x26,0x05,0x40,0x09,0x20,0x15,0x10,0x22,0x08'.replace(
    " ", "")
暴 = FB(bytearray([int('0x' + 暴[i + 2:i + 4]) for i in range(0, len(暴), 5)]), 16, 16, 3)
冻 = '0x00,0x40,0x40,0x40,0x20,0x40,0x27,0xFE,0x00,0x80,0x09,0x20,0x09,0x20,0x12,0x20, 0x13,0xFC,0xE0,0x20,0x21,0x28,0x21,0x24,0x22,0x22,0x24,0x22,0x20,0xA0,0x00,0x40'.replace(
    " ", "")
冻 = FB(bytearray([int('0x' + 冻[i + 2:i + 4]) for i in range(0, len(冻), 5)]), 16, 16, 3)
雪 = '0x3F,0xF8,0x01,0x00,0x7F,0xFE,0x41,0x02,0x9D,0x74,0x01,0x00,0x1D,0x70,0x00,0x00, 0x3F,0xF8,0x00,0x08,0x00,0x08,0x1F,0xF8,0x00,0x08,0x00,0x08,0x3F,0xF8,0x00,0x08'.replace(
    " ", "")
雪 = FB(bytearray([int('0x' + 雪[i + 2:i + 4]) for i in range(0, len(雪), 5)]), 16, 16, 3)
浮 = '0x00,0x08,0x20,0x3C,0x13,0xC0,0x10,0x04,0x82,0x44,0x41,0x28,0x48,0x00,0x0B,0xF8, 0x10,0x10,0x10,0x20,0xE7,0xFE,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0xA0,0x00,0x40'.replace(
    " ", "")
浮 = FB(bytearray([int('0x' + 浮[i + 2:i + 4]) for i in range(0, len(浮), 5)]), 16, 16, 3)
尘 = '0x01,0x00,0x01,0x00,0x09,0x20,0x09,0x10,0x11,0x08,0x21,0x04,0x41,0x04,0x00,0x00, 0x01,0x00,0x01,0x00,0x3F,0xF8,0x01,0x00,0x01,0x00,0x01,0x00,0xFF,0xFE,0x00,0x00'.replace(
    " ", "")
尘 = FB(bytearray([int('0x' + 尘[i + 2:i + 4]) for i in range(0, len(尘), 5)]), 16, 16, 3)
扬 = '0x10,0x00,0x11,0xF8,0x10,0x10,0x10,0x20,0xFC,0x40,0x10,0x80,0x11,0xFE,0x14,0x92, 0x18,0x92,0x30,0x92,0xD1,0x12,0x11,0x22,0x12,0x22,0x14,0x42,0x50,0x94,0x21,0x08'.replace(
    " ", "")
扬 = FB(bytearray([int('0x' + 扬[i + 2:i + 4]) for i in range(0, len(扬), 5)]), 16, 16, 3)
沙 = '0x00,0x40,0x20,0x40,0x10,0x40,0x11,0x48,0x81,0x44,0x42,0x42,0x42,0x42,0x14,0x48, 0x10,0x48,0x20,0x48,0xE0,0x10,0x20,0x10,0x20,0x20,0x20,0x40,0x21,0x80,0x06,0x00'.replace(
    " ", "")
沙 = FB(bytearray([int('0x' + 沙[i + 2:i + 4]) for i in range(0, len(沙), 5)]), 16, 16, 3)
雾 = '0x3F,0xF8,0x01,0x00,0x7F,0xFE,0x41,0x02,0x9D,0x74,0x01,0x00,0x1D,0x70,0x04,0x00, 0x0F,0xE0,0x14,0x40,0x03,0x80,0x1C,0x70,0xE2,0x0E,0x0F,0xE0,0x04,0x20,0x18,0x60'.replace(
    " ", "")
雾 = FB(bytearray([int('0x' + 雾[i + 2:i + 4]) for i in range(0, len(雾), 5)]), 16, 16, 3)
霾 = '0x3F,0xF8,0x01,0x00,0x7F,0xFE,0x41,0x02,0x9D,0x74,0x30,0x00,0xCB,0xFC,0x2D,0x24, 0x31,0xFC,0xC9,0x24,0x15,0xFC,0x64,0x20,0x0D,0xFC,0x34,0x20,0xC5,0xFE,0x18,0x00'.replace(
    " ", "")
霾 = FB(bytearray([int('0x' + 霾[i + 2:i + 4]) for i in range(0, len(霾), 5)]), 16, 16, 3)
飓 = '0x00,0x00,0x7C,0xF8,0x44,0x88,0x44,0xF8,0x44,0x88,0x4C,0xF8,0x6C,0x88,0x54,0xF8, 0x54,0x88,0x55,0xFC,0x6C,0x00,0x44,0x50,0x44,0x88,0x42,0x02,0x41,0xFE,0x80,0x00'.replace(
    " ", "")
飓 = FB(bytearray([int('0x' + 飓[i + 2:i + 4]) for i in range(0, len(飓), 5)]), 16, 16, 3)
风 = '0x00,0x00,0x3F,0xF0,0x20,0x10,0x20,0x10,0x28,0x50,0x24,0x50,0x22,0x90,0x22,0x90, 0x21,0x10,0x21,0x10,0x22,0x90,0x22,0x92,0x24,0x4A,0x48,0x4A,0x40,0x06,0x80,0x02'.replace(
    " ", "")
风 = FB(bytearray([int('0x' + 风[i + 2:i + 4]) for i in range(0, len(风), 5)]), 16, 16, 3)
卷 = '0x01,0x00,0x11,0x10,0x09,0x20,0x3F,0xF8,0x02,0x00,0x02,0x00,0x7F,0xFC,0x08,0x20, 0x10,0x10,0x2F,0xE8,0xC8,0x26,0x08,0x20,0x08,0xA8,0x08,0x48,0x08,0x08,0x07,0xF8'.replace(
    " ", "")
卷 = FB(bytearray([int('0x' + 卷[i + 2:i + 4]) for i in range(0, len(卷), 5)]), 16, 16, 3)
冷 = '0x00,0x40,0x40,0x40,0x20,0xA0,0x20,0xA0,0x01,0x10,0x02,0x48,0x14,0x26,0x10,0x20, 0x23,0xF8,0xE0,0x08,0x20,0x10,0x21,0x10,0x20,0xA0,0x20,0x40,0x20,0x20,0x00,0x20'.replace(
    " ", "")
冷 = FB(bytearray([int('0x' + 冷[i + 2:i + 4]) for i in range(0, len(冷), 5)]), 16, 16, 3)
热 = '0x10,0x40,0x10,0x40,0x10,0x40,0xFD,0xF8,0x10,0x48,0x10,0x48,0x1C,0xC8,0x30,0x48, 0xD0,0xAA,0x10,0xAA,0x51,0x06,0x22,0x02,0x00,0x00,0x48,0x88,0x44,0x44,0x84,0x44'.replace(
    " ", "")
热 = FB(bytearray([int('0x' + 热[i + 2:i + 4]) for i in range(0, len(热), 5)]), 16, 16, 3)
白 = '0x01,0x00,0x02,0x00,0x04,0x00,0x3F,0xF8,0x20,0x08,0x20,0x08,0x20,0x08,0x20,0x08, 0x3F,0xF8,0x20,0x08,0x20,0x08,0x20,0x08,0x20,0x08,0x20,0x08,0x3F,0xF8,0x20,0x08,'.replace(
    " ", "")
白 = FB(bytearray([int('0x' + 白[i + 2:i + 4]) for i in range(0, len(白), 5)]), 16, 16, 3)
天 = '0x00,0x00,0x3F,0xF8,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0xFF,0xFE,0x01,0x00, 0x02,0x80,0x02,0x80,0x04,0x40,0x04,0x40,0x08,0x20,0x10,0x10,0x20,0x08,0xC0,0x06'.replace(
    " ", "")
天 = FB(bytearray([int('0x' + 天[i + 2:i + 4]) for i in range(0, len(天), 5)]), 16, 16, 3)
夜 = '0x02,0x00,0x01,0x00,0xFF,0xFE,0x08,0x80,0x08,0x80,0x10,0xF8,0x11,0x08,0x31,0x48, 0x52,0x28,0x95,0x10,0x11,0x10,0x10,0xA0,0x10,0x40,0x10,0xA0,0x11,0x18,0x16,0x06'.replace(
    " ", "")
夜 = FB(bytearray([int('0x' + 夜[i + 2:i + 4]) for i in range(0, len(夜), 5)]), 16, 16, 3)
间 = '0x20,0x00,0x13,0xFC,0x10,0x04,0x40,0x04,0x47,0xC4,0x44,0x44,0x44,0x44,0x44,0x44, 0x47,0xC4,0x44,0x44,0x44,0x44,0x44,0x44,0x47,0xC4,0x40,0x04,0x40,0x14,0x40,0x08,'.replace(
    " ", "")
间 = FB(bytearray([int('0x' + 间[i + 2:i + 4]) for i in range(0, len(间), 5)]), 16, 16, 3)
获 = '0x08,0x20,0x08,0x20,0xFF,0xFE,0x08,0x20,0x44,0x40,0x28,0x50,0x10,0x48,0x28,0x40, 0x4F,0xFE,0x98,0x40,0x28,0xA0,0x48,0xA0,0x89,0x10,0x09,0x10,0x52,0x08,0x24,0x06'.replace(
    " ", "")
获 = FB(bytearray([int('0x' + 获[i + 2:i + 4]) for i in range(0, len(获), 5)]), 16, 16, 3)
取 = '0x00,0x00,0xFF,0x80,0x22,0xFC,0x22,0x44,0x3E,0x44,0x22,0x44,0x22,0x44,0x3E,0x44, 0x22,0x28,0x22,0x28,0x27,0xA8,0xFA,0x10,0x42,0x10,0x02,0x28,0x02,0x44,0x02,0x82'.replace(
    " ", "")
取 = FB(bytearray([int('0x' + 取[i + 2:i + 4]) for i in range(0, len(取), 5)]), 16, 16, 3)
时 = '0x00,0x08,0x00,0x08,0x7C,0x08,0x44,0x08,0x45,0xFE,0x44,0x08,0x44,0x08,0x7C,0x08, 0x44,0x88,0x44,0x48,0x44,0x48,0x44,0x08,0x7C,0x08,0x44,0x08,0x00,0x28,0x00,0x10'.replace(
    " ", "")
时 = FB(bytearray([int('0x' + 时[i + 2:i + 4]) for i in range(0, len(时), 5)]), 16, 16, 3)
省略号 = '0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x60,0x60,0x00,0x00'.replace(" ", "")
省略号 = FB(bytearray([int('0x' + 省略号[i + 2:i + 4]) for i in range(0, len(省略号), 5)]), 8, 16, 3)
失 = '0x01,0x00,0x11,0x00,0x11,0x00,0x11,0x00,0x3F,0xF8,0x21,0x00,0x41,0x00,0x01,0x00, 0xFF,0xFE,0x02,0x80,0x04,0x40,0x04,0x40,0x08,0x20,0x10,0x10,0x20,0x08,0xC0,0x06'.replace(
    " ", "")
失 = FB(bytearray([int('0x' + 失[i + 2:i + 4]) for i in range(0, len(失), 5)]), 16, 16, 3)
败 = '0x00,0x40,0x7C,0x40,0x44,0x40,0x54,0x80,0x54,0xFE,0x55,0x08,0x56,0x88,0x54,0x88, 0x54,0x88,0x54,0x50,0x54,0x50,0x10,0x20,0x28,0x50,0x24,0x88,0x45,0x04,0x82,0x02'.replace(
    " ", "")
败 = FB(bytearray([int('0x' + 败[i + 2:i + 4]) for i in range(0, len(败), 5)]), 16, 16, 3)
温 = '0x00,0x00,0x23,0xF8,0x12,0x08,0x12,0x08,0x83,0xF8,0x42,0x08,0x42,0x08,0x13,0xF8, 0x10,0x00,0x27,0xFC,0xE4,0xA4,0x24,0xA4,0x24,0xA4,0x24,0xA4,0x2F,0xFE,0x00,0x00'.replace(
    " ", "")
温 = FB(bytearray([int('0x' + 温[i + 2:i + 4]) for i in range(0, len(温), 5)]), 16, 16, 3)
度 = '0x01,0x00,0x00,0x80,0x3F,0xFE,0x22,0x20,0x22,0x20,0x3F,0xFC,0x22,0x20,0x22,0x20, 0x23,0xE0,0x20,0x00,0x2F,0xF0,0x24,0x10,0x42,0x20,0x41,0xC0,0x86,0x30,0x38,0x0E'.replace(
    " ", "")
度 = FB(bytearray([int('0x' + 度[i + 2:i + 4]) for i in range(0, len(度), 5)]), 16, 16, 3)
湿 = '0x00,0x00,0x27,0xF8,0x14,0x08,0x14,0x08,0x87,0xF8,0x44,0x08,0x44,0x08,0x17,0xF8, 0x11,0x20,0x21,0x20,0xE9,0x24,0x25,0x28,0x23,0x30,0x21,0x20,0x2F,0xFE,0x00,0x00'.replace(
    " ", "")
湿 = FB(bytearray([int('0x' + 湿[i + 2:i + 4]) for i in range(0, len(湿), 5)]), 16, 16, 3)
气 = '0x10,0x00,0x10,0x00,0x3F,0xFC,0x20,0x00,0x4F,0xF0,0x80,0x00,0x3F,0xF0,0x00,0x10, 0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x0A,0x00,0x0A,0x00,0x06,0x00,0x02,'.replace(
    " ", "")
气 = FB(bytearray([int('0x' + 气[i + 2:i + 4]) for i in range(0, len(气), 5)]), 16, 16, 3)
后 = '0x00,0x10,0x00,0xF8,0x1F,0x00,0x10,0x00,0x10,0x00,0x1F,0xFE,0x10,0x00,0x10,0x00, 0x10,0x00,0x17,0xF8,0x14,0x08,0x24,0x08,0x24,0x08,0x44,0x08,0x87,0xF8,0x04,0x08,'.replace(
    " ", "")
后 = FB(bytearray([int('0x' + 后[i + 2:i + 4]) for i in range(0, len(后), 5)]), 16, 16, 3)
明 = '0x00,0x00,0x00,0xFC,0x7C,0x84,0x44,0x84,0x44,0x84,0x44,0xFC,0x7C,0x84,0x44,0x84, 0x44,0x84,0x44,0xFC,0x7C,0x84,0x44,0x84,0x01,0x04,0x01,0x04,0x02,0x14,0x04,0x08,'.replace(
    " ", "")
明 = FB(bytearray([int('0x' + 明[i + 2:i + 4]) for i in range(0, len(明), 5)]), 16, 16, 3)
今 = '0x01,0x00,0x01,0x00,0x02,0x80,0x04,0x40,0x08,0x20,0x12,0x10,0x21,0x08,0xC1,0x06, 0x00,0x00,0x1F,0xF0,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x40,0x00,0x80,0x01,0x00,'.replace(
    " ", "")
今 = FB(bytearray([int('0x' + 今[i + 2:i + 4]) for i in range(0, len(今), 5)]), 16, 16, 3)


def set_beijing_time():
    """设置设备时间为北京时间（UTC+8）"""
    try:
        # 先获取UTC时间
        ntptime.settime()

        # 获取当前UTC时间戳（自1970年1月1日以来的秒数）
        utc_timestamp = time.time()

        # 添加8小时（28800秒）得到北京时间
        beijing_timestamp = utc_timestamp + (8 * 3600)

        # 设置设备时间为北京时间
        rtc = machine.RTC()
        # 将时间戳转换为时间元组
        beijing_time = time.localtime(beijing_timestamp)
        # 设置RTC：年、月、日、星期、时、分、秒、毫秒
        # 注意：星期几需要从0-6转换为1-7（1=星期一，7=星期日）
        weekday = beijing_time[6] + 1  # 原值0-6对应周一到周日，转换为1-7
        rtc.datetime((
            beijing_time[0], beijing_time[1], beijing_time[2], weekday,
            beijing_time[3], beijing_time[4], beijing_time[5], 0
        ))

        # 获取并格式化当前北京时间
        t = time.localtime()
        formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            t[0], t[1], t[2], t[3], t[4], t[5])

        print("时间同步成功! 北京时间:", formatted_time)
        return True

    except Exception as e:
        print("时间设置失败:", e)
        return False


def get_ntp_time(max_retries=3):
    """通过NTP获取时间，带重试机制，并设置为北京时间"""
    # 使用可靠的NTP服务器IP地址（避免DNS解析问题）
    ntp_servers = [
        "132.163.97.4",  # NIST, USA
        "129.6.15.30",  # NIST, USA
        "216.239.35.0",  # Google, USA
        "162.159.200.123",  # Cloudflare, Global
        "203.107.6.88"  # Alibaba, China
    ]

    # 保存原始NTP主机设置
    original_host = ntptime.host if hasattr(ntptime, 'host') else None

    for attempt in range(max_retries):
        try:
            # 尝试不同的NTP服务器
            server = ntp_servers[attempt % len(ntp_servers)]
            print("尝试从 {} 获取时间 (尝试 {}/{})".format(server, attempt + 1, max_retries))

            # 设置NTP服务器
            ntptime.host = server

            # 获取并设置北京时间
            if set_beijing_time():
                return True

        except OSError as e:
            print("错误: {} (代码: {})".format(e, e.args[0]))
            # 常见的错误代码处理建议
            if e.args[0] == -202:
                print("错误 -202: 网络问题，请检查连接")
            elif e.args[0] == 110:  # ETIMEDOUT
                print("错误 110: 连接超时，尝试下一个服务器")
            time.sleep(2)  # 重试前等待

        except Exception as e:
            print("未知错误:", e)
            time.sleep(2)

    # 恢复原始NTP主机设置
    if original_host:
        ntptime.host = original_host

    print("NTP时间获取失败，所有尝试均未成功")
    return False


def setup_wifi(ssid=WIFI_SSID, password=WIFI_PASSWORD):
    """设置并连接WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("连接到WiFi: {0}".format(ssid))
        wlan.connect(ssid, password)

        # 等待连接
        for _ in range(15):
            if wlan.isconnected():
                print("WiFi连接成功!")
                print("IP地址:", wlan.ifconfig()[0])
                return True
            time.sleep(1)
        print("WiFi连接失败!")
        return False
    return True


def get_device_location():
    """通过IP地址获取设备位置信息"""
    try:
        print("获取设备位置...")
        response = urequests.get(IP_LOCATION_URL)
        data = json.loads(response.text)
        response.close()

        if data.get("status") == "success":
            return {
                "city": data.get("city"),
                "country_code": data.get("countryCode"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon")
            }
        else:
            print("定位失败: {0}".format(data.get('message')))
            return None
    except Exception as e:
        print("定位错误: {0}".format(e))
        return None


def get_3day_forecast(location):
    """获取未来三天天气预报"""
    # 使用城市名称或经纬度定位
    location_param = location["city"] if location["city"] else "{0}:{1}".format(location['latitude'],
                                                                                location['longitude'])

    url = "https://api.seniverse.com/v3/weather/daily.json?key={0}&location={1}&language={2}&unit={3}&start=0&days=3".format(
        API_KEY, location_param, language, UNIT)

    try:
        print("获取天气预报...")
        response = urequests.get(url)

        if response.status_code != 200:
            print("天气API错误: {0}".format(response.text))
            response.close()
            return None

        data = json.loads(response.text)
        response.close()
        return data
    except Exception as e:
        print("天气请求错误: {0}".format(e))
        return None


def parse_specific_day(data, location, day_index):
    """解析并显示指定天的天气预报"""
    if not data or "results" not in data:
        print("无有效天气数据")
        if data:
            print("完整响应:", data)
        return []

    try:
        results = data["results"]
        if not results:
            print("无天气预报结果")
            return []

        location_info = results[0]["location"]
        city = location_info["name"]
        country = location_info["country"]

        daily_list = results[0]["daily"]

        # 检查day_index是否有效
        if day_index < 0 or day_index >= len(daily_list):
            print("无效的日期索引: {0}。可用范围: 0-{1}".format(day_index, len(daily_list) - 1))
            return []

        daily = daily_list[day_index]
        date_str = daily["date"][5:10]  # 提取MM-DD
        weather_day = daily["text_day"]
        weather_night = daily["text_night"]
        low_temp = daily["low"]
        high_temp = daily["high"]

        # 创建友好的日期名称
        day_names = ["今天", "明天", "后天"]
        day_name = day_names[day_index] if day_index < len(day_names) else date_str

        print("\n=== {0}, {1} 指定日天气预报 ===".format(city, country))
        print("日期: {0} ({1})".format(date_str, day_name))
        print("白天: {0}".format(weather_day))
        print("夜间: {0}".format(weather_night))
        print("温度: {0}~{1}°{2}".format(low_temp, high_temp, UNIT.upper()))
        return [date_str, str(day_index), int(daily["code_day"]), int(daily["code_night"]), low_temp, high_temp,
                UNIT.upper()]

    except KeyError as e:
        print("数据解析错误, 缺少字段: {0}".format(e))


def get_weather():
    # 主程序
    if setup_wifi():
        location = get_device_location()

        if location:
            print("检测到位置: {0}, {1}".format(location['city'], location['country_code']))
            forecast_data = get_3day_forecast(location)

            if forecast_data:
                # 在这里指定要输出的天数索引
                # 0 = 今天, 1 = 明天, 2 = 后天
                day_to_show = 0  # 这里设置为显示明天的天气

                # 注意：现在调用的是 parse_specific_day，并传递了三个参数
                global today, tomorrow, after_tomorrow
                today = parse_specific_day(forecast_data, location, day_to_show)
                day_to_show = 1
                tomorrow = parse_specific_day(forecast_data, location, day_to_show)
                day_to_show = 2
                after_tomorrow = parse_specific_day(forecast_data, location, day_to_show)
                return 1
            else:
                print("获取天气预报失败")
                global today, tomorrow, after_tomorrow
                today = tomorrow = after_tomorrow = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
                return 0
        else:
            print("无法确定位置，使用默认城市")
            location = {"city": "北京", "country_code": "CN", "latitude": 39.9042, "longitude": 116.4074}
            forecast_data = get_3day_forecast(location)
            if forecast_data:
                day_to_show = 1  # 显示明天的天气
                parse_specific_day(forecast_data, location, day_to_show)
            return 1


def out(a, b, c):
    if b[c] == 0 or b[c] == 1 or b[c] == 2 or b[c] == 3:
        oled.framebuf.blit(晴, 32, a)
    elif b[c] == 4 or b[c] == 5 or b[c] == 6 or b[c] == 7 or b[c] == 8:
        oled.framebuf.blit(多, 32, a)
        oled.framebuf.blit(云, 48, a)
    elif b[c] == 9:
        oled.framebuf.blit(阴, 32, a)
    elif b[c] == 10:
        oled.framebuf.blit(阵, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == 11:
        oled.framebuf.blit(雷, 32, a)
        oled.framebuf.blit(阵, 48, a)
        oled.framebuf.blit(雨, 54, a)
    elif b[c] == 12:
        oled.framebuf.blit(雷, 32, a)
        oled.framebuf.blit(阵, 48, a)
        oled.framebuf.blit(雨, 64, a)
        oled.framebuf.blit(冰, 80, a)
        oled.framebuf.blit(雹, 96, a)
    elif b[c] == 13:
        oled.framebuf.blit(小, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == 14:
        oled.framebuf.blit(中, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == 15:
        oled.framebuf.blit(大, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == a:
        oled.framebuf.blit(暴, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == 17:
        oled.framebuf.blit(大, 32, a)
        oled.framebuf.blit(暴, 48, a)
        oled.framebuf.blit(雨, 64, a)
    elif b[c] == 18:
        oled.framebuf.blit(特, 32, a)
        oled.framebuf.blit(大, 48, a)
        oled.framebuf.blit(暴, 64, a)
        oled.framebuf.blit(雨, 80, a)
    elif b[c] == 19:
        oled.framebuf.blit(冻, 32, a)
        oled.framebuf.blit(雨, 48, a)
    elif b[c] == 20:
        oled.framebuf.blit(雨, 32, a)
        oled.framebuf.blit(夹, 48, a)
        oled.framebuf.blit(雪, 64, a)
    elif b[c] == 21:
        oled.framebuf.blit(阵, 32, a)
        oled.framebuf.blit(雪, 48, a)
    elif b[c] == 22:
        oled.framebuf.blit(小, 32, a)
        oled.framebuf.blit(雪, 48, a)
    elif b[c] == 23:
        oled.framebuf.blit(中, 32, a)
        oled.framebuf.blit(雪, 48, a)
    elif b[c] == 24:
        oled.framebuf.blit(大, 32, a)
        oled.framebuf.blit(雪, 48, a)
    elif b[c] == 25:
        oled.framebuf.blit(暴, 32, a)
        oled.framebuf.blit(雪, 48, a)
    elif b[c] == 26:
        oled.framebuf.blit(浮, 32, a)
        oled.framebuf.blit(尘, 48, a)
    elif b[c] == 27:
        oled.framebuf.blit(扬, 32, a)
        oled.framebuf.blit(沙, 48, a)
    elif b[c] == 28:
        oled.framebuf.blit(沙, 32, a)
        oled.framebuf.blit(尘, 48, a)
        oled.framebuf.blit(暴, 64, a)
    elif b[c] == 29:
        oled.framebuf.blit(强, 32, a)
        oled.framebuf.blit(沙, 48, a)
        oled.framebuf.blit(尘, 64, a)
        oled.framebuf.blit(暴, 80, a)
    elif b[c] == 30:
        oled.framebuf.blit(雾, 32, a)
    elif b[c] == 31:
        oled.framebuf.blit(霾, 32, a)
    elif b[c] == 32:
        oled.framebuf.blit(风, 32, a)
    elif b[c] == 33:
        oled.framebuf.blit(大, 32, a)
        oled.framebuf.blit(风, 48, a)
    elif b[c] == 34:
        oled.framebuf.blit(飓, 32, a)
        oled.framebuf.blit(风, 48, a)
    elif b[c] == 35:
        oled.framebuf.blit(热, 32, a)
        oled.framebuf.blit(带, 48, a)
        oled.framebuf.blit(风, 64, a)
        oled.framebuf.blit(暴, 80, a)
    elif b[c] == 36:
        oled.framebuf.blit(龙, 32, a)
        oled.framebuf.blit(卷, 48, a)
        oled.framebuf.blit(风, 64, a)
    elif b[c] == 37:
        oled.framebuf.blit(冷, 32, a)
    elif b[c] == 38:
        oled.framebuf.blit(热, 32, a)
    else:
        oled.text('N/A', 32, a)


def out2(a, b):
    oled.framebuf.blit(a, 0, 0)
    oled.framebuf.blit(天, 16, 0)
    oled.text(b[0], 32, 4)
    oled.framebuf.blit(白, 0, 16)
    oled.framebuf.blit(天, 16, 16)
    oled.framebuf.blit(夜, 0, 32)
    oled.framebuf.blit(间, 16, 32)
    oled.framebuf.blit(温, 0, 48)
    oled.framebuf.blit(度, 16, 48)


# 先连接WiFi
oled.framebuf.blit(获, 20, 24)
oled.framebuf.blit(取, 36, 24)
oled.framebuf.blit(时, 52, 24)
oled.framebuf.blit(间, 68, 24)
oled.framebuf.blit(中, 84, 24)
oled.framebuf.blit(省略号, 100, 24)
oled.framebuf.blit(省略号, 104, 24)
oled.framebuf.blit(省略号, 108, 24)
oled.show()
if setup_wifi(WIFI_SSID, WIFI_PASSWORD):
    # 获取NTP时间并设置为北京时间
    get_ntp_time()

    # 显示本地时间（无论NTP是否成功）
    t = time.localtime()
    local_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])
    print("设备本地时间:", local_time)

else:
    oled.show_fill(0)
    oled.framebuf.blit(获, 15, 24)
    oled.framebuf.blit(取, 31, 24)
    oled.framebuf.blit(时, 47, 24)
    oled.framebuf.blit(间, 63, 24)
    oled.framebuf.blit(失, 79, 24)
    oled.framebuf.blit(败, 95, 24)
    oled.show()
    print("无法连接到WiFi，跳过时间同步")
    time.sleep(3)
oled.show_fill(0)
before_data = "0"
before_time = "0"
before_page = 4


def output_weather():
    oled.vline(64, 0, 64, 1)
    oled.vline(65, 0, 64, 1)
    oled.framebuf.blit(白, 0, 0)
    oled.framebuf.blit(天, 16, 0)
    oled.framebuf.blit(夜, 0, 16)
    oled.framebuf.blit(间, 16, 16)
    oled.show()


def digitalRead(p):
    pin0 = machine.Pin(p, machine.Pin.IN)
    return pin0.value()


def reget_weather():
    oled.show_fill(0)
    oled.framebuf.blit(获, 20, 24)
    oled.framebuf.blit(取, 36, 24)
    oled.framebuf.blit(天, 52, 24)
    oled.framebuf.blit(气, 68, 24)
    oled.framebuf.blit(中, 84, 24)
    oled.framebuf.blit(省略号, 100, 24)
    oled.framebuf.blit(省略号, 104, 24)
    oled.framebuf.blit(省略号, 108, 24)
    oled.show()
    if get_weather():
        print(today)
        print(tomorrow)
        print(after_tomorrow)
    else:
        oled.show_fill(0)
        oled.framebuf.blit(获, 15, 24)
        oled.framebuf.blit(取, 31, 24)
        oled.framebuf.blit(天, 47, 24)
        oled.framebuf.blit(气, 63, 24)
        oled.framebuf.blit(失, 79, 24)
        oled.framebuf.blit(败, 95, 24)
        oled.show()
        print("无法获取天气")
        time.sleep(3)
reget_weather()
oled.show_fill(0)
oled.show()
before_data = "0"
before_time = "0"
t = time.localtime()
now_hour, now_minute, now_second = t[3], t[4], t[5]
now_hour = now_hour % 12
now_minute = now_minute // 5
now_second = now_second // 5
before_hour, before_minute, before_second = now_hour, now_minute, now_second
rgb[now_hour] = (255, 0, 0)
rgb[now_minute] = (0, 255, 0)
rgb[now_second] = (0, 0, 255)
rgb.write()
while 1:
    darkness = not adc36.read()
    if darkness:
        oled.show_fill(0)
        for i in range(0, 12):
            rgb[i] = (0, 0, 0)
        rgb.write()
        page = 0
        continue
    rgb[now_hour] = (255, 0, 0)
    rgb[now_minute] = (0, 255, 0)
    rgb[now_second] = (0, 0, 255)
    rgb.write()
    t = time.localtime()
    now_data = "{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2])
    now_time = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
    oled.text(now_data, 24, 30)
    oled.text(now_time, 32, 40)
    now_hour, now_minute, now_second = t[3], t[4], t[5]
    now_hour = now_hour % 12
    now_minute = now_minute // 5
    now_second = now_second // 5
    if page == 0 and before_page != 0:
        if not now_data == before_data:
            oled.fill_rect(0, 32, 128, 8, 0)
            oled.text(now_data, 24, 30)
            oled.show()
            before_data = now_data
        if not now_time == before_time:
            oled.fill_rect(0, 40, 128, 8, 0)
            oled.text(now_time, 32, 40)
            oled.framebuf.blit(温, 0, 0)
            oled.framebuf.blit(度, 16, 0)
            oled.text(str(dhtx.get_dht_temperature('dht11', 16)), 33, 6)
            oled.framebuf.blit(湿, 70, 0)
            oled.framebuf.blit(度, 86, 0)
            oled.text(str(dhtx.get_dht_relative_humidity('dht11', 16)), 103, 6)
            oled.show()
    if now_hour != before_hour:
        rgb[before_hour] = (0, 0, 0)
        rgb[now_hour] = (255, 0, 0)
        rgb.write()
    if now_minute != before_minute:
        rgb[before_minute] = (0, 0, 0)
        rgb[now_minute] = (0, 255, 0)
        rgb.write()
    if now_second != before_second:
        rgb[before_second] = (0, 0, 0)
        rgb[now_second] = (0, 0, 255)
        rgb.write()
    before_hour, before_minute, before_second = now_hour, now_minute, now_second
    before_time = now_time
    if uart.any():
        order = uart.readline()
        if myvariable == b'\xf4\xf5\x06\x00\xf1\x0b':
            page += 1
    if digitalRead(2):
        time.sleep(1)
        if digitalRead(2):
            page += 1
            oled.show_fill(0)
    if page == 4:
        page = 0
    if page == -1:
        page = 3
    if page == 1 and before_page != 1:
        out2(今, today)
        # 白天
        out(16, today, 2)
        # 夜间
        out(32, today, 3)
        if after_tomorrow[4] == 'N/A':
            oled.text('N/A', 32, 52)
        else:
            t_out = after_tomorrow[4] + '-' + after_tomorrow[5] + '\'' + after_tomorrow[6]
            oled.text(t_out, 32, 52)
        oled.show()
        before_page = 1
    if page == 2 and before_page != 2:
        out2(明, tomorrow)
        # 白天
        out(16, tomorrow, 2)
        # 夜间
        out(32, tomorrow, 3)
        if tomorrow[4] == 'N/A':
            oled.text('N/A', 32, 52)
        else:
            t_out = tomorrow[4] + '-' + tomorrow[5] + '\'' + tomorrow[6]
            oled.text(t_out, 32, 52)
        oled.show()
        before_page = 2
    if page == 3 and before_page != 3:
        out2(后, after_tomorrow)
        # 白天
        out(16, after_tomorrow, 2)
        # 夜间
        out(32, after_tomorrow, 3)
        if after_tomorrow[4] == 'N/A':
            oled.text('N/A', 32, 52)
        else:
            t_out = after_tomorrow[4] + '-' + after_tomorrow[5] + '\'' + after_tomorrow[6]
            oled.text(t_out, 32, 52)
        oled.show()
        before_page = 3
    if  t[4] == 0 and t[5] == 0:
        reget_weather()
    if t[2] == 15 and t[3] == 15 and t[4] == 15 and t[5] == 15:
        machine.reset()

