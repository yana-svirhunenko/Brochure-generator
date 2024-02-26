"""
    This module contains different file paths
"""

INDEX = 1
COMMON_DATASET_PATH = 'dataset/'
COMMON_SAMPLES_PATH = 'samples/'
TEMPORARY_IMAGE = COMMON_SAMPLES_PATH + 'temporary_image.jpg'
TEMPORARY_TABLE = COMMON_SAMPLES_PATH + 'temporary_table.jpg'
CSV_IMAGE_TEXT = COMMON_DATASET_PATH + 'image_text.csv'

#JSON_TEXT_LINES = COMMON_DATASET_PATH + 'text_lines_locations/text_locations_' + str(INDEX) + '.json'
#JSON_TABLES = COMMON_DATASET_PATH + 'table_locations/tables_' + str(INDEX) + '.json'
#JSON_TEXT_BLOCKS = COMMON_DATASET_PATH + 'text_blocks_locations/text_blocks_' + str(INDEX) + '.json'
#RESULT_IMAGE_PATH = COMMON_DATASET_PATH + 'images/' + str(INDEX) + '.jpg'


def generate_path(folder, file_type, directory=True):

    path = folder + str(INDEX) + file_type
    if directory:
        path = COMMON_DATASET_PATH + path

    return path
