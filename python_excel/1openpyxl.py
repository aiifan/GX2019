import openpyxl

wb = openpyxl.load_workbook('123.xlsx')

print(wb.active)
print(wb.read_only)
print(wb.encoding)
print(wb.worksheets)
print(wb.get_sheet_names())
# print(wb.get_sheet_by_name(u'今天'))
wb.create_named_range(index=0 title='new sheet')