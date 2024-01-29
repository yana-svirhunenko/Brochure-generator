"""
    Main
"""
import random
import copy
import text_functions as tf
import layout_functions as lf
import brochure as brr
# -*- coding: utf-8 -*-

tf.delete_file(lf.JSON_FILE)
tf.delete_file(lf.JSON_TABLES)
tf.delete_file(lf.JSON_TEXT_BLOCKS)
text = lf.get_entire_text()
br = lf.generate_brochure_params()

if random.choice([True, False]):

    header_bl = lf.generate_header_params(br, [0.8, 1], [0.1, 0.15], [0.07, 0.1], [0.01, 1])
    color = tf.get_contrasting_color(br.image, header_bl)
    font_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_fonts', '*.ttf')
    header, main_text = tf.extract_header(text, random.randint(len(text)//200, len(text)//30))
    lf.put_text_in_block(header, br, header_bl, font_path, color, True)

    tf.prepare_data_for_json(lf.JSON_TEXT_BLOCKS, header_bl)
    header_height = header_bl.height + int(header_bl.height * random.uniform(0.3, 0.5))
    segments = tf.divide_text(main_text, br.text_parts)

else:

    segments = tf.divide_text(text, br.text_parts)
    header_height = 0

br.header_height = header_height
bl = lf.generate_block_params(br)

for row in br.layout_matrix:
    print(row)

text_pos = 0
for j in range(br.columns):
    for i in range(br.rows):

        choice = br.layout_matrix[i][j]
        bl.x = int(br.left_margin + j * (bl.width + bl.hor_dist))
        bl.y = int(br.top_margin + header_height + i * (bl.height + bl.ver_dist))
        color = tf.get_contrasting_color(br.image, bl)

        if choice == 1:

            lf.determine_type_of_image(br, bl)

        elif choice == 2:

            text = segments[text_pos]
            text_pos += 1
            font_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_fonts', '*.ttf')
            print(font_path)
            image_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_insert_images', '*.jpg')
            lf.put_text_and_image_in_block(text, br, bl, image_path, font_path, color)

        elif choice == 3:

            text = segments[text_pos] + segments[text_pos + 1]
            text_pos += 2
            header_bl = lf.generate_header_params_for_block(bl, [0.8, 1], [0.17, 0.2],
                                                            [0.1, 0.12], [0.01, 1])
            header, main_text = tf.extract_header(text,
                                                  random.randint(len(text) // 30, len(text) // 20))
            font_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_fonts', '*.ttf')
            print(font_path)
            lf.put_text_in_block(header, br, header_bl, font_path, color, True)

            tf.prepare_data_for_json(lf.JSON_TEXT_BLOCKS, header_bl)

            block_header_height = header_bl.height + int(header_bl.height * random.uniform(0.3, 0.5))
            font_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_fonts', '*.ttf')
            print(font_path)
            text_bl = copy.deepcopy(bl)
            text_bl.y += block_header_height
            text_bl.height -= block_header_height
            lf.put_text_in_block(main_text, br, text_bl, font_path, color, True)

            tf.prepare_data_for_json(lf.JSON_TEXT_BLOCKS, text_bl)

        elif choice == 4:

            text = segments[text_pos] + segments[text_pos + 1]
            text_pos += 2
            font_path = tf.get_random_file_path(lf.COMMON_PATH + 'sample_fonts', '*.ttf')
            print(font_path)
            lf.put_text_in_block(text, br, bl, font_path, color, True)

            tf.prepare_data_for_json(lf.JSON_TEXT_BLOCKS, bl)


RESULT_PATH = lf.COMMON_PATH + 'result/' + str(lf.INDEX) + '.jpg'
br.image.save(RESULT_PATH)
tf.delete_file('temporary_image.jpg')
tf.delete_file('table_image.jpg')
