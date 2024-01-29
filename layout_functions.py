"""
    This module contains functions that are used to generate layouts for brochures
"""
import random
import glob
import os
import cv2
import csv
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import text_functions as tf
import tables as t
import graphs as g
import brochure as br

# -*- coding: utf-8 -*-
COMMON_PATH = '' #'/content/drive/MyDrive/dataset_generation/'
INDEX = 100
JSON_FILE = 'text_lines_locations/text_locations_' + str(INDEX) + '.json'
JSON_TABLES = 'table_locations/tables_' + str(INDEX) + '.json'
JSON_TEXT_BLOCKS = 'text_blocks_locations/text_blocks_' + str(INDEX) + '.json'

def get_entire_text():
    """
        This function is used to get text that is used to
        generate brochure from random text file
    """
    dataset_path = COMMON_PATH + 'sample_text'
    text_files = glob.glob(os.path.join(dataset_path, '*.txt'))
    file = random.choice(text_files)

    with open(file, 'r', encoding='utf-8') as f:
        entire_text = f.read()

    return entire_text


def generate_brochure_layout(width, height):
    """
        This function generates general brochure layout as a matrix and
        calculates in how many blocks you have to divide initial text
    """
    columns = random.randint(1, 4) if width > height else random.randint(1, 3)
    rows = random.randint(1, 3) if width > height else random.randint(1, 4)
    matrix = [[0] * columns for _ in range(rows)]
    text_blocks_amount = 0

    for j in range(columns):
        for i in range(rows):

            choice = np.random.choice(np.arange(1, 5), p=[0.15, 0.2, 0.25, 0.4])
            matrix[i][j] = choice
            if choice in (3, 4):
                text_blocks_amount += 2
            elif choice == 2:
                text_blocks_amount += 1

    if text_blocks_amount == 0:
        print("0 text blocks! Regenerating!")
        return generate_brochure_layout(width, height)

    return matrix, text_blocks_amount, rows, columns


def determine_type_of_image(brochure, block):
    """
        This function is used to decide on type of image to use for
        the given block and insert it
    """
    image_choice = np.random.choice(np.arange(1, 4), p=[0.5, 0.4, 0.1])
    if image_choice == 1:
        tf.prepare_data_for_json(JSON_TABLES, block)
        insert_path = t.generate_table(block.width, block.height)
    elif image_choice == 2:
        insert_path = g.generate_plot(block.width, block.height)
    elif image_choice == 3:
        insert_path = tf.get_random_file_path(COMMON_PATH + 'sample_insert_images', '*.jpg')

    insert_image(brochure, insert_path, block)


