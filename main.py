"""
    Main
"""
import layout_functions as lf
import text_functions as tf
import constants as c
# -*- coding: utf-8 -*-


lf.create_directory_if_not_exists(c.COMMON_DATASET_PATH + '/images')
lf.create_directory_if_not_exists(c.COMMON_DATASET_PATH + '/table_locations')
lf.create_directory_if_not_exists(c.COMMON_DATASET_PATH + '/text_blocks_locations')
lf.create_directory_if_not_exists(c.COMMON_DATASET_PATH + '/text_lines_locations')
INSTANCES = 1

for i in range(INSTANCES):

    tf.delete_file(c.generate_path('text_lines_locations/text_locations_', '.json'))
    tf.delete_file(c.generate_path('text_blocks_locations/text_blocks_', '.json'))
    tf.delete_file(c.generate_path('table_locations/tables_', '.json'))
    tf.remove_tables_from_json(c.COMMON_DATASET_PATH + 'tables.json', str(c.INDEX) + '.jpg')
    lf.generate_brochure()
    c.INDEX += 1
