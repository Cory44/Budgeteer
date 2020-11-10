import datetime

def getDates(month, year):
    current_month = datetime.datetime(int(year), int(month), 1).strftime("%B")
    current_year = datetime.datetime(int(year), int(month), 1).strftime("%Y")
    previous_month_name = (datetime.datetime(int(year) - 1, 12,1) if month == "01" else datetime.datetime(int(year), int(month) - 1,  1)).strftime("%B")
    previous_month_num = (datetime.datetime(int(year) - 1, 12, 1) if month == "01" else datetime.datetime(int(year), int(month) - 1, 1)).strftime("%m")
    previous_year = (datetime.datetime(int(year) - 1, 12, 1) if month == "01" else datetime.datetime(int(year), int(month) - 1, 1)).strftime("%Y")
    next_month_name = (datetime.datetime(int(year) + 1, 1, 1) if month == "12" else datetime.datetime(int(year), int(month) + 1, 1)).strftime("%B")
    next_month_num = (datetime.datetime(int(year) + 1, 1, 1) if month == "12" else datetime.datetime(int(year), int(month) + 1, 1)).strftime("%m")
    next_year = (datetime.datetime(int(year) + 1, 1, 1) if month == "12" else datetime.datetime(int(year), int(month) + 1, 1)).strftime("%Y")

    dates = {"current_month": current_month , "current_year": current_year ,
             "previous_month_name": previous_month_name , "previous_year": previous_year ,
             "previous_month_num": previous_month_num ,
             "next_month_name": next_month_name , "next_year": next_year , "next_month_num": next_month_num}

    return dates