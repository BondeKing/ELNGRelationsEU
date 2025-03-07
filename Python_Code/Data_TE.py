#source: https://tradingeconomics.com/commodity/eu-natural-gas
import json
import math
import Analysis

#TODO: Make code for handeling the data: Should be able to split into a dict of years and quarters as in entsoe.
# plot the data, and find staticial values for the data. Also find correlation between the gas for eu and el prices in germany, france, italy and spain.



def Get_TE_data(years, type, area):
    
    path = "Data_TE/"
    if type == "ng":
        path += "NatGas_prices/ng_price_"+area+"_all.json"
    elif type == "el":
        path += "El_prices/"+area+"_all.json"
    
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
    
    for day in data:
        
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


def dict_to_list(dict):
    
    list = []
    
    for year in dict:
        for q in dict[year]:
            list += dict[year][q]
    
    return list


def get_spesific_data(dict, type):
    
    for year in dict:
        for q in dict[year]:
            i = 0
            for day in dict[year][q]:
                dict[year][q][i] = day[type]
                i+=1
                
    return dict            
                
                
def fill_blank_data(dict, method):
    
    return
    

def make_dict_same_size(dict1, dict2, method = None):
    
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

###################### MAIN CODE #############################

eu_ng_price = Get_TE_data([2024], "ng", "eu")

de_el_price = Get_TE_data([2024], "el", "germany")

fr_el_price = Get_TE_data([2023,2024], "el", "france")


eu_ng, de_el = make_dict_same_size(eu_ng_price, de_el_price)



ng = dict_to_list(get_spesific_data(eu_ng, "Close"))
el = dict_to_list(get_spesific_data(de_el, "Close"))

print(len(ng))
print(len(el))

corr = Analysis.Corr(ng, el)

print(corr)