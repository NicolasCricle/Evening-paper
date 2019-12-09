import time
from datetime import datetime

import xlwings
from openpyxl.utils import get_column_letter
from PIL import ImageGrab, Image, ImageChops

from myrequest import MyRequest


class ExcelWorker(object):
    BASE_PATH           = r"C:/Users/livis/Desktop/pic/demo.xlsx"
    PIC_DIR             = "C:/Users/livis/Desktop/pic/"
    SHEET_NAME          = "CC每日进账明细"
    START_ROW           = 6
    START_COLUMN        = "C"
    INCRE_COLUMN        = 5
    MAX_ROW             = 40

    def __init__(self, path=None):
        if path is None:
            path = ExcelWorker.BASE_PATH
        
        self._app = xlwings.App(visible=True, add_book=False)
        self._excel = self._app.books.open(self.BASE_PATH) 
        self._sheet = self._excel.sheets[ExcelWorker.SHEET_NAME]

    @property
    def current_sheet(self):
        return self._sheet

    @current_sheet.setter
    def current_sheet(self, sheetName):
        self._sheet = self._excel.sheets[sheetName]

    @property
    def excel(self):
        return self._excel

    @property
    def app(self):
        return self._app    
    
    @staticmethod
    def _get_column(column):
        return get_column_letter(column)

    @staticmethod
    def _get_start_row():
        return ExcelWorker.START_ROW

    @staticmethod
    def _get_start_column():
        return ExcelWorker.START_COLUMN
    
    @staticmethod
    def _get_cell_name(row, column):
        return f"{column}{row}"

    @property
    def today(self):
        return datetime.now().day + self.INCRE_COLUMN

    @staticmethod
    def write_cell(cell, value):
        if not value:
            return 
        elif value == "p":
            cell.value = None
        else:
            cell.value = int(value)

    @staticmethod
    def get_pic(sheet, index, path, nRow=None, nColumn=None):
        if nRow is None:
            nRow = sheet.api.UsedRange.Rows.count
        if nColumn is None:
            nColumn = sheet.api.UsedRange.Columns.count
        
        if nRow > ExcelWorker.MAX_ROW:
            nRow = ExcelWorker.MAX_ROW

        sheet.range((1, 1), (nRow, nColumn)).api.CopyPicture()
        sheet.api.Paste()


        curPic = sheet.pictures[0]
        curPic.api.Copy()

        img = ImageGrab.grabclipboard()
        img = ExcelWorker.trim(img)                        

        img.save(f"{path}{index}.jpg")
        curPic.delete()

    @staticmethod
    def trim(im):
        """去除图片四周空白"""
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def get_cell(self, row, column, cellName=None):
        if cellName:
            return self._sheet.range(cellName)
        cellName = self._get_cell_name(row, column)
        return self._sheet.range(cellName)

    def save(self):
        self.excel.save()
        self.excel.close()
        self.app.quit()

    def get_used_range(self):
        for index, sheet in enumerate(self.excel.sheets):
            if sheet.name == self.SHEET_NAME:
                continue
            self.get_pic(sheet, index, self.PIC_DIR)

    @staticmethod
    def _get_sales_num():
        return MyRequest().get_sales_num()

    def run(self):
        """
        执行函数
        """
        row = self._get_start_row()
        column = self._get_start_column()

        salesList = self._get_sales_num()

        while True:
            readCell = self.get_cell(row, column)

            if not readCell.value:
                return

            for item in salesList:
                if readCell.value == item.get("saler"):
                    salesNum = item.get("salesNum")
                    writeCell = self.get_cell(row, self._get_column(self.today))
                    self.write_cell(writeCell, salesNum)

            else:
                break

            row += 1
        
        self.get_used_range()
        self.save()


if __name__ == "__main__":
    ExcelWorker().run()
