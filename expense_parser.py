# -*- coding: utf-8 -*-
import argparse
from expense_class import *
import xlrd
from bs4 import BeautifulSoup, SoupStrainer
from os import remove
import os
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf-8')

#define vars
CATEGORIES_FN = "buisinesses.csv"
SHEET_START = 6
DOMESTIC_START = "עסקאות בארץ"
CASH_ENTRY = "משיכת מזומנים"
IGNORE_ISRACARD_ENTRY = "סך חיוב בש\"ח:"
LAST_FRGN_ISRACARD_ENTRY = "TOTAL FOR DATE"
CASH_ADVANCE_FEE = "CASH ADVANCE FEE"
AGUD_CARD = "פירוט חיובים"
ACNT_NUM = "157-13"
RELEVENT_EXPENSE = "חיוב הבא"
ISRCRD = '9130'
MYCARD = '0532'
LEUMI = "933-122"
MARIA_CRD = '0540'
BANK_AGUD = "AGUD"
BANK_LEUMI = "BANK LEUMI"

def program_parameters():
	parser = argparse.ArgumentParser()
	parser.add_argument("isracard_csv_directory", help="folder with downloaded isracard csv files")
	return parser

def set_crawler_params(first_sheet,row):
	if (row==SHEET_START):
		if first_sheet.cell(4,0).value==DOMESTIC_START:
			return 6,0,1,2
		else:
			return 6,0,2,5
	return row,0,2,5

def bank_set_estab(estab, asmacta):
	if "זיכוי" in estab or "העברה" in estab:
		return "Interbank Transaction " + asmacta
	if "כספומט" in estab:
		return "ATM " + asmacta
	if "שיק" in estab:
		return "Check " + asmacta
	return "Unknown " + asmacta

def set_name(input_name, date):
	key = input_name.decode('utf-8')
	key = key.replace(",","")
	key = key.replace("\'","")
	key = key.replace("\"","")
	if not date:
		key = key.replace("/","")
	key = key.replace(">","")
	key = key.replace("<","")
	key = key.replace("\t","")
	key = key.replace("\n","")
	return key

def print_to_csv(output_file,expense):
	output_file.write(str(expense.get_year()))
	output_file.write(",")
	output_file.write(str(expense.get_month()))
	output_file.write(",")
	output_file.write(expense.get_category())
	output_file.write(",")
	output_file.write(expense.get_establishment())
	output_file.write(",")
	out_amnt = out_effective = float(expense.get_amount())
	in_amnt = in_effective = 0
	if out_amnt<0:
		in_amnt =  in_effective = -1*out_amnt
		out_amnt = out_effective = 0
	output_file.write(str(out_amnt))
	output_file.write(",")
	if ISRCRD != expense.get_card() and BANK_LEUMI != expense.get_card():
		in_effective = in_effective/2
		out_effective = out_effective/2
	output_file.write(str(out_effective))
	output_file.write(",")
	output_file.write(str(in_amnt))
	output_file.write(",")
	output_file.write(str(in_effective))
	output_file.write(",")
	person = "Tzachi"
	if MARIA_CRD == expense.get_card():
		person = "Maria"
	if BANK_AGUD == expense.get_card():
		person = "Bank Agud"
	output_file.write(person)
	output_file.write("\n")

##parse categories csv
def parse_categories(categories_dic):
	f = open(CATEGORIES_FN, 'rb')
	reader = csv.reader(f)
	for row in reader:
		category = row[0]
		for i in range(1,len(row)):
			categories_dic[str(row[i])] = category
	f.close()

#Create Expense and Relative Establishment and put in appropriate set
def add_expense(date_made, estab_name, amount,expense_array,categories_dic, card):
	cat = "unlisted_category"
	if card == BANK_AGUD or card== BANK_LEUMI:
		cat = card
	expense_input = Expense(date_made, estab_name, amount, categories_dic.get(str(estab_name),cat), card)
	expense_array.append(expense_input)

