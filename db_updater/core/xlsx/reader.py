from typing import Generator

import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def reader() -> Generator:
    try:
        book: Workbook = openpyxl.load_workbook('/admin/Menu.xlsx')
    except FileNotFoundError:
        return 'No file'

    sheet: Worksheet = book.active

    for row in sheet.iter_rows(values_only=True):
        data = [value for value in row]
        yield data
