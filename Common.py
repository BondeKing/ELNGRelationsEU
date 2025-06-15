import Data_eurostat
import Data_entsoe
import Data_TE
import Analysis
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import pandas as pd
import Util
import seaborn as sns

def Make_TE_and_entsoe_dicts_same_size(entsoe_dict, TE_dict):
    
    
    ret_dict = {}
    for year in entsoe_dict:
        ret_dict[year] = {}
        for q in entsoe_dict[year]:
            ret_dict[year][q] = []
    
    if len(Data_TE.Dict_to_list(TE_dict)) < len(TE_dict)*365:
        temp_dict = Data_TE.fill_blank_data(TE_dict, method="mark")
        
        for year in TE_dict:
            for q in TE_dict[year]:
                len(entsoe_dict[year][q])
                for i in range(len(temp_dict[year][q])):
                    if temp_dict[year][q][i] != None:
                        ret_dict[year][q].append(entsoe_dict[year][q][i])
                
            
    return ret_dict            
                
        

def Plot_corrolation(TE_dict, Entsoe_dict, area):
    
    corr_list = []
    
    if len(TE_dict) == len(Entsoe_dict):
        for year in TE_dict:
            
            
            temp = {}
            temp[year] = TE_dict[year]
            list1 = Data_TE.Dict_to_list(temp)
            temp[year] = Entsoe_dict[year]
            list2 = Data_entsoe.dict_to_list(temp)
            
            
            
            corr_list.append(Analysis.Corr(list1, list2))
    
    xpoints = np.array(Data_entsoe.years)
    ypoints = np.array(corr_list)

    #plt.plot(xpoints, ypoints, label=area)
    #plt.show()
    
    return corr_list

def Find_total_corrolations_one_to_many(one_dict, many_dicts):
    
    corrolations = {}
    
    for area in many_dicts:
        
        dict = Make_TE_and_entsoe_dicts_same_size(many_dicts[area], one_dict)
        ng_price_list = Data_TE.Dict_to_list(Data_TE.Get_spesific_data(one_dict, "Close"))
        el_price_list = Data_entsoe.dict_to_list(dict)
        
        corrolations[area] = Analysis.Corr(ng_price_list, el_price_list)
        
    return corrolations    
    


def Plot_and_find_corrolations_one_to_many(one_dict, many_dicts):
    
    corrolations = {}
    
    
    for area in many_dicts:
        corrolations[area] = {}
        corrolations[area]["avrage"] = None
        for year in one_dict:
            corrolations[area][year] = None
            
    
    for area in many_dicts:
        
        dict = Make_TE_and_entsoe_dicts_same_size(many_dicts[area], one_dict)
        cloasing_one_dict = Data_TE.Get_spesific_data(one_dict, "Close")
        corrolation_list = Plot_corrolation(cloasing_one_dict, dict, area)
        sum = 0
        i = 0
        for year in one_dict:
            if i < len(corrolations[area]):
                sum += corrolation_list[i]
                corrolations[area][year] = corrolation_list[i]                
            i+=1
        corrolations[area]["avrage"] = sum/len(corrolation_list)
    
    
    return corrolations
    
def sort_and_print_d_list(d_list):
    
    sorted_list = []
    sorted_list.append(d_list[0])
    
    for d_point in d_list[1:]:
        for i in range(len(sorted_list)):
            if sorted_list[i]["corr"] < d_point["corr"]:
                if i == 0:
                    sorted_list = [d_point] + sorted_list
                else:
                    sorted_list = sorted_list[:i] + [d_point] + sorted_list[i:]
                break
            elif i == len(sorted_list)-1:
                sorted_list.append(d_point)
                
    for d_point in sorted_list:
        print(d_point["str"])        

    return    

period = ["2024", "2023", "2022", "2021", "2020", "2019","2018","2017"]

#period = ["2019"]

ng_price = Data_TE.Get_TE_data(period, "ng", "eu")

ng_monthly = Data_TE.Make_monthly_data(ng_price, "Close")

