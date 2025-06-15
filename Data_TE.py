#source: https://tradingeconomics.com/commodity/eu-natural-gas
import json
import math
import Analysis
import statistics
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import datetime as dt
import Data_eurostat

#TODO: Make code for handeling the data: Should be able to split into a dict of years and quarters as in entsoe.
# plot the data, and find staticial values for the data. Also find correlation between the gas for eu and el prices in germany, france, italy and spain.



def Get_TE_data(years, type, area=None):
    
    path = "Data_TE/"
    if type == "ng":
        path += "NatGas_prices/ng_price_"+area+"_all.json"
    elif type == "el":
        path += "El_prices/"+area+"_all.json"
    elif type == "oil":
        path += "Oil_prices/Brent_crude_oil_25y.json"    
    elif type == "uranium":
        path += "Uranium_price/Uranium_10y.json"
    
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    
    dict = {}
    current_year = 0
    
    for year in years:
        dict[str(year)] = {"Q1": [],
                           "Q2": [],
                           "Q3": [],
                           "Q4": [],}
        current_year = year 
    
    for day in reversed(data):
        
        date = day["Date"]
        #day_date = int(date[:2])
        month_date = int(date[3:5])
        year_date = int(date[6:10])
        
        if year_date == current_year:
            dict[str(year_date)]["Q"+str(math.ceil(month_date/3))].append(day)
        elif str(year_date) in dict:
            current_year = year_date
            dict[str(year_date)]["Q"+str(math.ceil(month_date/3))].append(day)
                
    return dict


def Dict_to_list(dict):
    
    list = []
    
    for year in dict:
        for q in dict[year]:
            list += dict[year][q]
    
    return list


def Get_spesific_data(dict, type):
    
    ret_dict = {}
    
    for year in dict:
        ret_dict[year] = {}
        for q in dict[year]:
            ret_dict[year][q] = []
            
            for day in dict[year][q]:
                ret_dict[year][q].append(day[type])
                
                
    return ret_dict            
                
                
def fill_blank_data(dict, method="fill"):
    
    current_day = datetime.strptime("01/01/"+list(dict.keys())[0], "%d/%m/%Y")
    end_day = datetime.strptime("31/12/"+list(dict.keys())[-1], "%d/%m/%Y")
    delta = dt.timedelta(days=1)
    
    temp_dict = {}

    for year in dict:
        temp_dict[year] = {}
        for q in dict[year]:
            temp_dict[year][q] = []                
    
    while (current_day <= end_day):
        
        d= str(current_day)
        date = d[8:10]+"/"+d[5:7]+"/"+d[:4]
        month_date = int(date[3:5])
        q = "Q"+str(math.ceil(month_date/3))
        year = date[6:10]
        
        temp_dict[year][q].append({"Date": date})
        
        current_day += delta
            
    for year in temp_dict:
        for q in temp_dict[year]:
            i = 0
            for j in range(len(temp_dict[year][q])):
                
                date1 = temp_dict[year][q][j]["Date"]
                if i < len(dict[year][q]):
                    date2 = dict[year][q][i]["Date"]
                else:
                    date2 = ""
                    i = len(dict[year][q]) - 1
                
                if method == "fill":
                    temp_dict[year][q][j] = dict[year][q][i]
                    temp_dict[year][q][j]["Date"] = date1
                
                if date2 == date1:
                    temp_dict[year][q][j] = dict[year][q][i]
                    i+=1
                elif method == "mark":
                      temp_dict[year][q][j] = None
                         
    return temp_dict
    

def Make_dict_same_size(dict1, dict2, method = None):
    
    ret_dict1 = {}
    ret_dict2 = {}
    
    for year in dict1:
        if year in dict2:
            ret_dict1[year] = {}
            ret_dict2[year] = {}
            
            for q in dict1[year]: 
                if q in dict2[year]:
                    ret_dict1[year][q] = []
                    ret_dict2[year][q] = []
                    
                    for i in range(min(len(dict1[year][q]), len(dict2[year][q]))):
                        
                        ok, j = list_has_date(dict1[year][q][i]["Date"], dict2[year][q])
                        
                        if ok:
                            ret_dict1[year][q].append(dict1[year][q][i])
                            ret_dict2[year][q].append(dict2[year][q][j])
                            
    return ret_dict1, ret_dict2


def list_has_date(date, list):

    for i in range(len(list)):
        if list[i]["Date"] == date:
            return True, i

    return False, -1

def find_missing_days(dict):
    
    return



