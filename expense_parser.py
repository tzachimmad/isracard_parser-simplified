# -*- coding: utf-8 -*-
from expense_class import *
import xlrd
from isracard_update import *
from os import remove
import os
sys.setdefaultencoding('utf-8')

#define vars
CATEGORIES_FN = "buisinesses.csv"
SHEET_START = 6
DOMESTIC_START = "עסקאות בארץ"
CASH_ENTRY = "משיכת מזומנים"
IGNORE_ISRACARD_ENTRY = "סך חיוב בש\"ח:"
LAST_FRGN_ISRACARD_ENTRY = "TOTAL FOR DATE"
CASH_ADVANCE_FEE = "CASH ADVANCE FEE"
#dictionaries
establishment_dic_array = [{},{},{},{},{},{},{},{},{},{},{},{}]
categories_dic = {}

def set_crawler_params(first_sheet,row):
    if (row==SHEET_START):
        if first_sheet.cell(4,0).value==DOMESTIC_START:
            return 6,0,1,2
        else:
            return 7,0,2,5
    return row,0,2,5

def set_name (input_name):
    key = input_name
    key = key.replace(",","")
    key = key.replace("\'","")
    key = key.replace("\"","")
    return key

def print_to_csv(output_file,estab,new_line):
    output_file.write(str(estab.get_year()))
    output_file.write(",")
    output_file.write(str(estab.get_month()))
    output_file.write(",")
    output_file.write(estab.get_category())
    output_file.write(",")
    output_file.write(estab.get_name())
    output_file.write(",")
    output_file.write(str(estab.get_amount()))
    if new_line:
        output_file.write("\n")

##parse categories csv
def parse_categories():
    f = open(CATEGORIES_FN, 'rb')
    reader = csv.reader(f)
    for row in reader:
        category = row[0]
        for i in range(1,len(row)):
            categories_dic[str(row[i])] = category
            print row[i]
    f.close()

#Create Expense and Relative Establishment and put in appropriate set
def add_expense(date_made, estab_name, amount):
    month = int(date_made[date_made.find('/')+1:date_made.find('/')+3])
    establishment_dic = establishment_dic_array[month-1]
    if estab_name in establishment_dic:
        estab = establishment_dic[estab_name]
    else:
        estab = Establishment(estab_name)
        establishment_dic[estab_name] =  estab
    expense_input = Expense(date_made, estab, amount)
    estab.add_expense(expense_input)
    estab.set_category(categories_dic.get(str(estab_name),"unlisted_category"))


#parse isracard xls in html format
def parse_xls_html(path, row_input):
    book = xlrd.open_workbook(filename=path, encoding_override="cp1252")
    first_sheet = book.sheet_by_index(0)
    keep_parsing = True
    row,date_col,estab_col,amount_col = set_crawler_params(first_sheet,row_input)
    while keep_parsing:
        establishment = first_sheet.cell(row,estab_col).value
        if establishment==LAST_FRGN_ISRACARD_ENTRY:
            return -1
        if establishment == IGNORE_ISRACARD_ENTRY:
            row += 1
            if first_sheet.cell(row,estab_col).value == xlrd.empty_cell.value:
                keep_parsing = False
            continue
        if establishment == CASH_ADVANCE_FEE:
            amount = first_sheet.cell(row,amount_col-2).value
            date_made = first_sheet.cell(row-1,date_col).value
        else:
            amount = first_sheet.cell(row,amount_col).value
            date_made = first_sheet.cell(row,date_col).value
        add_expense(date_made, set_name(establishment), amount)
        row +=1
    try:
        if (first_sheet.cell(row+1,estab_col).value == xlrd.empty_cell.value):
            return -1
    except:
        return -1
    return row+2

def output_data():
    output_file = open("output.csv", 'w')
    output_file.write("Year,Month,Category,Establishment,Amount\n")
    for month in range(0,12):
        establishment_dic = establishment_dic_array[month]
        pairs = sorted(establishment_dic.items(), key=lambda x: x[1].get_amount())
        for tuple in reversed(pairs):
            estab = tuple[1]
            print_to_csv(output_file, estab, True)
    output_file.close()

folder_path = sys.argv[1]
if (folder_path[-1]!='/'):
    folder_path = folder_path+'/'
##print "Processing..."
parse_categories()
for fn in sorted(os.listdir(folder_path)):
     if "Export" in fn and ".xls" in fn and fn[0]!='.':
         ##print fn
         next_row = parse_xls_html(folder_path + fn,SHEET_START)
         if next_row!=-1:
             next_row = parse_xls_html(folder_path + fn,next_row)
output_data()
##print "Done!"