def generate_brochure_params():
    """
        This function is used to generate brochure parameters
    """
    path = tf.get_random_file_path(COMMON_PATH + 'sample_images', '*.jpg')
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    left_margin = random.randint(20, width // 20)
    top_margin = random.randint(20, height // 10)
    matrix, text_parts, rows, columns = generate_brochure_layout(width, height)

    brochure = br.Brochure(rows=rows, columns=columns, width=width,
                           height=height, layout_matrix=matrix,
                           text_parts=text_parts, left_margin=left_margin,
                           top_margin=top_margin, image=image, draw=draw)

    return brochure


def put_text_and_image_in_block(text, brochure, block, image_path, font_path, color):
    """
        This function scales image and text so that it fits in a
        given bounding box
    """
    is_vertical = block.height > block.width
    direction = random.choice(['down', 'up']) if is_vertical else random.choice(['left', 'right'])
    image_ratio = random.uniform(0.3, 0.5)
    image_size = int((block.height if is_vertical else block.width) * image_ratio)

    if is_vertical:

        image_margin = block.height * random.uniform(0.05, 0.1)
        x_image = block.x
        y_image = block.y + (block.height - image_size) if direction == 'down' else block.y
        x_text = block.x
        y_text = block.y if direction == 'down' else block.y + image_size + image_margin
        im_width = block.width
        im_height = image_size
        text_width = block.width
        text_height = block.height - image_size - image_margin

    else:

        image_margin = block.width * random.uniform(0.05, 0.1)
        x_image = block.x + (block.width - image_size) if direction == 'right' else block.x
        y_image = block.y
        x_text = block.x if direction == 'right' else block.x + image_size + image_margin
        y_text = block.y
        im_width = image_size
        im_height = block.height
        text_width = block.width - image_size - image_margin
        text_height = block.height

    image_block = br.BrochureBlock(width=im_width, height=im_height, x=x_image, y=y_image)
    text_block = br.BrochureBlock(width=text_width, height=text_height, x=x_text, y=y_text)

    tf.prepare_data_for_json(JSON_TEXT_BLOCKS, block)
    insert_image(brochure, image_path, image_block)
    put_text_in_block(text, brochure, text_block, font_path, color, True)


def put_text_in_block(text, brochure, block, font_path, color, write, max_rows=0, font_size=0):
    """
        This function divides text in lines and scales them so that
        they fit in a given bounding box
    """

    if font_size == 0:
        font_size, lines = tf.scale_font(text, font_path, block.width, block.height, max_rows)
    else:
        lines = max_rows
    wrapped_text = tf.wrap_into_lines(text, lines)
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = font.getbbox(text)
    text_height = text_bbox[3] - text_bbox[1]

    for i, line in enumerate(wrapped_text):

        y_final = block.y + i * text_height
        brochure.draw.text((block.x, y_final), line, font=font, fill=color)

        if write:

            background_color = tf.get_contrasting_color(col=color)
            image = Image.new("RGB", (int(block.x + block.width + 50),
                                      int(block.y + block.height + 50)), background_color)
            draw = ImageDraw.Draw(image)
            draw.text((block.x, y_final), line, font=font, fill=color)
            image_array = np.array(image)

            lower = np.array([0, 0, 0])
            higher = np.array([150, 150, 150])

            mask = cv2.inRange(image_array, lower, higher)
            cv2.imwrite("temporary_image.jpg", mask)

            if color[0] <= higher[0] and color[1] <= higher[1] and color[2] <= higher[2]:
                target_color = (255, 255, 255)
            else:
                target_color = (0, 0, 0)

            image = cv2.imread("temporary_image.jpg")
            matching_pixels = np.argwhere(np.all(image == target_color, axis=-1))

            if len(matching_pixels) > 0:

                min_coordinates = np.min(matching_pixels, axis=0)
                max_coordinates = np.max(matching_pixels, axis=0)
                x1, y1 = int(min_coordinates[1]), int(min_coordinates[0])
                x2, y2 = int(max_coordinates[1]), int(max_coordinates[0])
                b_box = br.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)

                tf.append_to_json(JSON_FILE, b_box)
            else:
                print("Bounding box not found in the image.")


def insert_image(brochure, path, block):
    """
        This inserts image that has given size at a given position
    """
    insert = Image.open(path)
    insert = insert.resize((block.width, block.height), Image.Resampling.LANCZOS)
    brochure.image.paste(insert, (block.x, block.y))


def generate_block_params(brochure):
    """
        This function generates margins for blocks of the brochure
    """
    remaining_height = brochure.height - 2 * brochure.top_margin - brochure.header_height
    remaining_width = brochure.width - 2 * brochure.left_margin
    dist_ver = int(remaining_height * random.uniform(0.04, 0.05))
    dist_hor = int(remaining_width * random.uniform(0.04, 0.05))
    width = (brochure.width - 2 * brochure.left_margin - (brochure.columns - 1)
             * dist_hor) // brochure.columns
    height = (remaining_height - brochure.rows * dist_ver) // brochure.rows

    block = br.BrochureBlock(width=width, height=height, ver_dist=dist_ver, hor_dist=dist_hor)
    return block


def generate_header_params(brochure, width_range, w_height_range, h_height_range, centring_range):
    """
        This function generates size parameters for headers
    """
    w = brochure.width - 2 * brochure.left_margin
    h = brochure.height - 2 * brochure.top_margin
    block = br.BrochureBlock(width=w, height=h, x=brochure.left_margin, y=brochure.top_margin)

    return generate_header_params_for_block(block, width_range, w_height_range,
                                            h_height_range, centring_range)


def generate_header_params_for_block(block, width_range, w_height_range,
                                     h_height_range, centring_range):
    """
        This function generates size parameters for headers
    """
    header_height_ratio = random.uniform(w_height_range[0], w_height_range[1])\
        if block.width > block.height else random.uniform(h_height_range[0], h_height_range[1])
    header_height = int(block.height * header_height_ratio)
    header_width = int(block.width * random.uniform(width_range[0], width_range[1]))
    centre = (block.width - header_width) * random.uniform(centring_range[0], centring_range[1])
    header_block = br.BrochureBlock(width=header_width, height=header_height,
                                    x=block.x + centre, y=block.y)

    return header_block
