"""
    This module contains functions that are used to work with text
"""
import random
import glob
import json
import os
from PIL import ImageFont
import numpy as np
import brochure as br
# -*- coding: utf-8 -*-


def get_random_color(min_val, max_val):
    """
        This function returns red, green and blue values of a color that are
        randomly generated in a given range
    """
    red = random.randint(min_val, max_val)
    green = random.randint(min_val, max_val)
    blue = random.randint(min_val, max_val)

    return red, green, blue


def get_contrasting_color(image=None, block=None, col=(0, 0, 0)):
    """
        This module generates color that is contrasting to the average color
        of the given image
    """
    if col != (0, 0, 0):
        average_color = col
    else:
        cropped = image.crop((block.x, block.y, block.x + block.width, block.y + block.height))
        average_color_row = np.average(cropped, axis=0)
        average_color = np.average(average_color_row, axis=0)

    if average_color[0] < 130 and average_color[1] < 130 and average_color[2] < 130:
        return get_random_color(180, 255)
    return get_random_color(0, 70)


def get_random_file_path(directory, file_type):
    """
        This function returns path of a randon file of the given type
    """
    files = glob.glob(os.path.join(directory, file_type))
    file = random.choice(files)
    return file


def scale_font(txt, font_path, width, height, max_rows=0):
    """
        This function scales size of a given text so that it fits in the
        given bounding box and returns font size and number of lines in which text
        should be divided
    """
    font_size = 1
    rows = 1

    while True:

        font = ImageFont.truetype(font_path, font_size)
        text_bbox = font.getbbox(txt)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        if text_width / rows < width * 0.96 and text_height * rows < height:
            font_size += 1
            continue

        if max_rows and rows == max_rows:
            break

        if text_height * (rows + 1) < height:
            rows += 1
            continue

        break

    return font_size - 1, rows


def divide_text(text, number_of_parts):
    """
        This function divides text in given number of parts, so that each part
        contains full words
    """
    words = text.split()
    words_per_part = len(words) // number_of_parts
    remainder = len(words) % number_of_parts
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

    if remainder != 0:
        last_part = parts[number_of_parts - 1]
        last_part += ' ' + parts[number_of_parts]
        parts[number_of_parts - 1] = last_part

    return parts


def extract_header(text, min_header_length):
    """
        This function extracts header so that it consists only of full words
        and is longer than the minimum given length
    """
    words = text.split()
    selected_words = []
    remaining_text = text

    for word in words:
        selected_words.append(word)
        if len(' '.join(selected_words)) >= min_header_length:
            remaining_text = ' '.join(words[len(selected_words):])
            break

    header = ' '.join(selected_words)
    return header, remaining_text


def wrap_into_lines(text, lines):
    """
        This function wraps text into given number of lines, so that each line is exactly the
        same characters long with respect to the remainder
    """
    segments = []
    text_length = len(text)
    segment_length = text_length // lines
    remainder = text_length % lines
    start = 0

    for _ in range(0, lines):
        end = start + segment_length + (1 if remainder > 0 else 0)
        segments.append(text[start:end])
        start = end
        remainder -= 1

    return segments


def prepare_data_for_json(json_file_path, block):
    x1, y1 = block.x, block.y
    x2, y2 = block.x + block.width, block.y + block.height
    b_box = br.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)
    append_to_json(json_file_path, b_box)


def append_to_json(file_path, b_box):
    """
        This function is used to append text line coordinates to json file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        existing_data = []

    new_entry = {
        "x1": b_box.x1,
        "y1": b_box.y1,
        "x2": b_box.x2,
        "y2": b_box.y2
    }
    existing_data.append(new_entry)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=4)


def delete_file(file_path):
    """
        This function is used to automatically delete json file
    """
    try:
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
