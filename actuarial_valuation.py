import math
from datetime import datetime, timedelta, date
from load_static_files import *
from utils import str_to_date

class Valuation:
    
    def __init__(self, birthdate, afiliation,
                 omission_periods,
                 last_salary, gender, 
                 quoted_weeks, court_date=None):
        
        if court_date is None:
            self.court_date=datetime.now()
        else:
            self.court_date = str_to_date(court_date)

        self.birthdate = str_to_date(birthdate)
        self.afiliation = str_to_date(afiliation)        
        # self.start_omission = str_to_date(start_omission)
        # self.end_omission = str_to_date(end_omission)
        self.last_salary = last_salary
        self.gender = gender
        self.quoted_weeks = quoted_weeks
        
        self.__set_extremes(omission_periods)
        self.__set_start_omission()
        self.__set_end_omission()
        self.__self_afiliation_interest()
        self.__set_age_compliance()
        self.__set_age_date()
        self.__set_actual_age()
        self.__set_missed_weeks()
        self.__set_projected_weeks()
        self.__set_total_weeks()
        self.__set_minimum_weeks()
        self.__set_compliance_weeks_date()
        self.__set_reference_date()
        self.__set_reference_age()
        if self.court_date < self._reference_date:            
            self.__set_minimum_wage(str(self.court_date.year))
        else:
            self.__set_minimum_wage(str(self._reference_date.year))
        self.__set_national_average_salary_causation()
        self.__set_national_average_salary_reference()
        self.__set_base_salary()
        self.__set_reference_salary()
        self.__set_replacement_rate()
        self.__set_reference_pension()
        self.__set_funeral_assistance()    
        self.__set_actuarial_factor_1()
        self.__set_actuarial_factor_2()
        self.__set_actuarial_reserve()
        self.__set_actuarial_factor_3()
        self.__set_total_actuarial_reserve()
        self.__set_pensional_fixed_term_deposit()
        self.__set_proportional_actuarial_value()
        self.__set_actual_actuarial_reserve()
        self.__set_actuarial_valuation()
    
    def __set_extremes(self, omission_periods):
        self._omission_periods = []
        for start_str, end_str in omission_periods:
            self._omission_periods.append({
                "start": str_to_date(start_str),
                "end": str_to_date(end_str)
            })
    
    def __set_start_omission(self):        
        self.start_omission = min([p["start"] for p in self._omission_periods])    

    def __set_end_omission(self):
        self.end_omission = max([p["end"] for p in self._omission_periods])

    def __set_age_date(self):
        self._age_date = self.birthdate + timedelta(self._age_compliance*365.25)

    def __set_compliance_weeks_date(self):
        #self._weeks_date = (datetime.now() + timedelta((self._minimum_weeks - self._total_weeks)*7))
        missing_weeks = self._minimum_weeks - (self._missed_weeks + self.quoted_weeks)
        self._weeks_date = self.end_omission + timedelta(missing_weeks * 7)

    def __set_actual_age(self):
        self._actual_age = ((self.court_date - self.birthdate).days/365.25)

    def __set_age_compliance(self):
        self._age_compliance = {"M":62, "F":57}.get(self.gender)
    
    def __set_reference_age(self):
        if self._weeks_date < self._age_date:
            self._reference_age = self._age_compliance
        else:
            self._reference_age = ((self._reference_date - self.birthdate).days)/365.25

    def __set_reference_date(self):                
        self._reference_date = max(self._age_date, self._weeks_date)

    def __set_missed_weeks(self):
        total_missed_days = 0
        for period in self._omission_periods:
            days = (period["end"] - period["start"]).days
            total_missed_days += days
        self._missed_weeks = total_missed_days/7

    def __set_minimum_wage(self, year):        
        self._minimum_salary = float(search_minimum_salary(year))

    def __set_national_average_salary_reference(self):
        if self._reference_age - math.floor(self._reference_age) == 0:
            self._nas_reference = search_national_average_salary(self._reference_age)
        else:
            floor_nas = search_national_average_salary(math.floor(self._reference_age))
            ceil_nas = search_national_average_salary(math.ceil(self._reference_age))
            d1 = self._reference_age*365.25 - math.floor(self._reference_age)*365.25
            d2 = 365.25 - d1
            self._nas_reference = self.__interpolate_n_a_s(floor_nas, ceil_nas, d1, d2)

    def __set_national_average_salary_causation(self):
        causation_age = (self.end_omission - self.birthdate).days/365.25
        floor_nas = search_national_average_salary(math.floor(causation_age))
        ceil_nas = search_national_average_salary(math.ceil(causation_age))
        d1 = causation_age*365.25 - math.floor(causation_age)*365.25
        d2 = 365.25 - d1
        self._nas_causation = self.__interpolate_n_a_s(floor_nas, ceil_nas, d1, d2)
    
    def __interpolate_n_a_s(self, v1, v2, d1, d2):
        """Fórmula matemática del Decreto 1833 para interpolar SMN, FAC1 y FAC2"""
        return ((d1 * v2) + (d2 * v1)) / (d1 + d2)

    """CALCULAR SALARIO DE REFERENCIA"""
    def __set_reference_salary(self):
        self._reference_salary = self._base_salary * (self._nas_reference/self._nas_causation)
        if self._reference_salary < self._minimum_salary:            
            self._reference_salary = self._minimum_salary        

    def __set_base_salary(self):        
        i1 = 0
        i2 = 0
        if self.court_date < self._reference_date:
            lookup_month = self.court_date.month
            lookup_year = self.court_date.year
            if lookup_month - 1 == 0:
                lookup_month = 12
                lookup_year = lookup_year - 1
                i1 = search_inflation(lookup_year, lookup_month)
            else:
                i1 = search_inflation(lookup_year, lookup_month - 1)
        else:
            lookup_year = self._reference_date.year
            lookup_month = self._reference_date.month
            if lookup_month - 1 == 0:
                lookup_month = 12
                lookup_year = lookup_year - 1
                i1 = search_inflation(lookup_year, lookup_month)
            else:
                i1 = search_inflation(lookup_year, lookup_month - 1)            
        i2 = search_inflation(self.end_omission.year, self.end_omission.month)
        self._base_salary = (self.last_salary * (i1/i2))

    def __set_replacement_rate(self):    
        if self._total_weeks > self._minimum_weeks:
            self._replacement_rate = (0.655 - 0.005 * 
                                      min((self._reference_salary/self._minimum_salary), 25) + 
                                      min(((0.015 * 
                                                      math.floor((self._total_weeks-self._minimum_weeks)/50))), 0.15))
        else:
            self._replacement_rate = 0.655 - 0.005 * min((self._reference_salary/self._minimum_salary), 25)

    def __set_projected_weeks(self):        
        self._projected_weeks = ((self.court_date - self.end_omission).days)/7

    def __set_total_weeks(self):
        self._total_weeks = self._missed_weeks + self._projected_weeks + self.quoted_weeks        
    
    def __set_reference_pension(self):
        self._reference_pension = self._reference_salary * self._replacement_rate
        if self._reference_pension < self._minimum_salary:
            self._reference_pension = self._minimum_salary

    def __set_funeral_assistance(self):
        if self._reference_pension < (self._minimum_salary * 5):
            self._funeral_assistance = self._minimum_salary * 5
        elif self._reference_pension > (self._minimum_salary * 10):
            self._funeral_assistance = self._minimum_salary * 10
        else:
            self._funeral_assistance = self._reference_pension

    def __set_actuarial_factor_1(self):
        if self._reference_age - math.floor(self._reference_age) == 0:
            self._actuarial_factor_1 = search_actuarial_factor_1(self.gender, self._reference_age)
        else:            
            floor_af1 = search_actuarial_factor_1(self.gender, math.floor(self._reference_age))
            ceil_af1 = search_actuarial_factor_1(self.gender, math.ceil(self._reference_age))
            d1 = self._reference_age*365.25 - math.floor(self._reference_age)*365.25
            d2 = 365.25 - d1
            self._actuarial_factor_1 = self.__interpolate_n_a_s(floor_af1, ceil_af1, d1, d2)
    
    def __set_actuarial_factor_2(self):
        if self._reference_age - math.floor(self._reference_age) == 0:
            self._actuarial_factor_2 = search_actuarial_factor_2(self.gender, self._reference_age)
        else:            
            floor_af2 = search_actuarial_factor_2(self.gender, math.floor(self._reference_age))
            ceil_af2 = search_actuarial_factor_2(self.gender, math.ceil(self._reference_age))
            d1 = self._reference_age*365.25 - math.floor(self._reference_age)*365.25
            d2 = 365.25 - d1
            self._actuarial_factor_2 = self.__interpolate_n_a_s(floor_af2, ceil_af2, d1, d2)


    def __set_minimum_weeks(self):
        if self.gender == "M":
            self._minimum_weeks = 1300
        elif self.gender == "F":
            if self._age_date.year <= 2025:
                self._minimum_weeks = 1300
            elif self._age_date.year == 2026:
                self._minimum_weeks = 1250
            elif self._age_date.year == 2027:
                self._minimum_weeks = 1225
            elif self._age_date.year == 2028:
                self._minimum_weeks = 1200
            elif self._age_date.year == 2029:
                self._minimum_weeks = 1175
            elif self._age_date.year == 2030:
                self._minimum_weeks = 1150
            elif self._age_date.year == 2031:
                self._minimum_weeks = 1125
            elif self._age_date.year == 2032:
                self._minimum_weeks = 1100
            elif self._age_date.year == 2033:
                self._minimum_weeks = 1075
            elif self._age_date.year == 2034:
                self._minimum_weeks = 1050
            elif self._age_date.year == 2035:
                self._minimum_weeks = 1025            
            else:
                self._minimum_weeks = 1000

    def __set_actuarial_reserve(self):
        self._actuarial_reserve = ((self._reference_pension*self._actuarial_factor_1)+(self._funeral_assistance*self._actuarial_factor_2))

    def __set_total_actuarial_reserve(self):
        self._total_actuarial_reserve =  self._actuarial_reserve * self._actuarial_factor_3

    def __set_actual_actuarial_reserve(self):
        self._actual_actuarial_reserve = self._proportional_actuarial_value * self._actuarial_factor_3

    def __set_actuarial_factor_3(self):
        if self.court_date < self._reference_date:
            exp = ((self.court_date - self._reference_date).days/365.25)
            #print(f"Exponente: {exp}")
            self._actuarial_factor_3 = (1 + self._afiliation_interest)**exp
        else:
            self._actuarial_factor_3 = 1
    
    def __set_proportional_actuarial_value(self):
        factor = self._missed_weeks/self._minimum_weeks
        self._proportional_actuarial_value = self._actuarial_reserve * factor

    """"Depósito a término fijo DTF Pensional"""
    def __set_pensional_fixed_term_deposit(self):
        self._pensional_ftd = 1.0
        if self.court_date > self._reference_date:
            start = self._reference_date.year
            end = self.court_date.year            
            cumulative_factor = 1.0
            for y in range(start, end+1):                
                if y == self._reference_date.year:                    
                    days = (date(y, 12, 31) - self._reference_date.date()).days
                elif y == self.court_date.year:
                    days = (self.court_date.date() - date(y-1, 12, 31)).days
                else:
                    days = 365.25
                #inflation = search_anual_inflation(y-1) / 100
                #print(f"Inflación encontrada {inflation}")
                #anual_ftd = ((1 + self._afiliation_interest)*(1+inflation))
                anual_ftd = 1 + self._afiliation_interest
                span_ftd = anual_ftd**(days/365.25)
                cumulative_factor *=span_ftd
                #print(f"Interes para el año: {y} Interes: {span_ftd} Acumulado: {cumulative_factor}")
            self._pensional_ftd = cumulative_factor

    def __self_afiliation_interest(self):
        self._afiliation_interest = 0.04

    def __set_actuarial_valuation(self):
        if self.court_date <= self._reference_date:
            self._actuarial_valuation = self._proportional_actuarial_value * self._actuarial_factor_3
        else:
            #print("agregando de DTF Pensional:...")
            self._actuarial_valuation = self._proportional_actuarial_value * self._pensional_ftd

    """Pensión de referencia por Factor Actuarial 1"""
    @property
    def reserve(self):
        return self._reference_pension * self._actuarial_factor_1

    @property
    def funeral_aid(self):
        return self._funeral_assistance * self._actuarial_factor_2
    
    @property
    def age(self):
        return self._actual_age
    
    @property
    def af3(self):
        return self._actuarial_factor_3

    @property
    def ftd(self):
        return self._pensional_ftd

    @property
    def valuation(self):
        return self._actuarial_valuation

    def __str__(self):
        return (f"Edad actual: {self._actual_age}"+
                f"\nEdad de referencia: {self._reference_age}"+
                f"\nFecha de referencia: {self._reference_date}"+
                f"\nSemanas omisas: {self._missed_weeks}"+
                f"\nSemanas cotizadas: {self.quoted_weeks}"+
                f"\nSemanas proyectadas: {self._projected_weeks}"+                                
                f"\nSemanas totales: {self._total_weeks}"+
                f"\nSemanas mínimas: {self._minimum_weeks}"+
                f"\nFecha de corte: {self.court_date}"+
                f"\nSalario Mínimo: {self._minimum_salary}"+
                f"\nSalario Medio Nacional Caus: {self._nas_causation}"+
                f"\nSalario Medio Nacional Ref: {self._nas_reference}"+
                f"\nSalario base indexado: {self._base_salary}"+
                f"\nSalario de referencia: {self._reference_salary}"+
                f"\nTasa de reemplazo: {self._replacement_rate}"+
                f"\nPensión de referencia: {self._reference_pension}"+
                f"\nAuxilio Funerario de referencia: {self._funeral_assistance}"+
                f"\nFactor actuarial 1: {self._actuarial_factor_1}"+
                f"\nFactor actuarial 2: {self._actuarial_factor_2}"+
                f"\nFactor actuarial 3: {self._actuarial_factor_3}"+
                f"\nValor de la reserva actuarial: ${self._actuarial_reserve:,.2f}"+
                f"\nReserva actuarial aplicando FA3: ${self._total_actuarial_reserve:,.2f}"+
                f"\nReserva proporcional semanas adeudadas: ${self._proportional_actuarial_value:,.2f}"+
                f"\nReserva proporcional X FA3: ${self._actual_actuarial_reserve:,.2f}"+
                f"\nFactor DTF Pensional: {self._pensional_ftd:,.2f}"+
                f"\nValor del Cálculo actuarial (Semanas adeudadas): ${self._actuarial_valuation:,.2f}")