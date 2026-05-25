from datetime import datetime, timedelta

def str_to_date(string_date):
    return datetime.strptime(string_date, "%d/%m/%Y")
