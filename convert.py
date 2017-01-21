import xlsx2csv
import csv
import json
import xlrd
import xlwt
import os.path

def getColNames(sheet):
	rowSize = sheet.row_len(0)
	colValues = sheet.row_values(0, 0, rowSize )
	columnNames = []

	for value in colValues:
		columnNames.append(value)

	return columnNames

def getRowData(row, columnNames):
	rowData = {}
	counter = 0

	for cell in row:
		rowData[columnNames[counter]] = cell.value
		counter +=1

	return rowData

def getSheetData(sheet, columnNames):
	nRows = sheet.nrows
	sheetData = []
	counter = 1

	for idx in range(1, nRows):
		row = sheet.row(idx)
		rowData = getRowData(row, columnNames)
		sheetData.append(rowData)

	return sheetData

def getWorkBookData(workbook):
	nsheets = workbook.nsheets
	counter = 0
	workbookdata = {}

	for idx in range(0, nsheets):
		worksheet = workbook.sheet_by_index(idx)
		columnNames = getColNames(worksheet)
		sheetdata = getSheetData(worksheet, columnNames)
		workbookdata[worksheet.name] = sheetdata

	return workbookdata

def xlsx2JSON(filename):
        workbook = xlrd.open_workbook(filename)
        workbookdata = getWorkBookData(workbook)
        return json.dumps(workbookdata, sort_keys=True, indent=4,  separators=(',', ": "))

def csv2JSON(filename):
    f = open(filename)
    reader = csv.DictReader(f)
    rows = list(reader)
    return json.dumps(rows)
