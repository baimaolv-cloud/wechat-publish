# -*- coding: utf-8 -*-
"""数字经济封面图 - 边际成本归零曲线"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 900, 383

img = Image.new("RGB", (W, H), (10, 18, 40))
d = ImageDraw.Draw(img)

# 背景装饰：横向渐变条
for y in range(H):
    brightness = int(15 + (y / H) * 20)
    r = int(brightness * 1.2)
    g = int(brightness * 1.8)
    b = int(brightness * 3.0)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 网格线（淡）
for x in range(0, W, 60):
    d.line([(x, 60), (x, H - 40)], fill=(30, 60, 120), width=1)
for y in range(60, H - 40, 50):
    d.line([(0, y), (W, y)], fill=(30, 60, 120), width=1)

# 坐标轴
ax, ay = 100, H - 60
bx, by = W - 60, H - 60
cx, cy = 100, 80
d.line([(ax, ay), (bx, by)], fill=(120, 180, 255), width=2)  # X轴
d.line([(ax, ay), (cx, cy)], fill=(120, 180, 255), width=2)  # Y轴

# 标签
try:
    font_label = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    font_axis = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
    font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
except:
    font_label = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 16)
    font_axis = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 14)
    font_title = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 28)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 18)
    font_small = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 13)

# X轴标签
d.text((bx - 20, by + 5), "Q", fill=(120, 180, 255), font=font_axis)
d.text((ax - 30, cy + 5), "P", fill=(120, 180, 255), font=font_axis)
d.text((ax - 60, ay + 5), "0", fill=(120, 180, 255), font=font_small)

# 绘制 MC 曲线（边际成本趋近于零）
# y = P = c / (Q^alpha)，alpha < 1 让曲线接近双曲线形态
points = []
for i in range(1, 800):
    q = i * 1.0
    # 边际成本随产量增加而下降，趋近于零
    p = 280.0 / (q ** 0.35)
    if p > ay - cy:
        p = ay - cy
    x = ax + q * 0.9
    y = ay - p
    if x > bx:
        break
    points.append((x, y))

# 填充区域
fill_pts = [(ax, ay)] + points + [(bx, ay)]
poly_fill = []
for pt in fill_pts:
    poly_fill.append(pt[0])
    poly_fill.append(pt[1])
if len(poly_fill) >= 4:
    d.polygon(poly_fill, fill=(20, 80, 180, 80))

# 画曲线
for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    # 渐变颜色
    ratio = i / len(points)
    r = int(0 + ratio * 60)
    g = int(180 + ratio * 75)
    b = int(255)
    d.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=3)

# 箭头指向零
arrow_x = ax + 750 * 0.9
arrow_y = ay - 280.0 / (750 ** 0.35)
if arrow_y < cy:
    arrow_y = cx + 30
d.line([(arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y - 10)], fill=(100, 200, 255), width=2)

# 标注 MC
mc_x = ax + 580 * 0.9
mc_y = ay - 280.0 / (580 ** 0.35)
d.text((mc_x + 10, mc_y - 25), "MC", fill=(80, 220, 255), font=font_small)

# 零成本标注
zero_x = ax + 720 * 0.9
zero_y = ay - 280.0 / (720 ** 0.35) - 20
d.text((zero_x, zero_y - 5), "→ 0", fill=(255, 200, 80), font=font_small)

# 标题
title = "数字经济的本质"
d.text((int(W / 2 - 140), 15), title, fill=(255, 255, 255), font=font_title)

subtitle = "边际成本趋近于零"
d.text((int(W / 2 - 130), 48), subtitle, fill=(100, 220, 255), font=font_sub)

# 底部装饰线
d.line([(0, H - 35), (W, H - 35)], fill=(60, 120, 220), width=2)

# 底部标注
d.text((20, H - 25), "边际成本 MC", fill=(80, 200, 255), font=font_small)
d.text((20, H - 10), "产量 Q", fill=(80, 200, 255), font=font_small)
d.text((W - 180, H - 25), "数字经济", fill=(255, 200, 80), font=font_small)
d.text((W - 180, H - 10), "边际成本 → 0", fill=(255, 200, 80), font=font_small)

# 右上角数据标注框
d.rectangle([W - 220, 10, W - 10, 65], fill=(20, 50, 100, 180))
d.text((W - 215, 15), "P", fill=(120, 180, 255), font=font_small)
d.text((W - 190, 15), "= MC(Q) = C / Q^α", fill=(200, 230, 255), font=font_small)
d.text((W - 215, 35), "α < 1", fill=(200, 230, 255), font=font_small)
d.text((W - 215, 52), "→ 规模递减，趋近于零", fill=(180, 220, 255), font=font_small)

out_path = r"C:\Users\mac\.qclaw\workspace\tools\cover_digital_economy.png"
img.save(out_path)
print("Saved:", out_path)