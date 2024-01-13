from shutil import get_archive_formats
import random
import os
import glob
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from enum import Enum
# -*- coding: utf-8 -*-


def random_color():

    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


def get_contrasting_color(image, x, y, segment_width, segment_height):

    cropped = image.crop((x, y, x + segment_width, y + segment_height))
    average_color_row = np.average(cropped, axis=0)
    average_color = np.average(average_color_row, axis=0)

    dif = 255 * random.uniform(0.8, 1.2)
    color = tuple(int(max(0, min(255, abs(x - dif)))) for x in average_color)

    return color


def get_random_file_path(directory, type):
    files = glob.glob(os.path.join(directory, type))
    file = random.choice(files)
    return file


def insert_image(image, path, x, y, block_width, block_height):

  insert = Image.open(path)
  insert = insert.resize((block_width, block_height), Image.Resampling.LANCZOS)
  image.paste(insert, (x,y))


def decide_on_part(columns, rows):

    text_blocks = 0
    matrix = [[0] * columns for _ in range(rows)]

    for j in range(columns):
      for i in range(rows):

        choice = np.random.choice(np.arange(1, 5), p=[0.1, 0.3, 0.3, 0.3])
        matrix[i][j] = choice
        if choice == 3 or choice == 4:
            text_blocks += 2
        elif choice == 2:
            text_blocks += 1

    if text_blocks == 0:
      print("0 text blocks! Regenerating!")
      return decide_on_part(columns, rows)

    return matrix, text_blocks


def scale_font(text, font_path, width, height):

    fontsize = 1
    rows = 1

    while True:

        font = ImageFont.truetype(font_path, fontsize)
        text_size = font.getsize(text)
        row_width = text_size[0] / rows

        if row_width < width and text_size[1] * rows < height:
            fontsize += 1
            continue
        elif text_size[1] * rows < height:
            rows += 1
            continue

        break

    wrapped_text = wrap(text, rows)
    resize_flag = True

    l = rows
    while resize_flag:

        for line in wrapped_text:

            font = ImageFont.truetype(font_path, fontsize)
            text_size = font.getsize(line)

            if text_size[0] * l / rows > width:
                fontsize -= 1
                rows += 1
                break

            if text_size[1] * rows > height:
                rows -= 1

            resize_flag = False

    if rows == 0: rows = 1
    return fontsize, rows


def divide_text(text, num_parts):

    words = text.split()
    words_per_part = len(words) // num_parts

    parts = []
    current_part = []
    current_word_count = 0

    for word in words:

        current_part.append(word)
        current_word_count += 1

        if current_word_count >= words_per_part:

            parts.append(' '.join(current_part))
            current_part = []
            current_word_count = 0

    if current_part:
        parts.append(' '.join(current_part))

    return parts


def extract_header(text, min_length):

    words = text.split()
    selected_words = []
    remaining_text = text

    for word in words:
        selected_words.append(word)
        if len(' '.join(selected_words)) >= min_length:
            remaining_text = ' '.join(words[len(selected_words):])
            break

    header = ' '.join(selected_words)
    return header, remaining_text


def wrap(text, parts):

    segments = []
    text_length = len(text)
    segment_length = text_length // parts
    remainder = text_length % parts
    start = 0

    for i in range(0, parts):
        end = start + segment_length + (1 if remainder > 0 else 0)
        segments.append(text[start:end])
        start = end
        remainder -= 1

    return segments


def put_text_in_block(text, x, y, block_width, block_height, font_path, color, draw):

    font_size, lines = scale_font(text, font_path, block_width, block_height)
    wrapped_text = wrap(text, lines)
    font_ = ImageFont.truetype(font_path, font_size)
    textsize = font_.getsize(text)

    for i, line in enumerate(wrapped_text):
        y_final = y + i * textsize[1]
        draw.text((x, y_final), line, font=font_, fill=color)