def Make_monthly_data(dict, type):
    
    ret_dict = {}

    for year in dict:
        ret_dict[year] = {}
        
        for q in dict[year]:
            ret_dict[year][q] = []
            month = dict[year][q][0]["Date"][3:5]
            
            start = 0
            for _ in range(3):
                 
                list = []
                for day in dict[year][q][start:]:
                    current_month = day["Date"][3:5]
                    
                    if current_month != month:
                        month=current_month
                        break                    
                    
                    list.append(day[type])
                    start+=1
                    
                list.sort()
                # this gives the median value.
                ret_dict[year][q].append(statistics.median(list))
                
    return ret_dict            
            
    
def Plot_corr_ng_el_for_period(area, years):
    
    
    
    x = np.array(list(map(str, years)))
    
    for country in area:
        
        corr_list = []

        for year in years:
            
            eu_ng_price = Get_TE_data([year], "ng", "eu")
            el_price = Get_TE_data([year], "el", country)
            
            eu_ng, el = Make_dict_same_size(eu_ng_price, el_price)

            ng = Dict_to_list(Get_spesific_data(eu_ng, "Close"))
            el = Dict_to_list(Get_spesific_data(el, "Close"))

            corr = Analysis.Corr(ng, el)
            
            corr_list.append(corr)
        
        y = np.array(corr_list)
        plt.plot(x, y, label=country)
    
    plt.title("Correlation between electricity price and TTS gas price")    
    plt.legend()
    plt.show()
    
    return None            


def Print_variance_of_prices(area, type, years, prices=None):
    
    if prices == None:
        prices = Get_spesific_data(Get_TE_data(years, type, area), "Closing")
    
    result = {}
    
    for area in prices:
        fstr = area+"| "
        result[area] = {}
        total_period = []

        for year in prices[area]:
            
            p_list = Dict_to_list(prices[area][year])
            total_period[area] += p_list
            variance = Analysis.Var(p_list)
            result[area][year] = variance
            
            vstr = "%.2f" % variance
            fstr += str(year)+": var "+ vstr + " | "
        
        total_period_var = Analysis.Var(total_period)
        fstr = "total: "+ "%.2f" % total_period_var + fstr
        result[area]["total"] = total_period_var
        
        print(fstr)         
        
    return result
            
def print_gas_and_el_volatility(area = ["germany", "france", "italy", "spain", "eu"], period = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]):
    
    
    for country in area:
        total = []
        fstr = ""
        sum = 0
        i=0
        for year in period:
            
            if country == "germany" and year == 2017:
                fstr += "2017: std       | "
                continue 
            
            i+=1
            
            type = "el"
            if country == "eu":
                type = "ng"
            
            p_list = Dict_to_list(Get_spesific_data(Get_TE_data([year], type, country), "Close"))
            total += p_list
            
            std = Analysis.Std(p_list)
            sum += std
            
            vstr = "%.1f" % std
            
            if std < 100:
                vstr = " " + vstr
            if std < 10:
                vstr = " " + vstr
            
            fstr += str(year)+": std " + vstr +" | "
            
            
        
        std = Analysis.Std(total)
        vstr = "%.1f" % std
        if std < 100:
            vstr = " " + vstr
        
        fstr = transelate_cc[country] + "| total: " + vstr +" | average: "+ "%.1f" % (sum/i) + " | "+ fstr
            
        print(fstr)        
    
    return
            
            
transelate_cc = {
    "germany": "DE",
    "italy":   "IT",
    "france":  "FR",
    "spain":   "ES",
    "eu":      "EU",
}                
                
            

###################### MAIN CODE #############################

period = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]


eu_ng_price = Get_TE_data(period, "ng", "eu")

#de_el_price = Get_TE_data([2018], "el", "germany")

#fr_el_price = Get_TE_data([2017], "el", "france")


#eu_ng, de_el = Make_dict_same_size(eu_ng_price, fr_el_price)


ng_eu = Dict_to_list(Get_spesific_data(eu_ng_price, "Close"))
#el = Dict_to_list(Get_spesific_data(de_el, "Close"))

#corr = Analysis.Corr(ng, el)

#print(corr)

area = ["germany", "france", "italy", "spain"]
#area = ["france", "italy", "spain"]

#Plot_corr_ng_el_for_period(area, period)

corrolations = {}

