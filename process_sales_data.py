from sys import argv, exit
import os
from datetime  import date
from openpyxl import Workbook
import pandas as pd
import re



def get_sales_csv():

    # check whether command line parameter is provided.
    if len(argv) >= 2:
        sales_csv = argv[1]


    # check whether the csv path has an existing file.
        if os.path.isfile(sales_csv):
            return sales_csv
        else:
            print("**ERROR** This name of CVS file does not exist")
            exit("Script execution aborted")
    else:
        print("**ERROR** NO CSV path provided")
        exit("Script execution aborted")

def  get_order_dir(sales_csv):

    # Get directory path from sales data CSV file .
    sales_dir = os.path.dirname(sales_csv)

    # Determine orders directory name (Orders_ YYYY-MM-DD)
    todays_date = date.today().isoformat()
    order_dir_name = 'Orders_' + todays_date

    # Build the  full path of directory.
    order_dir = os.path.join(sales_dir, order_dir_name)

    # make the directory if it does not already exist.
    if not os.path.exists(order_dir):
        os.makedirs(order_dir)

    return order_dir

def split_sales_into_order(sales_csv, order_dir):

    # Read data from the sales data csv into DataFrame.
    sales_df = pd.read_csv(sales_csv)

    # insert a new colum  name total price.
    sales_df.insert(7,'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])

    # Deleting unwanted columns.
    sales_df.drop(columns =['ADDRESS','CITY','STATE','POSTAL CODE','COUNTRY'], inplace=True )

    for order_id, order_df in sales_df.groupby('ORDER ID'):

        #Drop the order id column.
        order_df.drop(columns=['ORDER ID'], inplace=True)


        # Sort the order by item number.
        order_df.sort_values(by='ITEM NUMBER', inplace=True)

        #add grand total row at bottom.
        grand_total = order_df['TOTAL PRICE'].sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE': ['GRAND TOTAL:'], 'TOTAL PRICE': [grand_total]})
        order_df = pd.concat([order_df, grand_total_df])

        #Determine the save path of the order file.
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\W','', customer_name)
        order_file_name = 'order' + str(order_dir) + '_' + customer_name + '.xlxx'
        order_file_name = os.path.join(order_dir, order_file_name)

        #saving other information to Excel sheet
        order_file_path = 'C:\\gitsem2\\COMP593-Lab2\\sales_data.xlsx'
        sheet_name = 'order #' + str(order_id)
        order_df.to_excel(order_file_path , index=False, sheet_name=sheet_name)

        order_file_path = 'C:\\gitsem2\\COMP593-Lab2\\sales_data.xlsx'
        writer = pd.ExcelWriter(order_file_path , engine='xlsxwriter')
        order_df.to_excel(writer, index=False, sheet_name='report')

        Workbook = 'C:\\gitsem2\\COMP593-Lab2\\sales_data.xlsx'
        money_fmt = Workbook.add_format({'num_format': '$#,##0', 'bold': True})

        worksheet.set_column('G:K', 12, money_fmt)

sales_csv = get_sales_csv()
order_dir = get_order_dir(sales_csv)
split_sales_into_order(sales_csv, order_dir)