#parse isracard xls in html format
def parse_isrcrd_xls(path, row_input,expense_array,categories_dic):
	if row_input== SHEET_START:
		print path
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
		add_expense(date_made, set_name(establishment, False), amount,expense_array,categories_dic, ISRCRD)
		row +=1
	try:
		if (first_sheet.cell(row+1,estab_col).value == xlrd.empty_cell.value):
			return -1
	except:
		return -1
	return row+2

#parse visa cal xls in html format
def parse_cal_xls_html(path, expense_array, categories_dic):
	print path
	htmlfile = open(path)
	xls_soup = BeautifulSoup(htmlfile,"html.parser")
	counter = 0
	for item in xls_soup.findAll("tr"):
		if ACNT_NUM in str(item):
			counter += 1
			if counter == 2:
				blocks = str(item).split('style="white-space:nowrap;"><span><span class="no-wrap">')
				for i in range(0,len(blocks)):
					if RELEVENT_EXPENSE in blocks[i]:
							date_made = blocks[i+1][:blocks[i+1].find('<')]
							establishment = blocks[i+2][:blocks[i+2].find('<')]
							card = MYCARD
							if MARIA_CRD in blocks[i+3][blocks[i+3].find('<')-4:blocks[i+3].find('<')]:
								card = MARIA_CRD
							amount = blocks[i+4][:blocks[i+4].find('<')]
							add_expense(date_made, set_name(establishment, False), amount,expense_array,categories_dic, card)
	htmlfile.close()
	return -1

#parse bank agud xls in html format
def parse_bank_xls_html(path, expense_array, categories_dic):
	print path
	htmlfile = open(path)
	xls_soup = BeautifulSoup(htmlfile,"html.parser")
	counter = 0
	arr = []
	bnk = BANK_AGUD
	for blob in xls_soup.findAll("tr"):
		blob2 = str(blob).split("tr class=")
		for item in blob2:
			if "חשבון" in item and LEUMI in item:
				bnk = BANK_LEUMI
			if "printItem ExtendedActivity_ForPrint" in item:
				line = item.split("td><td")
				date = set_name(line[0][line[0].rfind('>'):], True)
				strt = 0
				end = 8
				if not date[0].isdigit():
					strt = 1 
					end = 9
				date = date[strt:end]
				if "</a>" in line[1]:
						line[1] = line[1][:line[1].find("</a")]
				estab = set_name(line[1][line[1].rfind('>'):],False).decode('utf-8')[1:9]
				amount = set_name(line[3][line[3].rfind('>'):], False)
				if len(amount)<=2:
					amount = set_name(line[4][line[4].rfind('>'):], False)
					amnt = -1*float(amount)
				else:
					amnt = float(amount)
				if line[2][line[2].rfind('>'):]+date not in arr:
					arr.append(line[2][line[2].rfind('>'):]+date)
				else:
					continue
				if "ויזה" in line[1][line[1].rfind('>'):] or "ישראכרט" in line[1][line[1].rfind('>'):]:
					continue
				add_expense(date, estab, amnt,expense_array,categories_dic, bnk)
	htmlfile.close()
	return -1

def main():
	parser = program_parameters()
	params, unknown = parser.parse_known_args()
	folder_path = params.isracard_csv_directory+'/'
	categories_dic = {}
	print "Processing..."
	output_file = open("output.csv", 'w')
	output_file.write("Year,Month,Category,Establishment,Out Amount, Out Effective Amount,\
	 In Amount, In Effective Amount, Person\n")
	parse_categories(categories_dic)
	for fn in sorted(os.listdir(folder_path)):
		expense_array = []
		if ".xls" in fn and fn[0]!='.':
			if "פירוט" in fn:
				parse_cal_xls_html(folder_path + fn, expense_array, categories_dic)
			elif "בחשבון" in fn:
				parse_bank_xls_html(folder_path + fn, expense_array, categories_dic)
			elif "Export" in fn:
				next_row = parse_isrcrd_xls(folder_path + fn,SHEET_START,expense_array,categories_dic)
				if next_row!=-1:
					next_row = parse_isrcrd_xls(folder_path + fn,next_row,expense_array,categories_dic)
			for exp in expense_array:
				print_to_csv(output_file, exp)
	print "Done!"

if __name__ == "__main__":
	try:
		main()
	except:
		print "Error occured"
		sys.exit(1)
