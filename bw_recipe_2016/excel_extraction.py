# -*- coding: utf-8 -*-
import bw2io

if bw2io.__version__ >= (0, 8):
    from bw2io.extractors import ExcelExtractor
else:
    from bw2io.extractors import ExcelExtractor as Original

    def get_cell_value_handle_error(cell):
        if cell.ctype == 5:
            # Error type
            return None
        else:
            return cell.value

    class ExcelExtractor(Original):
        @classmethod
        def extract_sheet(cls, wb, name, strip=True):
            ws = wb.sheet_by_name(name)
            _ = lambda x: x.strip() if (strip and hasattr(x, "strip")) else x
            return [
                [
                    _(get_cell_value_handle_error(ws.cell(row, col)))
                    for col in range(ws.ncols)
                ]
                for row in range(ws.nrows)
            ]
