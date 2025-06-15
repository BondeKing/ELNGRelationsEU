# For information about how to use the eurostat API, go to: https://pypi.org/project/eurostat/
# Source:
# https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_203_v/default/table?lang=en&category=nrg.nrg_price.nrg_pc
# https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204__custom_14965471/default/table?lang=en

import eurostat
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math
import Data_entsoe
import Util

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

def Get_el_price_data(area="EU27_2020", type=""):
    
    e1 = "NRG_PC_204" # Electricity prices for household consumers
    e2 = "NRG_PC_205" # Electricity prices for non-household consumers
    
    df1 = eurostat.get_data_df(e1)
    df2 = eurostat.get_data_df(e2)
    
    el1 = df1.loc[(df1["nrg_cons"] == "KWH2500-4999") & (df1["tax"] == "X_TAX") & (df1["currency"] == "EUR") & (df1["geo\TIME_PERIOD"] == area)]
    el2 = df2.loc[(df2["nrg_cons"] == "KWH2500-4999") & (df2["tax"] == "X_TAX") & (df2["currency"] == "EUR") & (df2["geo\TIME_PERIOD"] == area)]
    
    el1 = el1.drop(columns=["freq","product","unit","nrg_cons","tax","currency","geo\TIME_PERIOD"]).reset_index(drop=True)
    el2 = el2.drop(columns=["freq","product","unit","nrg_cons","tax","currency","geo\TIME_PERIOD"]).reset_index(drop=True)
    
    return el1, el2



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
    
    #print(production["geo\TIME_PERIOD"])    
        
    total_production = df[df["siec"]=="TOTAL"]
    total_production = total_production[total_production["unit"]=="GWH"]
    total_production = total_production.drop(columns=["freq","siec","unit"])
    
    if area != None: 
        production = production[production["geo\TIME_PERIOD"]==area]
        total_production = total_production[total_production["geo\TIME_PERIOD"]==area]

    res = production.drop(columns=["geo\TIME_PERIOD"]).reset_index(drop=True).div(total_production.drop(columns=["geo\TIME_PERIOD"]).reset_index(drop=True))
    
    return res.dropna(axis=1, how="all")


# This function finds the el production contribution form a group of countries for a given source and relative to the EU.
def Plot_relative_el_production(area=None, type="TOTAL"):
    
    df = eurostat.get_data_df("NRG_CB_PEM")
    
    production = df[df["siec"]==type]
    production = production[production["unit"]=="GWH"]
    production = production.drop(columns=["freq","siec","unit"])
    production = production.reset_index(drop=True).dropna(axis=1, how="all")
    
    eu_production = production[production["geo\TIME_PERIOD"]=="EU27_2020"].reset_index(drop=True).dropna(axis=1, how="all")
    
    production = production.drop(production[production["geo\TIME_PERIOD"]=="EU27_2020"].index)
    
    if area != None:
        for country in production["geo\TIME_PERIOD"]:
            if country not in area:
                production = production.drop(production[production["geo\TIME_PERIOD"]==country].index)
    
    vals = []
    dates = []
    
    for country in production["geo\TIME_PERIOD"]:
        col = []    
        
        for month in production.keys()[1:]:
            if month not in eu_production.keys():
                continue
            
            val = (production[production["geo\TIME_PERIOD"]==country][month].values/(eu_production[month].values))[0]
            
            if not (0<val<1) :
                val = float(0)
            
            col.append(val)
            
            if month not in dates:
                dates.append(month)
        
        vals.append(np.array(col))    
    
    
    
    dates.append(np.datetime64(dates[-1]) + np.timedelta64(1, 'M'))
    time = np.arange(dates[0], dates[-1], dtype='datetime64[M]')    
    plt.stackplot(time, np.array(vals), labels=production["geo\TIME_PERIOD"])
    plt.legend(loc='best')
    plt.show()
    
    return production
            