#ng_cloasing = Data_TE.Get_spesific_data(ng_monthly, "Close")


ng_relative_el_production =  Data_eurostat.Get_data_for_period(Data_eurostat.Get_relativ_el_production_data("DE"), period)


ng_price_list = Data_TE.Dict_to_list(ng_monthly)
ng_production_list = ng_relative_el_production.values.flatten().tolist()


corr = Analysis.Corr(ng_price_list, ng_production_list)
#print(corr)

'''
corr_list = []

for year in period:
    
    print("hello")
    ng_price = Data_TE.Get_TE_data([year], "ng", "eu")
    ng_monthly = Data_TE.Make_monthly_data(ng_price, "Close")
    
    ng_relative_el_production =  Data_eurostat.Get_data_for_period(Data_eurostat.Get_relativ_el_production_data("DE"), [year])
    ng_price_list = Data_TE.Dict_to_list(ng_monthly)
    ng_production_list = ng_relative_el_production.values.flatten().tolist()

    corr = Analysis.Corr(ng_price_list, ng_production_list)
    
    corr_list.append(corr)

xpoints = np.array(period)
ypoints = np.array(corr_list)

plt.plot(xpoints, ypoints)
plt.show()    
''' 

# Find el and ng price correlation for norway, sweden, poland and the netherlands. Have to use el price data from entsoe for this.

period = Data_entsoe.years

TE_ng_price_eu = Data_TE.Get_TE_data(period, "ng", "eu")
entsoe_daily_el_price_nl = Data_entsoe.daily_cloasing_price_NL


el_price_nl = Make_TE_and_entsoe_dicts_same_size(entsoe_daily_el_price_nl, TE_ng_price_eu)
ng_price_eu = Data_TE.Get_spesific_data(TE_ng_price_eu,"Close")


p_type = "G3000"

corrolations = Plot_and_find_corrolations_one_to_many(Data_TE.Get_TE_data(period, "ng", "eu"), Data_entsoe.daily_cloasing_prices)
corrolations_oil = Plot_and_find_corrolations_one_to_many(Data_TE.Get_TE_data(period, "oil"), Data_entsoe.daily_cloasing_prices)
corrolations_uranium = Plot_and_find_corrolations_one_to_many(Data_TE.Get_TE_data(period, "uranium"), Data_entsoe.daily_cloasing_prices)

#ng_production_data = Data_eurostat.Plot_relative_source_of_el_production(type=[p_type], start="2017-01", end="2025-01", area=Data_entsoe.area+["DE"], relativ_to="self", no_plot=True)
ng_production_data = Data_eurostat.get_gas_production_data(Data_entsoe.area+["DE"])
total_period_corrolations = Find_total_corrolations_one_to_many(Data_TE.Get_TE_data(period, "ng", "eu"), Data_entsoe.daily_cloasing_prices)
corrolations_17to20 = Find_total_corrolations_one_to_many(Data_TE.Get_TE_data(period[:4], "ng", "eu"), Data_entsoe.daily_cloasing_prices)
corrolations_21to24 = Find_total_corrolations_one_to_many(Data_TE.Get_TE_data(period[4:], "ng", "eu"), Data_entsoe.daily_cloasing_prices)
"""
corr_list = []
ng_p_list = []

#print("#####################################################################")
for area in ["FR", "IT", "ES"]:
    fstr = area+"| "
    p = 0
    i= 0
    for year in corrolations[area]:
        if year == "avrage":
            fstr += year+": corr  "+ "%.2f" % corrolations[area][year] + " |"
            continue
        
        cstr = "%.2f" % corrolations[area][year]
        if 0 <= corrolations[area][year] :        
            cstr = " " + cstr

        fstr += year+": corr "+ cstr + " | "
        
        if ng_production_data[area][p_type][year] == 0:
            continue
    
        #corr_list.append(corrolations[area][year])
        #ng_p_list.append(ng_production_data[area][year])
        
        p += ng_production_data[area][p_type][year]
        i += 1
    
    if 0 < i:
        ng_p_list.append(p/i)
        corr_list.append(corrolations[area]["avrage"])
    
    #print(fstr)

#print("Corrolation between relative el production from gas and the corr of gas and el prices: "+ "%.2f" % Analysis.Corr(corr_list, ng_p_list))
"""

