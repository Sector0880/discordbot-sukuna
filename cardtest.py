import discord
from discord.ext import commands
from discord import app_commands
import yaml

import datetime, time
import locale
from typing import Any, Dict, Generic, List, TYPE_CHECKING, Optional, TypeVar, Union
from time import *
import requests
import enum
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

template_path = "./.db/content/card/template.png"
circle_path =   "./.db/content/card/circle.png"
font_path =     "./.db/content/card/arialmt.ttf"

img = Image.open(template_path)
draw_img = ImageDraw.Draw(img)

draw_img.text((100, 370), f"ID: 43728742948729847", 'black', font = ImageFont.truetype(font_path, 20))
draw_img.text((100, 400), f"sukuna-test", 'black', font = ImageFont.truetype(font_path, 80))

avatar = Image.open("./.db/content/avatar.png")
avatar = avatar.resize((570, 570))

#circle_img = Image.new('RGBA', (200, 200), (255, 255, 255, 255))
circle_img = Image.open(circle_path)
draw_circle = ImageDraw.Draw(circle_img)
#draw_circle.ellipse((0, 0, 200, 200), fill='white', outline=(0, 0, 0), width=4)
draw_circle.text((30, 25), '影', (0, 0, 0), font = ImageFont.truetype("./.db/content/card/simsun.ttc", 150))

img.paste(avatar, (img.width - avatar.width - 50, img.height - avatar.height - 50))
img.paste(circle_img, (img.width - avatar.width - 140, img.height - avatar.height - 70), mask=circle_img)

img.show()