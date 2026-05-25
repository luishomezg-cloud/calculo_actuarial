from actuarial_valuation import Valuation

# periodos_omisión = [
#     ("01/02/1996", "30/09/1996"),  # Primer fragmento
#     ("01/03/1998", "31/01/2008"),  # Segundo fragmento    
# ]

# print("Calculo Uno:")

# v = Valuation("10/12/1967",
#               "01/04/1994", 
#               periodos_omisión,              
#               483382,
#               "F",
#               0)

# print(v)

# print("Calculo Dos: ")

periodos_omisión_2 = [
    ("01/05/1995","30/09/1996"),
    ("01/05/1998","30/05/1998"),
    ("01/07/1998","30/04/2012"),
    ("01/11/2012","30/06/2015")
]

v2 = Valuation("03/07/1962",
               "01/04/1994",
               periodos_omisión_2,
               1359800,
               "M",
               54.57)

print(v2)