corr_avrages = {}
corr_avrages["avrage"] = 0
for area in corrolations:
    for year in corrolations[area]:
        corr_avrages[year] = 0
        
tavg1 = 0
tavg2 = 0
tavg3 = 0        

corr_list = []
ng_p_list = []
i_e_list = []
import_export = Data_eurostat.trade_exposure
d_list = []
d_list_p = []

print("############################ EL- GAS PRICE CORRELATIONS ###################################")
for area in corrolations:
    tstr = area+"| total: " + "%.2f" % total_period_corrolations[area]
    tstr = tstr + "| 2017-2020: " + "%.2f" % corrolations_17to20[area]
    tstr = tstr + "| 2021-2024: " + "%.2f" % corrolations_21to24[area]
    tavg1 += total_period_corrolations[area]
    tavg2 += corrolations_17to20[area]
    tavg3 += corrolations_21to24[area]
    
    fstr = area+"| "
    fstr_p = ""
    p=0
    i=0
    d_point = {"corr": [], "p": [], "str":[], "area": area}
    d_point_p = Util.make_new_d_point(area=area)
    sum_p = 0
    
    for year in corrolations[area]:
        
        corr_avrages[year] += corrolations[area][year]
        
        if year == "avrage":
            fstr += year+":corr  "+ "%.2f" % corrolations[area][year] + "|"
            d_point["corr"] = corrolations[area][year]
            corr_list.append(corrolations[area][year])
            continue
        
        cstr = "%.2f" % corrolations[area][year]
        pstr = "%.2f" % ng_production_data[area][p_type][year]
        if 0 <= corrolations[area][year] :        
            cstr = " " + cstr
        if 0 <= ng_production_data[area][p_type][year]:
            pstr = " "+pstr

        fstr += year+": corr "+ cstr +" p " + pstr + " |"
        fstr_p += year+": el-ng p "+ pstr + " | "
        

        sum_p += ng_production_data[area][p_type][year]
        
        
        p += ng_production_data[area][p_type][year]
        i += 1
    
    d_point["str"] = fstr
    d_list.append(d_point)
    
    p_avg = sum_p/len(ng_production_data[area][p_type])
    fstr_p = area+"| avrage: "+ "%.2f" % p_avg +" | "+ fstr_p
    d_point_p["str"] = fstr_p
    d_point_p["data"] = p_avg
    d_list_p.append(d_point_p)
    
    ng_p_list.append(p_avg)
    
    print(tstr)

tstr = "AVG total: " + "%.2f" % (tavg1/len(corrolations)) + "| 2017-2020: "  + "%.2f" % (tavg2/len(corrolations)) + "| 2021-2024: "  + "%.2f" % (tavg3/len(corrolations))
print(tstr)

print("############################################################################")

sort_and_print_d_list(d_list)

fstr = "AVG"
for col in corr_avrages:
        
        corr = corr_avrages[col]/len(corrolations)
        vstr = "%.2f" % corr
        
        
        
        if col == "avrage":  
            fstr += " "+col+": "+vstr+" |"
        else:
            if corr > 0 :
                vstr = " " + vstr
            fstr += " "+col+": corr "+vstr+" |"    
print(fstr)

print("#############################################################################")
Util.sort_and_print_d_list(d_list_p)
      
   
print("Corrolation between relative el production from gas and the corr of gas and el prices: "+ "%.2f" % Analysis.Corr(corr_list, ng_p_list))
#print("%.2f" % Analysis.Corr(corr_list, i_e_list))

