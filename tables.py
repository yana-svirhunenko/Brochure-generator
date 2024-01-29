"""
    This module is used to generate tables for brochures
"""
import copy
import random
from itertools import cycle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import text_functions as tf
import layout_functions as lf
import brochure as br
# -*- coding: utf-8 -*-

cycol = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
#words = ['Крінж', 'Крінж', 'Крінж', 'Крінж', 'Крінж', 'Крінж', 'Крінж', 'Крінж', 'Крінж']
words = [
    "привіт",
    "кава",
    "книга",
    "сонце",
    "мова",
    "день",
    "ночі",
    "річка",
    "дерево",
    "пташка"
]

class Table:
    """
        This class is used to represent table structure
    """
    def __init__(self, rows, columns, width, height, cell_width, cell_height,
                 cell_left_margin, cell_top_margin, draw, image):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_left_margin = cell_left_margin
        self.cell_top_margin = cell_top_margin
        self.draw = draw
        self.image = image


def draw_table_borders(table):
    """
        This function is used to draw a table layout
    """
    row_lines = random.choice([True, False])
    col_lines = random.choice([True, False])
    borders = random.choice([True, False])
    inner_borders = random.choice([True, False])

    if row_lines:
        for i in range(table.rows - 1):
            draw_line(table.draw, (0, (i + 1) * table.cell_height),
                      (table.width, (i + 1) * table.cell_height))

    if col_lines:
        for j in range(table.columns - 1):
            draw_line(table.draw, ((j + 1) * table.cell_width, 0),
                      ((j + 1) * table.cell_width, table.height))

    if borders:
        draw_rectangle(table.draw, (0, 0), (table.width, table.height), 2)

    if inner_borders:
        draw_line(table.draw, (0, table.cell_height), (table.width, table.cell_height), 2)
        draw_line(table.draw, (table.cell_width, 0), (table.cell_width, table.height), 2)


def draw_line(draw, start, end, line_width=1):
    """
        This function is used to draw a line to create layout for the table
    """
    shape = [start, end]
    draw.line(shape, fill=(0, 0, 0), width=line_width)


def draw_rectangle(draw, start, end, outline_width=1):
    """
        This function is used to draw a rectangle to create layout for the table
    """
    shape = [start, end]
    draw.rectangle(shape, outline=(0, 0, 0), width=outline_width)


def generate_and_scale_table_content(table, font_path):

    matrix_content = [[0 for _ in range(table.columns)] for _ in range(table.rows)]
    min_font = 10000
    text_width = table.cell_width - 2 * table.cell_left_margin
    text_height = table.cell_height - 2 * table.cell_top_margin

    for j in range(table.columns):
        numbers = random.choice([True, False])
        digits = random.randint(0, 3)
        for i in range(table.rows):
            if numbers and j and i:
                matrix_content[i][j] = str(round(random.uniform(-100, 100), digits))
            else:
                matrix_content[i][j] = random.choice(words)

            font_size, r = tf.scale_font(matrix_content[i][j], font_path, text_width, text_height, 1)
            if font_size < min_font:
                min_font = font_size

    return matrix_content, min_font


