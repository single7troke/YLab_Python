from typing import Generator

import openpyxl
from core.config import Config
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

config = Config()


def reader() -> Generator:
    try:
        book: Workbook = openpyxl.load_workbook(config.path_to_menu_file)
    except FileNotFoundError:
        return 'No file'

    sheet: Worksheet = book.active

    for row in sheet.iter_rows(values_only=True):
        data = [value for value in row]
        yield data
