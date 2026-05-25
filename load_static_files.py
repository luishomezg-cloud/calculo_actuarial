import csv

def search_minimum_salary(year):
    salary = 0
    try:
        with open(r"./static_files/Historico_salarios_minimos.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:                
                if row[0] == year:                    
                    salary = row[1]        
        return salary
    except Exception as e:
         raise e
    
def search_national_average_salary(age):
    average_salary = 0
    try:
        with open(r"./static_files/Salarios_medios_nacionales.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:                
                if row[0] == str(age):
                    average_salary = float(str(row[1]).replace(',', '.'))
        return average_salary
    except Exception as e:
         raise e

def search_inflation(year, month):
    intro_value = str(year)+"-"+"0"+str(month) if month < 10 else str(year)+"-"+str(month)
    inflation = 0
    try:
        with open(r"./static_files/IPC Series de empalme DANE.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if row[0] == str(intro_value):
                    inflation = float(str(row[1]).replace(',', '.'))        
        return inflation
    except Exception as e:
         raise e

def search_actuarial_factor_1(gender, age):
    af = 0
    column = 0
    if gender == "M":
        column = 1
    else:
        column = 2
    try:
        with open(r"./static_files/Factor_actuarial_1.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)            
            for row in reader:                
                if row[0] == str(age):
                    af = float(str(row[column]).replace(',', '.'))        
        return af
    except Exception as e:
         raise e
    

def search_actuarial_factor_2(gender, age):
    af = 0
    column = 0
    if gender == "M":
        column = 1
    else:
        column = 2
    try:
        with open(r"./static_files/Factor_actuarial_2.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)            
            for row in reader:                
                if row[0] == str(age):
                    af = float(str(row[column]).replace(',', '.'))        
        return af
    except Exception as e:
         raise e


def search_anual_inflation(age):
    ai = 0
    try:
        with open(r"./static_files/IPC Anual.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if row[0] == str(age):
                    ai = float(str(row[1]).replace(',', '.'))        
        return ai
    except Exception as e:
         raise e