def generate_table_params(width, height):
    """
        This function is used to generate instance of table class that
        represents table
    """
    columns = random.randint(width // 100, width // 60)
    rows = random.randint(height // 30, height // 25)
    columns = max(columns, 2)
    rows = max(rows, 2)

    cell_width = width // columns
    cell_height = height // rows
    left_margin = int(cell_width * 0.1)
    top_margin = int(cell_height * 0.1)

    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    table = Table(rows=rows, columns=columns, width=width, height=height,
                  cell_width=cell_width, cell_height=cell_height,
                  cell_left_margin=left_margin, cell_top_margin=top_margin,
                  draw=draw, image=image)
    return table


def get_irregular_horizontal_layout(remaining_space, horizontal_widths):

    i = 0
    while remaining_space > 0:

        if i == 0 and horizontal_widths[i] == 1:
            horizontal_widths[i] += 1
            remaining_space -= 1

        if random.choice([True, False]):
            horizontal_widths[i] += 1
            remaining_space -= 1
        i += 1

        if i == len(horizontal_widths):
            i = 0

    return horizontal_widths


def generate_cell_content():

    if random.choice([True, False]):
        digits = random.randint(0, 5)
        return str(round(random.uniform(-100, 100), digits))

    else:
        return random.choice(words)


def draw_irregular_layout(table, horizontal_widths, index, vertical_widths):

    left_margin = 0
    for i in range(0, index):
        left_margin += vertical_widths[i]
    left_margin *= table.cell_width

    if horizontal_widths == 0:
        draw_line(table.draw, (left_margin, 0), (left_margin, table.height), 2)
        return

    column_width = vertical_widths[index] * table.cell_width
    for i in range(len(horizontal_widths)):

        draw_line(table.draw, (left_margin, 0), (left_margin, table.height), 2)
        top_margin = 0

        for j in range(len(horizontal_widths) - 1):
            top_margin += horizontal_widths[j] * table.cell_height
            draw_line(table.draw, (left_margin, top_margin), (column_width + left_margin, top_margin))


def decide_on_vertical_layout(column_types, avoid, use):

    for i in range(0, len(column_types)):
        if column_types[i] == avoid:
            continue
        if random.choice([True, False]):
            column_types[i] = use


def generate_irregular_table(table):

    max_v = max(2, table.columns)
    vertical_blocks = random.randint(max(2, table.columns // 2), max_v)
    vertical_widths = [1 for _ in range(vertical_blocks)]
    remaining_columns = table.columns - vertical_blocks

    horizontal_layout_types = random.randint(3, 5)
    column_layout_types = [0] * vertical_blocks

    i = 0
    while remaining_columns > 0:
        if random.choice([True, False]):
            vertical_widths[i] += 1
            remaining_columns -= 1
        i += 1
        if i == len(vertical_widths):
            i = 0

    layouts = [0]
    for i in range(0, horizontal_layout_types):
        max_h = max(2, table.rows)
        horizontal_blocks = random.randint(max(2, table.columns // 2), max_h)
        horizontal_widths = [1 for _ in range(horizontal_blocks)]
        remaining_rows = table.rows - horizontal_blocks
        hw = get_irregular_horizontal_layout(copy.deepcopy(remaining_rows), copy.deepcopy(horizontal_widths))
        layouts.append(hw)

    possibility_of_zero = 0.1
    other_pos = (1 - possibility_of_zero) / (horizontal_layout_types - 1)
    p = [possibility_of_zero] + [other_pos] * (horizontal_layout_types - 1)

    for i in range(0, len(column_layout_types)):

        layout = np.random.choice(np.arange(0, horizontal_layout_types), p=p)
        column_layout_types[i] = layout
        draw_irregular_layout(table, layouts[layout], i, vertical_widths)

    font_path = 'sample_fonts/Arial.ttf'
    current_width = 0
    print(column_layout_types)

    for i in range(len(column_layout_types)):

        if column_layout_types[i] != 0:
            horizontal_widths = layouts[column_layout_types[i]]
        else:
            text = generate_cell_content()
            block = br.BrochureBlock(width=vertical_widths[i] * table.cell_width,
                                     height=table.height, x=current_width, y=0)
            scale_and_write_vertical_text(table, text, font_path, block, (0, 0, 0), (255, 255, 255))
            current_width += vertical_widths[i] * table.cell_width
            continue

        divide_flag, divide_pos = get_divide_pos(vertical_widths[i], horizontal_widths)
        top_margin = 0

        for j in range(0, divide_pos):

            text = generate_cell_content()
            block_width = vertical_widths[i] * table.cell_width
            block_height = horizontal_widths[j] * table.cell_height
            text_block = br.BrochureBlock(width=block_width, height=block_height, x=current_width, y=top_margin)
            if block_width > block_height:
                scale_and_write_horizontal_text(table, text, font_path, text_block, (0, 0, 0))
            else:
                scale_and_write_vertical_text(table, text, font_path, text_block,
                                              (0, 0, 0), (255, 255, 255))
            top_margin += horizontal_widths[j] * table.cell_height

        if divide_flag:

            first_width = random.randint(1, vertical_widths[i] - 1)
            block1_width = first_width * table.cell_width
            block2_width = (vertical_widths[i] - first_width) * table.cell_width
            draw_line(table.draw, (current_width + block1_width, top_margin), (current_width + block1_width, table.height))

            for k in range(divide_pos, len(horizontal_widths)):

                block_height = horizontal_widths[k] * table.cell_height
                block_1 = br.BrochureBlock(width=block1_width, height=block_height, x=current_width, y=top_margin)
                block_2 = br.BrochureBlock(width=block2_width, height=block_height,
                                           x=current_width + block1_width, y=top_margin)
                text_1 = generate_cell_content()
                text_2 = generate_cell_content()

                if block1_width > block_height:
                    scale_and_write_horizontal_text(table, text_1, font_path, block_1, (0, 0, 0))
                else:
                    scale_and_write_vertical_text(table, text_1, font_path, block_1, (0, 0, 0), (255, 255, 255))

                if block2_width > block_height:
                    scale_and_write_horizontal_text(table, text_2, font_path, block_2, (0, 0, 0))
                else:
                    scale_and_write_vertical_text(table, text_2, font_path, block_2, (0, 0, 0), (255, 255, 255))

                top_margin += horizontal_widths[k] * table.cell_height

        current_width += vertical_widths[i] * table.cell_width

    draw_rectangle(table.draw, (0, 0), (table.width, table.height), 2)
    result_path = 'table_image.jpg'
    table.image.save(result_path)


def get_divide_pos(vertical_width, horizontal_widths):

    if vertical_width < 2:
        divide_flag = False
        divide_pos = len(horizontal_widths)
    else:
        divide_flag = random.choice([True, False])
        if divide_flag:
            upper_limit = len(horizontal_widths) - 2 if len(horizontal_widths) - 2 > 1 else len(horizontal_widths)
            start_at = random.randint(1, upper_limit)
            divide_pos = len(horizontal_widths) - start_at
        else:
            divide_pos = len(horizontal_widths)

    return divide_flag, divide_pos


def get_text_width_and_height(text, font_path, font_size):

    font = ImageFont.truetype(font_path, font_size)
    text_bbox = font.getbbox(text)
    return text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]


def scale_and_write_vertical_text(table, text, font_path, block, color, background_color):

    margin = 4
    width = block.width - margin
    height = block.height - margin
    max_text_width = int((height - margin) * 0.8)
    max_text_height = int((width - margin) * 0.5)
    font_size, r = tf.scale_font(text, font_path, max_text_width, max_text_height, 1)

    text_width, text_height = get_text_width_and_height(text, font_path, font_size)

    initial_cell = Image.new("RGB", (height, width), background_color)
    draw = ImageDraw.Draw(initial_cell)
    background = br.Brochure(image=initial_cell, draw=draw)

    x = int((height - text_width + margin) // 2)
    height_coefficient = 0.3 * block.width/block.height
    y = int(height_coefficient * width)
    bl = br.BrochureBlock(width=text_width, height=text_height, x=x, y=y)

    lf.put_text_in_block(text, background, bl, font_path, color, False, 1, font_size)
    rotated_cell = initial_cell.rotate(90, expand=True)
    paste_position = (block.x + margin//2, block.y + margin//2)
    table.image.paste(rotated_cell, paste_position)


def scale_and_write_horizontal_text(table, text, font_path, block, color):

    max_text_width = int(block.width * 0.8)
    max_text_height = int(block.height * 0.5)
    font_size, r = tf.scale_font(text, font_path, max_text_width, max_text_height, 1)

    text_width, text_height = get_text_width_and_height(text, font_path, font_size)

    height_coefficient = 0.3 * block.height / block.width
    x = int(block.x + (block.width - text_width) // 2)
    y = int(block.y + (height_coefficient * block.height))
    bl = br.BrochureBlock(width=text_width, height=text_height, x=x, y=y)

    lf.put_text_in_block(text, table, bl, font_path, color, False, 1, font_size)


def generate_table(width, height):
    """
        This function is used to generate table for brochure
        based on it`s future width and height
    """

    table = generate_table_params(width, height)
    font_path = 'sample_fonts/Arial.ttf'
    content_matrix, font_size = generate_and_scale_table_content(table, font_path)

    if np.random.choice([True, False], p=[0.7, 0.3]):
        generate_irregular_table(table)
    else:
        draw_table_borders(table)
        for j in range(table.columns):
            for i in range(table.rows):

                x = int(table.cell_left_margin + j * table.cell_width)
                y = int(table.cell_top_margin + i * table.cell_height)
                bl = br.BrochureBlock(width=table.cell_width - 2 * table.cell_left_margin,
                                  height=table.cell_height - 2 * table.cell_top_margin,
                                  x=x, y=y)

                lf.put_text_in_block(content_matrix[i][j], table, bl, font_path, (0, 0, 0), False, 1, font_size)

    result_path = 'temporary_image.jpg'
    table.image.save(result_path)
    return result_path


