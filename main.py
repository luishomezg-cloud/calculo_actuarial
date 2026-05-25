
import numpy as np
from actuarial_valuation import Valuation
from load_static_files import *
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
from graphics import graficar_actuarial_interactivo

age = []
reserve = []
funeral_aid = []
actuarial_valuation = []
af3 = []



def grafica_factor_actuarial_uno():
    x = [i for i in range(55, 91)]    
    y = [search_actuarial_factor_1('M', i) for i in x]
    #plt.plot(x, y, marker='.', linestyle='--')
    plt.bar(x,y)
    #plt.plot(x, y)
    plt.title("Factor Actuarial 1")
    plt.xlabel("Edad de referencia")
    plt.ylabel("Mesadas Pensionales")    
    plt.grid()
    plt.show()

def grafica_factor_actuarial_dos():
    x = [i for i in range(55, 91)]    
    y = [search_actuarial_factor_2('M', i) for i in x]
    plt.plot(x, y, marker='.', linestyle='--')
    plt.plot(x, y)
    plt.title("Factor Actuarial 2 (Porcentaje de Entre 5 y 10 SMMLV)")
    plt.xlabel("Edad de referencia")
    plt.ylabel("Proporción Auxilio Funerario")
    plt.grid()
    plt.show()

def grafica_calculo_funcion_edad():

    periods = [("19/03/1990","16/02/2015"),]    

    for y in range(1985, 2026):
        v = Valuation(birthdate=f"01/01/1950",
                    afiliation="01/04/1994",
                    omission_periods=periods,
                    last_salary=644350,
                    gender="M",
                    quoted_weeks=0,
                    court_date=f"01/01/{y}")

        age.append(v.age)
        reserve.append(v.reserve)
        funeral_aid.append(v.funeral_aid)
        actuarial_valuation.append(v.valuation)
        af3.append(v.af3)

            

if __name__ == "__main__":
    
    periods = [("19/03/1990","16/02/2015"),]
    v = Valuation(birthdate=f"01/01/1950",
                    afiliation="01/04/1994",
                    omission_periods=periods,
                    last_salary=644350,
                    gender="M",
                    quoted_weeks=0,
                    court_date=f"01/01/2026")
    print(v)

    #grafica_factor_actuarial_uno()
    # grafica_factor_actuarial_dos()
    grafica_calculo_funcion_edad()
    graficar_actuarial_interactivo(age, reserve, funeral_aid, actuarial_valuation, af3)
    #graficar_separados()