# This function plots the size of a counties contrebution of electicity generation for one or multiple el generation sources relative to the EU or another country or itself.
# Use this function to show what the composition of electicity production sources for a country or the EU.
def Plot_relative_source_of_el_production(type = None, area=None, start = None, end = None, relativ_to="EU27_2020", plot_type="stack", no_plot = False):
    
    production = eurostat.get_data_df("NRG_CB_PEM")
    
    production = production[production["unit"]=="GWH"]
    production = production.drop(columns=["freq","unit"])
    production = production.reset_index(drop=True).dropna(axis=1, how="all")
    
    if relativ_to != "self":
        total_production = production[production["geo\TIME_PERIOD"]==relativ_to][production["siec"]=="TOTAL"].drop(columns=["siec"]).reset_index(drop=True).dropna(axis=1, how="all")
    
    if area != None:
        for country in production["geo\TIME_PERIOD"]:
            if country not in area:
                production = production.drop(production[production["geo\TIME_PERIOD"]==country].index)        
    else:
        production = production.drop(production[production["siec"]=="TOTAL"].index)
        #production = production[production["geo\TIME_PERIOD"]=="EU27_2020"]
        production = production.drop(production[production["geo\TIME_PERIOD"]=="EU27_2020"].index)
        
    
    if relativ_to == "self":
        total_production = production[production["siec"]=="TOTAL"].drop(columns=["siec"]).reset_index(drop=True).dropna(axis=1, how="all")
    
    if type != None:
        for t in production["siec"]:
            if t not in type:
                production = production.drop(production[production["siec"]==t].index)
        if area == None:
            area = production["geo\TIME_PERIOD"].values
            print(area)
                
    
    
    if start != None:
        s = np.datetime64(start)
        for date in production.keys()[2:]:
            if s > np.datetime64(date):
                production = production.drop(columns=[date])
        
    if end != None:
        e = np.datetime64(end)
        for date in production.keys()[2:]:
            if e < np.datetime64(date):
                production = production.drop(columns=[date])
    
    
    vals = []
    dates = []
    data = {}
    ret_dict = {}
    
    if plot_type == "line":
        for t in production["siec"]:
            data[t] = []
    
    i = 0
    
    
    for country in production["geo\TIME_PERIOD"]:
        labels = []
        j= 0
        ret_dict[country] = {}    
        for t in production[production["geo\TIME_PERIOD"]==country]["siec"]:
            col = []
            labels.append(transelate_siec(t))
            sum = 0
            ret_dict[country][t] = {}
            
            for month in production.keys()[2:]:
                if month not in total_production.keys():
                    continue
                
                if relativ_to == "self":
                    
                    #val = (production[production["geo\TIME_PERIOD"]==country][production["siec"]==t][month].values/(total_production[total_production["geo\TIME_PERIOD"]==country][month].values))[0]
                    v1 = production[production["geo\TIME_PERIOD"]==country]#[production["siec"]==t]#[month].values
                    v1 = v1[v1["siec"]==t]
                    v1 = v1[month]
                    v2 = total_production[total_production["geo\TIME_PERIOD"]==country]#[month]#.values
                    v2 = v2[month]
                    val = (v1.values/v2.values)[0]
                else:
                    val = (production[production["geo\TIME_PERIOD"]==country][production["siec"]==t][month].values.div((total_production[month].values))[0])
                
                if not (0<val<1) :
                    val = float(0)
                
                col.append(val)
                
                if month not in dates:
                    dates.append(month)
                
                sum += val    
                ret_dict[country][t][month[:4]] = sum/len(col)    
                
            
            if plot_type == "stack":
                vals.append(np.array(col))
            elif plot_type == "line":
                data[t].append(np.array(col))    
        
        
        if plot_type == "stack" and not no_plot:
            labels = np.array(labels)
            dates.append(np.datetime64(dates[-1]) + np.timedelta64(1, 'M'))
            time = np.arange(dates[0], dates[-1], dtype='datetime64[M]')    
            plt.stackplot(time, np.array(vals), labels=labels)
            plt.legend(loc='upper left')
            plt.show()
    
    if no_plot:
        return ret_dict
            
    if plot_type == "line":
        
        labels =production["geo\TIME_PERIOD"].values
        
        
        for t in data:
            
            dates.append(np.datetime64(dates[-1]) + np.timedelta64(1, 'M'))
            time = np.arange(dates[0], dates[-1], dtype='datetime64[M]')
            
            size= 15
            
            if size<len(area):
                j = 0
                for i in range(len(data[t])):
                    plt.plot(time, np.array(data[t][i]), label=labels[i])
                    j+=1
                    if j == size:
                        plt.legend(loc='upper left')
                        plt.title("Line plot of el generation from "+transelate_siec(t)+" relative to "+relativ_to)
                        plt.show()
                        j=0
                        
                    
            else:      
                for i in range(len(data[t])):
                    plt.plot(time, np.array(data[t][i]), label=labels[i])    
                
            #plt.plot(time, np.array(data[t]), labels=labels)
            plt.legend(loc='upper left')
            plt.title("Line plot of el generation from "+transelate_siec(t)+" relative to "+relativ_to)
            plt.show()
    
    
    return ret_dict


