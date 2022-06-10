from sys import argv, exit
import os
from datetime  import date


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




sales_csv = get_sales_csv()
order_dir = get_order_dir(sales_csv)
