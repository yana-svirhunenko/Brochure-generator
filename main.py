from shutil import get_archive_formats
import random
import os
import glob
import cv2
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from enum import Enum
import functions
# -*- coding: utf-8 -*-


class BlockType(Enum):
    image = 1
    text_and_image = 2
    text_and_header = 3
    text = 4


def put_text_and_image_in_block(text, image, insert_image_path, x, y,
                                block_height, block_width, font, color, draw):

    if block_height > block_width:

        down = random.choice([True, False])
        image_height = int(block_height * random.uniform(0.3, 0.5))
        image_margin = int(block_height * random.uniform(0.05, 0.1))

        if down:

            functions.insert_image(image, insert_image_path, x, y + block_height - image_height, block_width, image_height)
            functions.put_text_in_block(text, x, y, block_width,
                          block_height - image_height - image_margin, font, color, draw)

        else:

            functions.insert_image(image, insert_image_path, x, y, block_width, image_height)
            functions.put_text_in_block(text, x, y + image_height + image_margin, block_width,
                          block_height - image_height - image_margin, font, color, draw)

    else:

        left = random.choice([True, False])
        image_width = int(block_width * random.uniform(0.3, 0.5))
        image_margin = int(block_width * random.uniform(0.05, 0.1))

        if left:

            functions.insert_image(image, insert_image_path, x, y, image_width, block_height)
            functions.put_text_in_block(text, x + image_width + image_margin, y,
                          block_width - image_width - image_margin, block_height, font, color, draw)

        else:

            functions.insert_image(image, insert_image_path, x + block_width - image_width, y, image_width, block_height)
            functions.put_text_in_block(text, x, y, block_width - image_width - image_margin,
                          block_height, font, color, draw)



def divide_image(entire_text, index):

  path = functions.get_random_file_path('sample_images', '*.jpg')
  image = Image.open(path)
  draw = ImageDraw.Draw(image)

  width, height = image.size
  left_margin = random.randint(10, width//20)
  top_margin = random.randint(10, height//10)


  if width > height:

    columns = random.randint(1, 5)
    rows = random.randint(1, 3)
    h = int((height - 2*top_margin) * random.uniform(0.1, 0.15))

  else:

    columns = random.randint(1, 3)
    rows = random.randint(1, 4)
    h = int((height - 2*top_margin) * random.uniform(0.07, 0.1))


  matrix, text_parts = functions.decide_on_part(columns, rows)
  header_height = 0
  text_pos = 0
  header_flag = random.choice([True, False])

  if header_flag:

    min_length = random.randint(len(entire_text)//200, len(entire_text)//20)
    header, main_text = functions.extract_header(entire_text, min_length)

    header_width = int((width - 2*left_margin) * random.uniform(0.8, 1))
    centre = left_margin + (width - left_margin - header_width) * random.uniform(0.01, 1)

    color = functions.get_contrasting_color(image, centre, top_margin, header_width, h)
    font_path = functions.get_random_file_path('sample_fonts', '*.ttf')

    functions.put_text_in_block(header, centre, top_margin, header_width, h,
                      font_path, color, draw)

    header_height = h + (int)(height * random.uniform(0.03, 0.05))
    segments = functions.divide_text(main_text, text_parts)

  else:
    segments = functions.divide_text(entire_text, text_parts)


  dist_between_blocks_ver =  int((height - 2*top_margin - header_height) * random.uniform(0.02, 0.05))
  dist_between_blocks_hor =  int((width - 2*left_margin) * random.uniform(0.02, 0.05))

  block_width = int((width - 2*left_margin - (columns - 1) * dist_between_blocks_hor)/columns)
  block_height = int((height - 2*top_margin - header_height - rows * dist_between_blocks_ver)/rows)

  for row in matrix:
    print(row)

  for j in range(columns):
    for i in range(rows):

        choice = matrix[i][j]
        x = int(left_margin + j * (block_width + dist_between_blocks_hor))
        y = int(top_margin + header_height + i * (block_height + dist_between_blocks_ver))
        color = functions.get_contrasting_color(image, x, y, block_width, block_height)

        if choice == 1:

          path =  functions.get_random_file_path('sample_insert_images', '*.jpg')
          functions.insert_image(image, path, x, y, block_width, block_height)

        elif choice == 2:

          text = segments[text_pos]
          text_pos += 1
          font_path = functions.get_random_file_path('sample_fonts', '*.ttf')
          image_path =  functions.get_random_file_path('sample_insert_images', '*.jpg')

          put_text_and_image_in_block(text, image,
                            image_path, x, y, block_height, block_width, font_path, color, draw)

        elif choice == 3:

          if block_width > block_height:
            h = int(block_height * random.uniform(0.15, 0.2))
          else:
            h = int(block_height * random.uniform(0.1, 0.12))

          text = segments[text_pos] + segments[text_pos + 1]
          text_pos += 2
          min_header_length = random.randint(len(text)//30, len(text)//15)

          header, main_text = functions.extract_header(text, min_header_length)
          header_font_path = functions.get_random_file_path('sample_fonts', '*.ttf')

          functions.put_text_in_block(header, x, y, block_width, h, header_font_path, color, draw)
          block_header_height = h + (int)(block_height * random.uniform(0.05, 0.07))

          text_font_path = functions.get_random_file_path('sample_fonts', '*.ttf')
          functions.put_text_in_block(main_text, x, y + block_header_height, block_width,
                            block_height - block_header_height, text_font_path, color, draw)

        elif choice == 4:

          text = segments[text_pos] + segments[text_pos + 1]
          text_pos += 2

          font_path = functions.get_random_file_path('sample_fonts', '*.ttf')
          functions.put_text_in_block(text, x, y, block_width, block_height, font_path,
                        color, draw)


  result_path = 'result/' + str(index) + '.jpg'
  image.save(result_path)


dataset_path = 'sample_text'
text_files = glob.glob(os.path.join(dataset_path, '*.txt'))

index = 1
for file in text_files:

  with open(file, 'r', encoding='utf-8') as f:
      entire_text = f.read()
  divide_image(entire_text, index)

  index+=1