def get_gas_production_data(area):

    ret_dict = {}
    
    filter = {"geo": area, "siec": ["G3000"], "unit": ["PC"]}
    production = eurostat.get_data_df("NRG_CB_PEM", filter_pars=filter)
    production = production.drop(columns=["freq","unit","siec"])
    production = production.reset_index(drop=True).dropna(axis=1, how="all")

    for country in production["geo\TIME_PERIOD"]:

        ret_dict[country] = {}    
        ret_dict[country]["G3000"] = {}        
        sum = 0
        i=0
        current_year = "2017"
        for month in production.keys()[1:]:

            year = month[:4]
            
            if int(year) < 2017:
                continue
            
            if year != current_year:
                if i != 0:
                    ret_dict[country]["G3000"][current_year] = sum/i
                else:
                    ret_dict[country]["G3000"][current_year] = 0
                sum = 0
                i=0
                current_year = year
               
            val = production[production["geo\TIME_PERIOD"]==country][month].values[0]/100
                
            if not (0<val<1) :
                val = float(0)
            else:
                i+=1     
                    
            sum += val
               
        if i != 0:
            ret_dict[country]["G3000"][current_year] = sum/i
    
    return ret_dict



def transelate_siec(siec):
    
    t = {
        "TOTAL": "Total",
        "CF": "Combustible fuels",
        "CF_R": "Combustible fuels - renewable",
        "CF_NR": "Combustible fuels - non-renewable",
        "C0000": "Coal",# and manufactured gases",
        "G3000": "Natural gas",
        "O4000XBIO": "Oil and petroleum products",# (excluding biofuel portion)",
        "RA000": "Renewables and biofuels",
        "RA100": "Hydro",
        "RA110": "Pure hydro power",
        "RA120": "Mixed hydro power",
        "RA130": "Pumped hydro power",
        "RA200": "Geothermal",
        "RA300": "Wind",
        "RA310": "Wind on shore",
        "RA320": "Wind off shore",
        "RA400": "Solar",
        "RA410": "Solar thermal",
        "RA420": "Solar photovoltaic",
        "RA500_5160": "Other renewable energies",
        "N9000": "Nuclear",# fuels and other fuels n.e.c.",
        "X9900": "Other fuels n.e.c.",
        "FE": "Fossil energy",
    }
    
    return t[siec]


    
def Get_relative_electricity_export(area):
    
    for a in area:
        if a not in all_countries:
            print(a + " not a valid area from eurostat")
            
    filter = {"geo": area, "siec": ["E7000"], "unit": ["GWH"]} #, "nrg_bal": ["EXP"]}
    electricity = eurostat.get_data_df("NRG_BAL_C", filter_pars=filter)
    exported_electricity = electricity[electricity["nrg_bal"]=="EXP"]
    exported_electricity = exported_electricity.drop(columns=["freq","unit","siec", "nrg_bal"])
    exported_electricity_t = exported_electricity.reset_index(drop=True).dropna(axis=1, how="all")
    
    imported_electricity = electricity[electricity["nrg_bal"]=="IMP"]
    imported_electricity = imported_electricity.drop(columns=["freq","unit","siec", "nrg_bal"])
    imported_electricity_t = imported_electricity.reset_index(drop=True).dropna(axis=1, how="all")
    
    
    filter = {"geo": area, "siec": ["TOTAL"], "unit": ["GWH"]}
    total_el_production = eurostat.get_data_df("NRG_CB_PEM", filter_pars=filter)
    total_el_production = total_el_production.drop(columns=["freq","unit","siec"])
    total_el_production_t = total_el_production.reset_index(drop=True).dropna(axis=1, how="all")
    

    

 
    relative_el_export = {}
    relative_el_export_defficit = {}
    trade_exposure = {}
    export_dict = {}
    import_dict = {}
        
    
    
    for country in area:
        total_el_production = total_el_production_t[total_el_production_t["geo\TIME_PERIOD"]==country].drop(columns = ["geo\TIME_PERIOD"])
        exported_electricity = exported_electricity_t[exported_electricity_t["geo\TIME_PERIOD"]==country].drop(columns = ["geo\TIME_PERIOD"])
        imported_electricity = imported_electricity_t[imported_electricity_t["geo\TIME_PERIOD"]==country].drop(columns = ["geo\TIME_PERIOD"])
        
        relative_el_export[country] = []
        relative_el_export_defficit[country] = []
        trade_exposure[country] = {}
        export_dict[country] = {}
        import_dict[country] = {}
        
        years = []
        sum = 0
        n_month = 12
         
        for month in total_el_production.keys():
            year = month[:4]
            
            
            if year not in years:
                if n_month != 12:
                    print("missing months")
                    continue
                n_month = 1
                sum = total_el_production[month].values
                years.append(year)
            elif n_month == 11:
                n_month += 1
                sum += total_el_production[month].values
                
                if year not in exported_electricity.keys():
                    break                

                relative_el_export[country].append(exported_electricity[year].values/sum)
                relative_el_export_defficit[country].append((exported_electricity[year].values - imported_electricity[year].values)/sum)
                trade_exposure[country][year] = ((exported_electricity[year].values + imported_electricity[year].values)/sum)[0]
                export_dict[country][year] = (exported_electricity[year].values/sum)[0]
                import_dict[country][year] = (imported_electricity[year].values/sum)[0]
            else:
                sum += total_el_production[month].values
                n_month += 1
        
    
    
    return relative_el_export, years, relative_el_export_defficit, trade_exposure, export_dict, import_dict

 