"""
for country in ["spain", "france", "italy"]:
    TE_dict = Data_TE.Get_TE_data(period, "el", country)
    entsoe_dict = Make_TE_and_entsoe_dicts_same_size(Data_entsoe.daily_cloasing_prices[Data_TE.transelate_cc[country]], TE_dict) 
    plt.plot(np.array(Data_entsoe.dict_to_list(entsoe_dict)), label="entsoe")
    plt.plot(np.array(Data_TE.Dict_to_list(Data_TE.Get_spesific_data(TE_dict,"Close"))), label="TE")
    plt.legend(loc='upper left')
    plt.title(country.capitalize() + " el closing prices")
    plt.show()
"""

data = {}
col = []
el_prices = Data_entsoe.daily_cloasing_prices

for area in el_prices:
    col.append(area)
    list = Data_entsoe.dict_to_list(el_prices[area])
    if len(list) < 2922:
        diff = 2922-len(list)
        list = list + list[len(list)-diff:]
    elif 2922 < len(list):
        list = list[:2922]
    
    data[area] = list
    
corr_matrix = pd.DataFrame(data=data, columns=col).corr()
print(corr_matrix)

heatmap = sns.heatmap(corr_matrix, vmin=-1, vmax=1, annot=True)
heatmap.set_title('Correlation Heatmap Of Electricity Prices')

plt.show()




corr_avrages = {}
corr_avrages["avrage"] = 0
for area in corrolations_oil:
    for year in corrolations_oil[area]:
        corr_avrages[year] = 0
      

d_list = []


print("############################ OIL- GAS PRICE CORRELATIONS ###################################")
for area in corrolations_oil:
    
    fstr = area+"| "

    d_point = Util.make_new_d_point(area=area)
    sum_p = 0
    
    for year in corrolations_oil[area]:
        
        corr_avrages[year] += corrolations_oil[area][year]
        
        if year == "avrage":
            fstr += year+":corr  "+ "%.2f" % corrolations_oil[area][year] + "|"
            d_point["data"] = corrolations_oil[area][year]
            continue
        
        cstr = "%.2f" % corrolations_oil[area][year]
        if 0 <= corrolations_oil[area][year] :        
            cstr = " " + cstr

        fstr += year+": corr "+ cstr + " |"
        
    d_point["str"] = fstr
    d_list.append(d_point)    
    
Util.sort_and_print_d_list(d_list)

fstr = "AVG"
for col in corr_avrages:
        
        corr = corr_avrages[col]/len(corrolations_oil)
        vstr = "%.2f" % corr
        
        
        
        if col == "avrage":  
            fstr += " "+col+": "+vstr+" |"
        else:
            if corr > 0 :
                vstr = " " + vstr
            fstr += " "+col+": corr "+vstr+" |"    
print(fstr)




corr_avrages = {}
corr_avrages["avrage"] = 0
for area in corrolations_uranium:
    for year in corrolations_uranium[area]:
        corr_avrages[year] = 0
      

d_list = []


print("############################ URANIUM- GAS PRICE CORRELATIONS ###################################")
for area in corrolations_uranium:
    
    fstr = area+"| "

    d_point = Util.make_new_d_point(area=area)
    sum_p = 0
    
    for year in corrolations_uranium[area]:
        
        corr_avrages[year] += corrolations_uranium[area][year]
        
        if year == "avrage":
            fstr += year+":corr  "+ "%.2f" % corrolations_uranium[area][year] + "|"
            d_point["data"] = corrolations_uranium[area][year]
            continue
        
        cstr = "%.2f" % corrolations_uranium[area][year]
        if 0 <= corrolations_uranium[area][year] :        
            cstr = " " + cstr

        fstr += year+": corr "+ cstr + " |"
        
    d_point["str"] = fstr
    d_list.append(d_point)    
    
Util.sort_and_print_d_list(d_list)

fstr = "AVG"
for col in corr_avrages:
        
        corr = corr_avrages[col]/len(corrolations_uranium)
        vstr = "%.2f" % corr
        
        
        
        if col == "avrage":  
            fstr += " "+col+": "+vstr+" |"
        else:
            if corr > 0 :
                vstr = " " + vstr
            fstr += " "+col+": corr "+vstr+" |"    
print(fstr)