for country in area:
    corrolations[country] = {}
    corrolations[country]["avrage"] = 0
    sum = 0
    i = 0
    for year in period:
        
        if country == "germany" and year == 2017:
            #corrolations[country][year] = None
            continue
        i += 1
    
        eu_ng_price = Get_TE_data([year], "ng", "eu")

        el_price = Get_TE_data([year], "el", country)
        
        eu_ng, el = Make_dict_same_size(eu_ng_price, el_price)

        ng = Dict_to_list(Get_spesific_data(eu_ng, "Close"))
        el = Dict_to_list(Get_spesific_data(el, "Close"))

        corr = Analysis.Corr(ng, el)
        
        corrolations[country][year] = corr
        sum += corr
    
    corrolations[country]["avrage"] = sum/i

p_type = "G3000"

ng_production_data = Data_eurostat.Plot_relative_source_of_el_production(type=[p_type], start="2017-01", end="2025-01", area=["FR", "IT", "ES", "DE"], relativ_to="self", no_plot=True)

corr_list = []
ng_p_list = []
"""
for area in corrolations:
    fstr = transelate_cc[area]+"| "
    for year in corrolations[area]:
        if year == "avrage":
            fstr += str(year)+": corr  "+ "%.2f" % corrolations[area][year] + " | "
            continue
        elif corrolations[area][year] < 0:
            fstr += str(year)+": corr "+ "%.2f" % corrolations[area][year] + " | "
        else:
            fstr += str(year)+": corr  "+ "%.2f" % corrolations[area][year] + " | "
    
        corr_list.append(corrolations[area][year])
        ng_p_list.append(ng_production_data[transelate_cc[area]][str(year)])
    
    print(fstr)

print("Corrolation between relative el production from gas and the corr of gas and el prices(TE_data): "+ "%.2f" % Analysis.Corr(corr_list, ng_p_list))
"""

print("##############################################################################")

for area in corrolations:
    fstr = transelate_cc[area]+"| "
    p=0
    i=0
    
    
    for year in corrolations[area]:
        if year == "avrage":
            fstr += str(year)+": corr  "+ "%.2f" % corrolations[area][year] + " |"
            if area == "germany":
                fstr += "2017: corr       p       |"
            continue
        
        cstr = "%.2f" % corrolations[area][year]
        
        pstr = "%.2f" % ng_production_data[transelate_cc[area]][p_type][str(year)]
        if 0 <= corrolations[area][year] :        
            cstr = " " + cstr
        if 0 <= ng_production_data[transelate_cc[area]][p_type][str(year)]:
            pstr = " "+pstr

        fstr += str(year)+": corr "+ cstr +" p " + pstr + " |"
    
        if ng_production_data[transelate_cc[area]][p_type][str(year)] == 0:
            continue
    
        #corr_list.append(corrolations[area][year])
        #ng_p_list.append(ng_production_data[transelate_cc[area]][str(year)])
        
        p += ng_production_data[transelate_cc[area]][p_type][str(year)]
        i += 1
    
    if 0 < i:
        ng_p_list.append(p/i)
        corr_list.append(corrolations[area]["avrage"])
    
    print(fstr)
    
print("##############################################################################")

print_gas_and_el_volatility()

#print("Corrolation between relative el production from gas and the corr of gas and el prices(TE_data): "+ "%.2f" % Analysis.Corr(corr_list, ng_p_list))

    
#xpoints = np.array(list(map(str, period)))
#ypoints = np.array(ng_eu)

#plt.plot(ypoints, label = "NG closing prices")
#plt.legend(loc='upper left')
#plt.show()    


corrolations = {"oil": {}, "uranium": {}}

for src in corrolations:
    sum = 0
    i = 0
    ng_list = []
    src_list = []
    for year in period:
        
        i += 1
    
        eu_ng_price = Get_TE_data([year], "ng", "eu")

        src_price = Get_TE_data([year], src)
        
        eu_ng, src_price = Make_dict_same_size(eu_ng_price, src_price)

        ng = Dict_to_list(Get_spesific_data(eu_ng, "Close"))
        resrc = Dict_to_list(Get_spesific_data(src_price, "Close"))
        ng_list += ng
        src_list += resrc

        corr = Analysis.Corr(ng, resrc)
        
        corrolations[src][year] = corr
        sum += corr
    
    corrolations[src]["total"] = Analysis.Corr(ng_list, src_list)
    corrolations[src]["avrage"] = sum/i
    
    

print("############################## RESOURCE CORROLATIONS (WITH NAT GAS) ############################")
    
for year in corrolations["oil"]:
    
    fstr = ""
    for src in corrolations:
    
        corr = corrolations[src][year]
        cstr = "%.2f" % corrolations[src][year]
        if 0 <= corr :        
            cstr = " " + cstr
        
        fstr += src+" "+str(year)+": corr "+ cstr + " | "

    print(fstr)