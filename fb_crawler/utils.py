import os
from fb_crawler.setting import OUTPUTS_DIR


class Utils:
    def __init__(self):
        pass

    def create_dirs(self):
        os.makedirs(OUTPUTS_DIR, exist_ok=True)

    def get_output_filepath(self, name):
        filename = name + ".xlsx"
        return os.path.join(OUTPUTS_DIR, filename)