def Plot_electricity_export(area, no_plot = False):
    
    exported, dates, defficit, exposure, exported_dict, imported_dict = Get_relative_electricity_export(area)
    
    if no_plot:
        return exposure, exported_dict, imported_dict
    
    """
    labels = np.array(area+" realative gorss el export")
    #dates.append(np.datetime64(dates[-1]) + np.timedelta64(1, 'M'))
    time = np.arange(dates[0], dates[-1], dtype='datetime64[Y]')    
    plt.plot(time, np.array(exported), label=labels)
    plt.plot(time, np.array(defficit), label=np.array(area+" relative net el export"))
    plt.legend(loc='upper left')
    plt.show()
    """
    return None 


def Find_electricty_sources_for_areas(area, end, start):
    
    domestic_el_p_dict = Plot_relative_source_of_el_production(area=area, start=start, end=end, relativ_to="self", no_plot=True)
    exposure_dict, export_dict, import_dict = Plot_electricity_export(area, no_plot=True)
    
    for area in domestic_el_p_dict:
        
        
        print (area+": \n")
        for t in domestic_el_p_dict[area]:
            
            fstr = transelate_siec(t) + "| "
            for year in domestic_el_p_dict[area][t]:
                
                fstr = fstr + "year: " + "%.2f" % domestic_el_p_dict[area][t][year]+" | " 
                
            print(fstr)
        
        fstr = "trade exposure: "
        for year in exposure_dict[area]:
            
            fstr = fstr + "year:  " + "%.2f" % exposure_dict[area][t][year]+" | "
                              
    
    
    return None
    
            
def transpose_production(df):
    return df.set_index("geo\TIME_PERIOD").transpose()

def Get_data_for_period(df, years):
    
    response_df = pd.DataFrame()
    
    for key in df.keys():
        
        if key[:4] in years:
            response_df[key] = df[key]
    
    return response_df


def gas_consumption_relative_to_electricty_consumption():
    
    
    filter = {"nrg_bal":["FC_E"], "siec": ["G3000"], "unit": ["TJ_GCV"]}
    gas = eurostat.get_data_df("nrg_cb_gas", filter_pars=filter)
    gas = gas.drop(columns=["freq","unit","siec", "nrg_bal"])
    gas = gas.reset_index(drop=True).dropna(axis=1, how="all")
    
    filter = {"nrg_bal":["NEP"], "siec": ["E7000"], "unit": ["GWH"]}
    el = eurostat.get_data_df("nrg_cb_e", filter_pars=filter)
    el = el.drop(columns=["freq","unit","siec", "nrg_bal"])
    el = el.reset_index(drop=True).dropna(axis=1, how="all")
    
    
    dict = {}
    d_list = []
    
    
    print("############### TOTAL GAS CONSUMPTION RELATIVE TO TOTAL EL PRODUCTION ############")
    
    for area in gas["geo\TIME_PERIOD"]:
        
        fstr = ""
        
        dict[area]= {}
        sum = 0 
        i = 0
        d_point = Util.make_new_d_point(area=area)
        
        for year in gas[1:]:
            
            gas_val = gas["geo\TIME_PERIOD" == area][year].values[0]
            el_val = el["geo\TIME_PERIOD" == area][year].values[0]
            
            val = gas_val/(3.6*el_val)
            sum += val
            i += 1            
            
            dict[area][year] = val
            
            fstr += "year:  " + "%.2f" % val + " | "
        
        avg = sum/i
        fstr = area + "| avg: " + "%.2f" % avg + " | " + fstr
        
        d_point["data"] = avg
        d_point["str"] = fstr
        d_list.append(d_point)    
            
    Util.sort_and_print_d_list(d_list)
    
    
    return dict
    



