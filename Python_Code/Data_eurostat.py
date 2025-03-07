# For information about how to use the eurostat API, go to: https://pypi.org/project/eurostat/
# Source:
# https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_203_v/default/table?lang=en&category=nrg.nrg_price.nrg_pc
# https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204__custom_14965471/default/table?lang=en

import eurostat
import pandas as pd
import matplotlib.pyplot as plt

'''
toc_df = eurostat.get_toc_df()

energy = eurostat.subset_toc_df(toc_df, "Electricity prices")

#print(energy)

gas = eurostat.subset_toc_df(toc_df, "gas price")

#print(gas)
'''
# Electricity prices
e1 = "NRG_PC_204" # Electricity prices for household consumers
e2 = "NRG_PC_205" # Electricity prices for non-household consumers

# Gas prices
g1 = "NRG_PC_202" # Gas prices for household consumers
g2 = "NRG_PC_203" # Gas prices for non-household consumers

# Monthly electricity production by type
p = "NRG_CB_PEM"

# With ng production
ng_siec = "G3000"
total_siec = "TOTAL"

#el_price_data_household = eurostat.get_data_df(e1)
#el_price_data_non_household = eurostat.get_data_df(e2)


#gas_price_data_household = eurostat.get_data_df(g1)
#gas_price_data_non_household = eurostat.get_data_df(g2)

#print(el_price_data_household[el_price_data_household["currency"] == "EUR"])
#print(el_price_data_household)

#df = el_price_data_household
#relevant = df.loc[(df["nrg_cons"] == "KWH2500-4999") & (df["tax"] == "X_TAX") & (df["currency"] == "EUR")]

#print(relevant)
#print(el_price_data_household)

#index = el_price_data_household.keys()[7:]
#keys = relevant["geo\TIME_PERIOD"].to_string(index = False) #el_price_data_household[el_price_data_household["currency"] == "EUR"]["geo\TIME_PERIOD"]#.to_string(index = False)


#formated_df = ""

#el_price_data_household.plot()
#plt.show()


def Get_el_production_data(area=None, type="G3000"):
    
    df = eurostat.get_data_df("NRG_CB_PEM")
    production = df[df["siec"]==type]
    production = production[production["unit"]=="GWH"]
    production = production.drop(columns=["freq","siec","unit"])
    
    if area != None: 
        production = production[production["geo\TIME_PERIOD"]==area]

    return production


def Get_relativ_el_production_data(area=None, type="G3000"):
    
    df = eurostat.get_data_df("NRG_CB_PEM")
    
    production = df[df["siec"]==type]
    production = production[production["unit"]=="GWH"]
    production = production.drop(columns=["freq","siec","unit"])
        
    total_production = df[df["siec"]=="TOTAL"]
    total_production = total_production[total_production["unit"]=="GWH"]
    total_production = total_production.drop(columns=["freq","siec","unit"])
    
    if area != None: 
        production = production[production["geo\TIME_PERIOD"]==area]
        total_production = total_production[total_production["geo\TIME_PERIOD"]==area]

    res = production.drop(columns=["geo\TIME_PERIOD"]).reset_index(drop=True).div(total_production.drop(columns=["geo\TIME_PERIOD"]).reset_index(drop=True))
    
    return res.dropna(axis=1, how="all")
        
            
def transpose_production(df):
    return df.set_index("geo\TIME_PERIOD").transpose()

#total_production = el_production[el_production["siec"]==total_siec]

data=Get_relativ_el_production_data("DE")

print(data)

#t = transpose_production(data)

#t["DE"][-36:].plot(x = "Year and month", y="Gas production(MWH)")

data.transpose().plot()

plt.show()

#print(ng_production[ng_production["geo\TIME_PERIOD"]=="DE"])

#formated = Get_el_production_data().set_index("geo\TIME_PERIOD").transpose()

#print(formated)

#formated["DE"][-36:].plot(x = "Year and month", y="Gas production(MWH)")

#plt.show()

# make a list with the % of produced that is from natruall gas.