#total_production = el_production[el_production["siec"]==total_siec]

'''
data=Get_relativ_el_production_data("DE")

print(data)

data = Get_data_for_period(data, ["2020", "2021", "2022"])

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


Get_relativ_el_production_data()

el1, el2 = Get_el_price_data()

print(el1.iloc[0])
#print(el2)



#el1 = el1.set_index("geo\TIME_PERIOD").transpose()
#el2 = el2.set_index("geo\TIME_PERIOD").transpose()

el1.iloc[0].plot().set_ylabel("Euro per kWh")
#el2.plot()

plt.legend()
plt.show()
'''




# would be intresting to see what the correlation between TTS and domestic el prices are for countries with a very high reliance on gas for el production and what the correlation is for 
# countires with low or no reliance on gas for electricity. The expectation here whould be that countries with lower gas dependencies would have less correlation with changes in gas prices.
# countries to look at for high dependecie for gas based electricity production would be Italy. For countries with a low dependance on gas would be Sweden and Norway.


largest_contributing_countries = ["DE","FR", "ES", "IT", "SE","PL", "NL","BE", "CZ", "DK","FI"]
all_countries = ['AL', 'AT', 'BA', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'GE', 'HR', 'HU', 'IE', 'IS', 'IT', 'LT', 'LU', 'LV', 'MD', 'ME', 'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'RS', 'SE', 'SI', 'SK', 'TR', 'UA', 'UK', 'XK']

high_gas = ["BE", "GE", "EL", "IE", "ES", "MD", "LV", "NL", "UK", "TR", "MT", "IT"]
mid_gas = ["CZ", "DE", "HU", "HR", "LT", "MK", "PT"]
low_gas = ["DK", "FI", "LU", "PL", "RS", "SI", "FR"]
nordics = ["NO", "SE", "DK", "FI", "IS"]
notably_high = ["IE", "ES", "MD", "LV", "NL", "UK", "MT", "IT"]
notably_high_eu = ["IE", "ES", "MD", "LV", "NL", "MT", "IT"]
notably_high_eu_larger = ["IE", "ES", "NL", "IT"]

#Plot_relative_el_production(area=countries, type ="G3000")

#type = ["G3000", "C0000", "N9000", "RA100", "RA300", "RA400", "RA200"]
type = ["G3000"]
#countries = None
#Plot_relative_source_of_el_production(type=type, start="2017-01", end="2025-01", area=["IT"], relativ_to="self")
#Plot_relative_source_of_el_production(type=type, start="2017-01", end="2025-01", area=["MT","MD"], relativ_to="self", plot_type="line")


trade_exposure = {}
export_dict = {}
import_dict = {}


data = Plot_electricity_export(Data_entsoe.area, no_plot=True)
trade_exposure = data[0]
export_dict = data[1]
import_dict = data[2]


print("################################ EL TRADE EXPOSURE ((IMPORT + EXPORTS)/DOMESTIC PRODUCTION)####################################################")

d_list = []
for area in trade_exposure:
    sum = 0
    i = 0
    fstr = ""
    d_point = Util.make_new_d_point(area=area)
    for year in trade_exposure[area]:
        if int(year) < 2017:
            continue
        
        i+=1

        te = trade_exposure[area][year]
        testr = "%.2f" % te
        sum += te
        
        fstr += year+": te "+ testr +" | "
    
    avg = sum/i
    astr = "%.2f" % avg
    
    fstr = area+"| avrage: " + astr + " | " + fstr
    
    d_point["data"] = avg
    d_point["str"] = fstr
    d_list.append(d_point)
    
    #print(fstr)

Util.sort_and_print_d_list(d_list)

#Find the gas consumption for each country, and find out what the corrolation  with el/gas price corr of this, and compare it with el gen from gas amount.    