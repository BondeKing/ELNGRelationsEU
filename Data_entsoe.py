#Source: https://newtransparency.entsoe.eu/market/energyPrices

import requests
import xmltodict
import os
import matplotlib.pyplot as plt
import numpy as np
import Analysis
import Util

#NOTE: Entsoe only tracks data in regards to electrisity production, transmissions and consumption. Gas data for entsoe is only realated to power production.
# Energy prices are in entsoe is only provided as "day-ahead" prices. 


# the xml file is parsed into a dict (like a JSON file) and you have to search for elements in it like a nested dict. (look at the xml file to see how to search for particular data)
# Itterate over the list after "TimeSeries" to get the days, and itterate after "Point" to get the houres.

def make_data_request(period_start, period_end, domain, doc_type="A44", contract_MarketAgreement_type="A01", process_type="A16", security_token="aa7c1479-9351-4afe-895f-315870625a61"):
    
    payload = {}
    headers = {}
    url = "https://web-api.tp.entsoe.eu/api?"
    
    if doc_type == "A44":
        payload={"documentType": doc_type, "periodStart": period_start, "periodEnd": period_end, "out_Domain":domain, "in_Domain": domain, "securityToken": security_token}
    elif doc_type == "A65":
        payload={"documentType": doc_type, "processType": process_type, "periodStart": period_start, "periodEnd": period_end, "outBiddingZone_Domain":domain, "securityToken": security_token}
    
    respons = requests.request("GET", url, headers=headers, params=payload).text
    
    
    return respons

Area_names = ["EE",
    "SE1",
    "SE2",
    "SE3",
    "SE4",
    "NO5",
    "SEM",
    "IT-GR",
    "IT-NORTH_SI",
    "IT-NORTH_CH",
    "IT-CENTRE_NORTH",
    "IT-CENTRE_SOUTH",
    "IT-NORTH",
    "IT-SARDINIA",
    "IT-SICILY",
    "IT-SOUTH",
    "IT-NORTH_AT",
    "IT-NORTH_FR",
    "DE_LU",
    "IT-MT",
    "IT-SACO_AC",
    "IT-SACODC",
    "IT-MONFALCONE",
    "ICELAND",
    "MOLDOVA",
    "UA-IPS",
    "AL",
    "AT",
    "BA",
    "BE",
    "BG",
    "CH",
    "ME",
    "RS",
    "CY",
    "CZ",
    "DK1",
    "DK2",
    "ES",
    "FI",
    "FR",
    "GB",
    "GR",
    "HR",
    "HU",
    "LT",
    "LV",
    "MK",
    "NL",
    "NO1",
    "NO2",
    "NO3",
    "NO4",
    "PL",
    "PT",
    "RO",
    "SI",
    "SK"]
    
Bidding_zones = {
    "EE": "10Y1001A1001A39I",
    "SE1": "10Y1001A1001A44P",
    "SE2": "10Y1001A1001A45N",
    "SE3": "10Y1001A1001A46L",
    "SE4": "10Y1001A1001A47J",
    "NO5": "10Y1001A1001A48H",
    "DE_AT_LU": "10Y1001A1001A63L",
    "KALININGRAD_AREA": "10Y1001A1001A50U",
    "BELARUS_AREA": "10Y1001A1001A51S",
    "LT_BEL_IMP_AREA": "10Y1001A1001A55K",
    "LT_BEL_EXP_AREA": "10Y1001A1001A56I",
    "GB_N2EX_PRICZONE": "10Y1001A1001A57G",
    "GB_APX_PRICEZONE": "10Y1001A1001A58E",
    "SEM": "10Y1001A1001A59C",
    "IT-GR": "10Y1001A1001A66F",
    "IT-NORTH_SI": "10Y1001A1001A67D",
    "IT-NORTH_CH": "10Y1001A1001A68B",
    "IT-CENTRE_NORTH": "10Y1001A1001A70O",
    "IT-CENTRE_SOUTH": "10Y1001A1001A71M",
    "IT-NORTH": "10Y1001A1001A73I",
    "IT-SARDINIA": "10Y1001A1001A74G",
    "IT-SICILY": "10Y1001A1001A75E",
    "IT-SOUTH": "10Y1001A1001A788",
    "IT-NORTH_AT": "10Y1001A1001A80L",
    "IT-NORTH_FR": "10Y1001A1001A81J",
    "DE_LU": "10Y1001A1001A82H",
    "IT-MT": "10Y1001A1001A877",
    "IT-SACO_AC": "10Y1001A1001A885",
    "IT-SACODC": "10Y1001A1001A893",
    "IT-MONFALCONE": "10Y1001A1001A90I",
    "ICELAND": "10Y1001A1001A958",
    "MOLDOVA": "10Y1001A1001A990",
    "UA-IPS": "10Y1001C--000182",
    "IT-MONTENEGRO": "10Y1001C--000611",
    "IT-CALABRIA": "10Y1001C--00096J", 	#Italy Calabria				Bidding Zone,Scheduling Area
    "FR_UK_IFA_BZN": "10Y1001C--00098F",		#IFA Bidding Zone		10XFR-RTE------Q		Bidding Zone
    "CAKOSTT": "10Y1001C--00100H",		#Control Area Kosovo*				Bidding Zone,Control Area
    "NO_FICT_AREA_2A": "10Y1001C--001219",		#Norwegian Fictitious Area 2A				Bidding Zone
    "NORDIC_SYNC_AREA": "10Y1001C--00146U",	#Nordic Synchronous Area				Bidding Zone,Synchronous Area
    "SE3A": "10Y1001C--00148Q",		#Swedish Fictitious Area SE3A				Bidding Zone
    "AL": "10YAL-KESH-----5",		#Albania				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "AT": "10YAT-APG------L",		#Austria				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "BA": "10YBA-JPCC-----D",		#Bosnia and Herzegovina				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "BE": "10YBE----------2",		#Belgium				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "BG": "10YCA-BULGARIA-R",		#Bulgaria				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area,Control Block
    "CH": "10YCH-SWISSGRIDZ",		#Switzerland				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "ME": "10YCS-CG-TSO---S",		#Montenegro		10XCS-CG-TSO---5		Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "RS": "10YCS-SERBIATSOV",		#Serbia				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "CY": "10YCY-1001A0003J",		#Cyprus				Bidding Zone,Control Area,Member State,Scheduling Area
    "CZ": "10YCZ-CEPS-----N",		#Czech Republic				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "DK1": "10YDK-1--------W",		#Denmark DK1		10X1001A1001A248		Bidding Zone,LFC Area,Scheduling Area
    "DK2": "10YDK-2--------M",		#Denmark DK2		10X1001A1001A248		Bidding Zone,LFC Area,Scheduling Area
    "ES": "10YES-REE------0",		#Spain		10XES-REE------E		Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "FI": "10YFI-1--------U",		#Finland				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "FR": "10YFR-RTE------C",		#France				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area,Control Block
    "GB": "10YGB----------A",		#Great Britain				Bidding Zone,Control Area,LFC Area,LFC Block,Scheduling Area,Synchronous Area
    "GR": "10YGR-HTSO-----Y",		#Greece				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "HR": "10YHR-HEP------M",		#Croatia				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "HU": "10YHU-MAVIR----U",		#Hungary				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "LT": "10YLT-1001A0008Q",		#Lithuania				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "LV": "10YLV-1001A00074",		#Latvia				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "MK": "10YMK-MEPSO----8",		#FYROM				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "NL": "10YNL----------L",		#Netherlands				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "NO1": "10YNO-1--------2",		#Norwegian Area Elspot Area 1				Bidding Zone,Scheduling Area
    "NO2": "10YNO-2--------T",		#Norwegian Area Elspot Area 2				Bidding Zone,Scheduling Area
    "NO3": "10YNO-3--------J",		#Norwegian Area Elspot Area 3				Bidding Zone,Scheduling Area
    "NO4": "10YNO-4--------9",		#Norwegian Area Elspot Area 4				Bidding Zone,Scheduling Area
    "PL": "10YPL-AREA-----S",		#Poland				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "PT": "10YPT-REN------W",		#Portugal		10XPT-REN------9		Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "RO": "10YRO-TEL------P",		#Romania				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "SI": "10YSI-ELES-----O",		#Slovenia				Bidding Zone,Control Area,LFC Area,Member State,Scheduling Area
    "SK": "10YSK-SEPS-----K",		#Slovak Republic				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "TEIAS_AREA": "10YTR-TEIAS----W",		#TEIAS Area				Bidding Zone,Control Area,LFC Area,LFC Block,Member State,Scheduling Area
    "UA-BEI": "10YUA-WEPS-----0",		#Ukrainian Area of Burshtyn island		10X1001C--00001X		Bidding Zone,LFC Area,Scheduling Area
    "AT-EXAAMC": "14Y----0000041-W",		#Virtual Bidding Zone EXAA		13X----EXAA----G		Bidding Zone,Market Area
    "CCPACCP1": "14YCCPADATENMLDW",		#CCP Austria GmbH				Balance Group,Bidding Zone,Market Area
    "EXAACCP": "14YEXAADATENMLDU",	 #EXAA Abwicklungsstelle für Energieprodukte AG				Balance Group,Bidding Zone,Market Area
    "FR_UK_IFA2000_1": "17Y000000930808E",		#vhub_UK_IFA2000_link1		10XFR-RTE------Q		Bidding Zone
    "FR_FR_IFA2000_1": "17Y000000930809C",		#vhub_FR_IFA2000_link1		10XFR-RTE------Q		Bidding Zone
    "FR_UK_IFA2000_2": "17Y000000930810R",		#vhub_UK_IFA2000_link2		10XFR-RTE------Q		Bidding Zone
    "FR_FR_IFA2000_2": "17Y000000930811P",		#vhub_FR_IFA2000_link2		10XFR-RTE------Q		Bidding Zone
    "FR_UK_IFA2": "17Y000000930814J",		#vhub_UK_IFA2		10XFR-RTE------Q		Bidding Zone
    "FR_FR_IFA2": "17Y000000930815H",		#vhub_FR_IFA2		10XFR-RTE------Q		Bidding Zone
    "FR_IT_SAV_PIE": "17Y000000930816F",		#vhub_IT_Savoie_Piemont		10XFR-RTE------Q		Bidding Zone
    "FR_FR_SAV_PIE": "17Y000000930817D",		#vhub_FR_Savoie_Piemont		10XFR-RTE------Q		Bidding Zone
    "FR_UK_IFA2_V_BZN": "17Y0000009369493",		#IFA2_virtual_BZN		10XFR-RTE------Q		Bidding Zone,Border Area
    "PEGNORDB": "21Y000000000001U",		#Point Exchange Gas - NORD B		21X-FR-A-A0A0A-S		Bidding Zone
    "VOB-CZ": "21Y---A001A001-B",		#Virtual Trading Point RWE Transgas Net		21X000000001304L		Bidding Zone,Market Area,Metering Grid Area
    "PEGNORD": "21YPNT-EX-GAS-NT",		#Point Exchange Gas - NORD		21X-FR-A-A0A0A-S		Bidding Zone
    "PEGSUD": "21YPNT-EX-GAS-SJ",		#Point Exchange Gas - SUD		21X-FR-A-A0A0A-S		Bidding Zone
    "FI_FS": "44Y-00000000160K",		#Fingrid Oyj		10X1001A1001A264		Bidding Zone
    "FI_EL": "44Y-00000000161I",		#Fingrid Oyj		10X1001A1001A264		Bidding Zone
    "DKW-NO2": "45Y000000000001C",		#DKW-NO2 virtual Bidding Zone Border				Bidding Zone,Border Area
    "DKW-SE3": "45Y000000000002A",		#DKW-SE3 virtual Bidding Zone Border				Bidding Zone,Border Area
    "DKW-DKE": "45Y0000000000038",		#DKW-DKE virtual Bidding Zone Border				Bidding Zone,Border Area
    "SE3_FS": "46Y000000000001Y",		#SE3_FS (SE3, Fennoskan)				Bidding Zone
    "SE3_KS": "46Y000000000002W",		#SE3_KS (SE3, Kontiskan)				Bidding Zone
    "SE4_SP": "46Y000000000003U",		#SE4_SP (SE4, Swepol link)				Bidding Zone
    "SE4_NB": "46Y000000000004S",		#SE4_NB (SE4, Nordbalt)				Bidding Zone
    "SE4_BC": "46Y000000000005Q",		#SE4_BC (SE4, Baltic Cable)				Bidding Zone
    "CUT_AREA_SE3LS": "46Y000000000007M",		#Cut area SE3LS				Bidding Zone
    "CUT_AREA_SE3": "46Y000000000008K",		#Cut area SE3				Bidding Zone
    "CUTCOR_SE3LS-SE3": "46Y000000000009I",		#Cut corridor SE3LS-SE3				Bidding Zone
    "VBZ_SE3-SE4_ACSW": "46Y000000000015N",		#Virtual bidding zone border SE3-SE4 AC+SWL				Bidding Zone
    "VBZ_SE4-SE3_ACSW": "46Y000000000016L",	#Virtual bidding zone border SE4-SE3 AC+SWL				Bidding Zone
    "SE3_SWL": "46Y000000000017J",		#SE3_SWL (SE3, Sydvastlanken)				Bidding Zone
    "SE4_SWL": "46Y000000000018H",		#SE4_SWL (SE4, Sydvastlanken)				Bidding Zone
    "CUTCOR_SE3A-SE3": "46Y000000000019F",		#Cut corridor SE3A-SE3				Bidding Zone
    "NO_NO2NSL": "50Y0JVU59B4JWQCU",		#Virtual Bidding Zone NO2NSL		10X1001A1001A38Y		Bidding Zone
    "NO_NO2_NL": "50Y73EMZ34CQL9AJ",		#Virtual Bidding Zone NO2-NL		10X1001A1001A38Y		Bidding Zone
    "NO_NO2_DK1": "50YCUY85S1HH29EK",		#Virtual Bidding Zone NO2-DK1		10X1001A1001A38Y		Bidding Zone
    "NO_NO2-GB": "50Y-HTS3792HUOAC",		#Virtual bidding Zone NO2-GB		10X1001A1001A38Y		Bidding Zone
    "NO_NO2-DE": "50YNBFFTWZRAHA3P",		#Virtual bidding Zone NO2-DE  		10X1001A1001A38Y		Bidding Zone
    "VISKOL2003": "67Y-VISKOL-2003T",		#VISKOL DOO NOVI SAD SRBIJA		67X-RS-00000003H		Bidding Zone,ITC,Local Market Area,Market Area
    "TTN-VBZ_DK1": "49Y000000000003M",		#TTN-DK1 Virtual Bidding Zone on TTN Side		10X1001A1001A361		Bidding Zone
    "TTN-VBZ_NO2": "49Y000000000004K",
} 

def reverse_lookup(d, value):
    keys = []
    for key, val in d.items():
        if val == value:
            keys.append(key)
    return keys   



def daily_cloasing(years, area):
    
    respons = {}
    
    for year in years:
        path = "Data_entsoe/Price_data/"+area+"/"+year+"/"
        respons[year] = {}
        for q in os.listdir(path):
            
            respons[year][q] = []
            price_data = open(os.path.join(path, q), "r")
            dict = xmltodict.parse(price_data.read())
            price_data.close()
        
            if dict["Publication_MarketDocument"]["TimeSeries"][0]["currency_Unit.name"] != "EUR":
                    print(area)
                    print(year)
                    print(q)
                    print(dict["Publication_MarketDocument"]["TimeSeries"][0]["currency_Unit.name"])
        
            i = 0
            for day in dict["Publication_MarketDocument"]["TimeSeries"]:
            
                
                    
                if i+1 == len(dict["Publication_MarketDocument"]["TimeSeries"]):
                    break
                
                    
                if not isinstance(day["Period"]["Point"], list):
                    print(area)
                    print(year)
                    print(q)
                    print(day["Period"]["Point"]) 
                    print("not list")
                    continue
                    
                respons[year][q].append(float(day["Period"]["Point"][-1]["price.amount"]))
            
                i+=1
                        
    return respons


def daily_cloasing_several_areas(years, areas, agregate = False):
    
    response = {}
    
    for area in areas:
        response[area] = daily_cloasing(years, area)
    
    if agregate:
        agregate_name = areas[0][:2]
        response2 = {agregate_name: {}}
        first_run = True
        
        for area in response:
            for year in response[area]:
                
                if first_run:
                    response2[agregate_name][year] = {}
                for q in response[area][year]:
                    
                    if first_run:
                        response2[agregate_name][year][q] = []
                    for i in range(len(response[area][year][q])):
                        
                        # if any agregated area should be weighted, this is where to add in the weights.
                        if first_run or len(response2[agregate_name][year][q]) <= i:
                            response2[agregate_name][year][q].append(response[area][year][q][i])
                        else:
                            response2[agregate_name][year][q][i] += response[area][year][q][i]
                            
            first_run = False    
        
        for year in response2[agregate_name]:
            for q in response2[agregate_name][year]:
                for i in range(len(response2[agregate_name][year][q])):
                    response2[agregate_name][year][q][i] = response2[agregate_name][year][q][i]/len(areas)
        
        return response2
    
    return response


def daily_avrage(dict):

    result = []
    
    for day in dict["Publication_MarketDocument"]["TimeSeries"]:
        
        tot = 0
        amt = 0
        
        for price in day["Period"]["Point"]:
            tot += float(price["price.amount"])
            amt += 1
        
        if amt != 0:
            result.append(tot/amt)
    
    return result        

        
def monthly_avrage(dict):
    
    result = []
    monthly_tot = 0
    monthly_amt = 0
    current_month = dict["Publication_MarketDocument"]["TimeSeries"][0]["Period"]["timeInterval"]["end"][5:7]
    
    for day in dict["Publication_MarketDocument"]["TimeSeries"]:
        
        daily_tot = 0
        daily_amt = 0
        
        for price in day["Period"]["Point"]:
            daily_tot += float(price["price.amount"])
            daily_amt += 1
        
        if daily_amt != 0:
            monthly_tot += daily_tot/daily_amt
            monthly_amt += 1 
            
        month = int(day["Period"]["timeInterval"]["end"][5:7])
        
        if current_month != month:
            current_month = month
            if monthly_amt != 0:
                result.append(monthly_tot/monthly_amt)
                monthly_tot = 0
                monthly_amt = 0
                
    return result

def flush_data():
    
    for file in os.listdir("Data_entsoe"):
        f = os.path.join("Data_entsoe",file)
        os.remove(f)


def request_data_for_year(year, domain, doc_type = "A44", zones=Bidding_zones):
    
    q1 = make_data_request(year+"01010000",year+"04010000",domain, doc_type)
    q2 = make_data_request(year+"04010000",year+"07010000",domain, doc_type)    
    q3 = make_data_request(year+"07010000",year+"10010000",domain, doc_type)
    q4 = make_data_request(year+"10010000", str(int(year)+1)+"01010000", domain, doc_type)
    quarters = [q1, q2, q3, q4]
    
    if doc_type == "A44":
        path = "Data_entsoe/Price_data/"+reverse_lookup(zones, domain)[0]+"/"+year
    else:
        path = "Data_entsoe/Load_data/"+reverse_lookup(zones, domain)[0]+"/"+year
    
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(4):
        f = open(path+"/Q"+str(i+1), "w")
        f.write(quarters[i])
        f.close()
        
    return quarters    


# yeras should be a list of years in text that you want to retrive data from.
# biddingzones is a list of countries and area you want to retrive data from.
def request_data_in_biddingzone(years, country_area, zones=Bidding_zones, data_type="A44"):
    
    respons = {}
    
    for area in country_area:
        domain = zones[area]
        quarter_list = []
        print(area)
        for year in years:
            print(year)
            quarter_list.append(request_data_for_year(year,domain, doc_type=data_type))
        #respons[area] = quarter_list
        
        
    return respons                    
    

def bougth_amount(years, area):
    
    stub_load_data = "Data_entsoe/Load_data/"+area+"/"
    stub_price_data = "Data_entsoe/Price_data/"+area+"/"
    loads = {}
    prices = {}
    bought_amount = {}
    bought_amount_hourly = {}
    bought_amount_daily = {}
    bought_amount_weekly = {}
    #bought_amount_monthly = {}
    bought_amount_qurterly = {}
    bought_amount_yearly = {}
    
    for year in years:
        dir_load_data = stub_load_data+year
        dir_price_data = stub_price_data+year
        loads[year] = {}
        prices[year] = {}
        bought_amount[year] = {}
        bought_amount_hourly[year] = {}
        bought_amount_daily[year] = {}
        bought_amount_weekly[year] = {}
        #bought_amount_monthly[year] = {}
        bought_amount_qurterly[year] = {}
        bought_amount_yearly[year] = []
        
        year_amount = 0
        
        for q in os.listdir(dir_load_data):
             
            bought_amount[year][q] = []
            bought_amount_hourly[year][q] = []
            bought_amount_daily[year][q] = []
            bought_amount_weekly[year][q] = []
            bought_amount_qurterly[year][q] = 0
            
            quarter_amount = 0
            
            loads[year][q] = [] 
            load_data = open(os.path.join(dir_load_data, q), "r")
            load_dict = xmltodict.parse(load_data.read())
            load_data.close()
            retard_format = isinstance(load_dict["GL_MarketDocument"]["TimeSeries"], list)
            if retard_format:
                load_resolution = 60/int(load_dict["GL_MarketDocument"]["TimeSeries"][0]["Period"]["resolution"][2:4])
            else:
                load_resolution = 60/int(load_dict["GL_MarketDocument"]["TimeSeries"]["Period"]["resolution"][2:4])
            
            prices[year][q] = []
            price_data = open(os.path.join(dir_price_data, q), "r")
            price_dict = xmltodict.parse(price_data.read())
            price_data.close()
            price_resolution = 60/int(price_dict["Publication_MarketDocument"]["TimeSeries"][0]["Period"]["resolution"][2:4])
            

            for day in price_dict["Publication_MarketDocument"]["TimeSeries"]:
                i=1
                pos = 0
                prev_pos = 0
                for price in day["Period"]["Point"]:
                     
                    pos = int(price["position"]) 
                    if pos-1 != prev_pos:
                        #print("missing")
                        #print(day["Period"]["timeInterval"]["start"])
                        #print(prev_pos+1)
                        if len(prices[year][q]) == 0:
                            prices[year][q].append(float(0))
                        else:
                            #could be more sophisticated about how to add missing data. this will decrease volatility of data    
                            prices[year][q].append(prices[year][q][-1]) # append price last hour if missing data
                        prev_pos += 1
                        i+=1 
                        continue 
                    prev_pos = pos    
                     
                    if (i%price_resolution == 0):
                        prices[year][q].append(float(price["price.amount"]))
                    i+=1    
                
                #this is for adding in data where it is missing
                if i/price_resolution < 24:
                    for _ in range(24-i):
                        #what data should be subistuded should be thought more about later.
                        #just appening a zero for now.
                        prices[year][q].append(prices[year][q][-1])
            
            k=1
            if retard_format:
                for period in load_dict["GL_MarketDocument"]["TimeSeries"]:   
                    for point in period["Period"]["Point"]:
                        if k%load_resolution == 0:
                            loads[year][q].append(int(point["quantity"]))
                        k+=1
            else:    
                for point in load_dict["GL_MarketDocument"]["TimeSeries"]["Period"]["Point"]:   
                    if k%load_resolution == 0:
                        loads[year][q].append(int(point["quantity"]))
                    k+=1
                
            
            
            if len(prices[year][q]) < len(loads[year][q]):
                for _ in range(len(loads[year][q])-len(prices[year][q])):
                    prices[year][q].append(prices[year][q][-1])
            
            # change this to == later    
            if len(loads[year][q]) <= len(prices[year][q]):
                day_amount = 0
                week_amount = 0
                for i in range(len(loads[year][q])):
                
                    if (i+1) % 24 == 0:
                        bought_amount_daily[year][q].append(day_amount)
                        week_amount += day_amount
                        day_amount = 0
                    
                    
                    if (i+1) % 24*7 == 0:
                        bought_amount_weekly[year][q].append(week_amount)
                        week_amount = 0
                    
                    hour_amount = loads[year][q][i]*prices[year][q][i]
                    day_amount += hour_amount
                    quarter_amount += hour_amount
                    year_amount += hour_amount
                    
                    
                    bought_amount[year][q].append(hour_amount)
                    bought_amount_hourly[year][q].append(hour_amount)
                
                bought_amount_qurterly[year][q] = quarter_amount
                 
        
                
            load_data.close()
            price_data.close()
            
        bought_amount_yearly[year].append(year_amount)    
             
    return  [bought_amount, bought_amount_hourly, bought_amount_daily, bought_amount_weekly, bought_amount_qurterly, bought_amount_yearly]       
            

            
def volume_amount(years, area):
    
    stub_load_data = "Data_entsoe/Load_data/"+area+"/"
    
    daily_volume = {}
    weekly_volume = {}
    quarterly_voume = {}
    yearly_volume = {}
    
    loads = {}
    
    for year in years:
        dir_load_data = stub_load_data+year
        
        daily_volume[year] = {}
        weekly_volume[year] = {}
        quarterly_voume[year] = {}
        yearly_volume[year] = []
        
        loads[year] = {}
    
        year_amount = 0
        
        for q in os.listdir(dir_load_data):
            
            quarter_amount = 0
            day_amount = 0
            week_amount = 0
            
            daily_volume[year][q] = []
            weekly_volume[year][q] = []
            quarterly_voume[year][q] = 0
            
            
            loads[year][q] = [] 
            load_data = open(os.path.join(dir_load_data, q), "r")
            dict = xmltodict.parse(load_data.read())
            load_data.close()
            retard_format = isinstance(dict["GL_MarketDocument"]["TimeSeries"], list)
            if retard_format:
                load_resolution = 60/int(dict["GL_MarketDocument"]["TimeSeries"][0]["Period"]["resolution"][2:4])
            else:
                load_resolution = 60/int(dict["GL_MarketDocument"]["TimeSeries"]["Period"]["resolution"][2:4])
           
            
            k=1
            if retard_format:
                for period in dict["GL_MarketDocument"]["TimeSeries"]:   
                    for point in period["Period"]["Point"]:
                        if k%load_resolution == 0:
                            loads[year][q].append(int(point["quantity"]))
                        k+=1
            else:    
                for point in dict["GL_MarketDocument"]["TimeSeries"]["Period"]["Point"]:   
                    if k%load_resolution == 0:
                        loads[year][q].append(int(point["quantity"]))
                    k+=1
            
            for i in range(len(loads[year][q])):
                hour_amount = loads[year][q][i]
                day_amount += hour_amount
                week_amount += hour_amount
                quarter_amount += hour_amount
                year_amount += hour_amount
                    
                if (i+1) % 24 == 0:
                    daily_volume[year][q].append(day_amount)
                    day_amount = 0
                       
                if (i+1) % 24*7 == 0:
                    weekly_volume[year][q].append(week_amount)
                    week_amount = 0
                        

                
            quarterly_voume[year][q] = quarter_amount
        
        
        yearly_volume[year].append(year_amount)            
                        
        load_data.close()
            
             
    return [daily_volume, weekly_volume, quarterly_voume, year_amount]
    

# combine_amount will add the elements on the same index of two lists with eachother and append it to a new list, which is returned.           
def combine_amount(amount1, amount2):
    
    combined = []
    
    if len(amount1) == len(amount2):
        for i in range(len(amount1)):
            combined.append(amount1[i]+amount2[i])
    
    return combined

# combine_whole_amount will do the same as combine_amount, but will do so for all years and quarters for two provided dicts (of the dict{year}{quarter}[data] format)            
def combine_whole_amount(dict1, dict2):
    
    combined = {}
    
    if len(dict1) == len(dict2):
        for year in dict1:
            combined[year] = {}
            for q in dict1[year]:
                combined[year][q] = combine_amount(dict1[year][q], dict2[year][q])
    
    return combined                

    
def dict_to_list(dict):
    
    list = []
    
    for year in dict:
        for q in dict[year]:
            list += dict[year][q]
    
    return list        



def daily_avrage_price(volum, cost):
    
    resp = []
    
    if len(volum) == len(cost):
        for i in range(len(volum)):
            resp.append(cost[i]/volum[i])
    
    return resp        
            

def Print_volatility_of_prices(area, years, prices=None):
    
    if prices == None:
        prices = daily_cloasing_several_areas(years, area)
    
    result = {}
    avragesp = {"total":0, "2017-2020": 0, "2021-2024":0}
    d_list = []
    td_list = []
    
    avrages = {}
    avrages["total"] = 0
    avrages["avrage"] = 0
    for area in prices:
        for year in prices[area]:
            avrages[year] = 0
    
    
    for area in prices:
        fstr = ""
        result[area] = {}
        sum = 0
        d_point = Util.make_new_d_point(area=area)
        td_point = Util.make_new_d_point(area=area)
        period_2017_2020 = []
        period_2021_2024 = []
        
        for year in prices[area]:
            
            p_list = dict_to_list({year:prices[area][year]})
            std = Analysis.Std(p_list)
            result[area][year] = std
            avrages[year] += std
            sum += std
            
            vstr = "%.1f" % std
            if std < 100:
                vstr = " " + vstr
            if std < 10:
                vstr = " " + vstr
            
            fstr += year+": std "+ vstr + " | "
            
            if int(year)<2021:
                period_2017_2020 += p_list
            else:
                period_2021_2024 += p_list
        
        total_period_var = Analysis.Std(dict_to_list(prices[area]))
        vstr = "%.1f" % total_period_var
        astr = "%.1f" % (sum/len(prices[area]))
        fstr = area+"| "+"total: "+ vstr +" | avrage: " + astr +" | "+ fstr
        result[area]["total"] = total_period_var
        avrages["avrage"] += sum/len(prices[area])
        avrages["total"] += total_period_var
        
        d_point["str"] = fstr
        d_point["data"] = (sum/len(prices[area]))
        d_list.append(d_point)
        
        tstr = area+"| "+"total: "+ vstr +" | 2017-2020: "+"%.1f" % Analysis.Std(period_2017_2020)+" | 2021-2024: " + "%.1f" % Analysis.Std(period_2021_2024)
        
        td_point["data"] = total_period_var
        td_point["str"] = tstr
        td_list.append(td_point)
        
        #print(tstr)
        avragesp["total"] += total_period_var
        avragesp["2017-2020"] += Analysis.Std(period_2017_2020)
        avragesp["2021-2024"] += Analysis.Std(period_2021_2024)
    
    print("############################ EL PRICE VOLATILITY FOR PERIODS ############################################################")
    
    Util.sort_and_print_d_list(td_list)
    
    fstr = "AVG"
    for col in avragesp:
        
        std = avragesp[col]/len(prices)
        vstr = "%.1f" % std
        
        if col == "total":
            fstr += " "+col+": "+vstr+" |"
        else:
            fstr += " "+col+": "+vstr+" |"
    print(fstr[:-1])
    
    print("################################ EL PRICE VOLATILITY ########################################")             
    
    Util.sort_and_print_d_list(d_list)
    
    fstr = "AVG"
    for col in avrages:
        
        std = avrages[col]/len(prices)
        vstr = "%.1f" % std
        
        if col == "total" :
            fstr += " "+col+": "+vstr+" |"
        elif col == "avrage":  
            fstr += " "+col+": "+vstr+" |"
        else:
            if std < 100:
                vstr = " " + vstr
            if std < 10:
                vstr = " " + vstr
            fstr += " "+col+": std "+vstr+" |"
    
    print(fstr)
        
    
    return result



##################_MAIN_CODE_##########################

"""
# time format: YYYYMMDDHHHH (year-month-day-hour)
period_start = "202401010100" #start time
period_end = "202404012200" #end time


price_data = "A44"
load_data = "A65"


domain = Bidding_zones["NO2"]
domain2 = Bidding_zones["EE"]


#request_data_for_year("2024", domain, price_data)
#request_data_for_year("2023", domain)
#request_data_for_year("2024", domain2, price_data)

#request_data_for_year("2024", domain, load_data)
#request_data_for_year("2024", domain2, load_data)


daily_cost_NO2 = dict_to_list(bougth_amount(["2024"], "NO2")[2])

vol = volume_amount(["2024"], "NO2")[0]
daily_volum_NO2 = dict_to_list(vol)

#print(len(vol["2024"]["Q3"]))


daily_price = daily_avrage_price(daily_volum_NO2, daily_cost_NO2)

daily_closing_price = daily_cloasing("2024", "NO2")

print(len(daily_price))

plt.plot(dict_to_list(daily_closing_price))



plt.plot(daily_price)

plt.show()

#make plots for daily payed, daily avrage prices, and daily cloasing prices for NO2

#Find correlation between amount payed in Norway for NO2 and NO1


#dict = xmltodict.parse(respons)

"""
###########  REQUESTING DATA  ###################### 
norway = ["NO1","NO2","NO3","NO4","NO5"]
sweden = ["SE1","SE2","SE3","SE4",]
italy = [
    "IT-CENTRE_NORTH",
    "IT-CENTRE_SOUTH",
    "IT-NORTH",
    "IT-SARDINIA",
    "IT-SICILY",
    "IT-SOUTH",
    ]
denmark = ["DK1","DK2"]
poland = ["PL"]
netherlands = ["NL"]
other = ["SEM", "ICELAND", "MOLDOVA", "UA-IPS", "AL", "BA", "DE_LU", "ME", "CY", "GB", "HR", "MK","IT-SACO_AC", "CH", "GR",
    "IT-SACODC", "IT-MONFALCONE", "IT-GR", "IT-MT", "IT-NORTH_SI", "IT-NORTH_CH", "IT-NORTH_AT", "IT-NORTH_FR", "IT-NORTH_AT", "IT-NORTH_FR"]

composit_area = norway + sweden + italy + denmark + other
area = [x for x in Area_names if x not in composit_area]


years = ["2017","2018","2019","2020","2021","2022","2023", "2024"]
#years = ["2019","2020","2021","2022","2023", "2024"]

price_data = "A44"
load_data = "A65"


#request_data_in_biddingzone(years=years, country_area=area, data_type=price_data)
#request_data_in_biddingzone(years=years, country_area=area, data_type=load_data)

##########  HANDELING DATA ##################


"""
# Finding daily avrage price for norway
daily_cost_NO1 = bougth_amount(years, "NO1")[2]
daily_cost_NO2 = bougth_amount(years, "NO2")[2]
daily_cost_NO3 = bougth_amount(years, "NO3")[2]
daily_cost_NO4 = bougth_amount(years, "NO4")[2]
daily_cost_NO5 = bougth_amount(years, "NO5")[2]

daily_cost_norway = combine_whole_amount(daily_cost_NO1, combine_whole_amount(daily_cost_NO2, combine_whole_amount(daily_cost_NO3, combine_whole_amount(daily_cost_NO4, daily_cost_NO5))))

volume_NO1 = volume_amount(years, "NO1")[0]
volume_NO2 = volume_amount(years, "NO2")[0]
volume_NO3 = volume_amount(years, "NO3")[0]
volume_NO4 = volume_amount(years, "NO4")[0]
volume_NO5 = volume_amount(years, "NO5")[0]

volume_norway = combine_whole_amount(volume_NO1, combine_whole_amount(volume_NO2, combine_whole_amount(volume_NO3, combine_whole_amount(volume_NO4, volume_NO5))))

daily_avrage_price_norway = daily_avrage_price(dict_to_list(volume_norway), dict_to_list(daily_cost_norway))

#Finding daily avrage price for sweden
daily_cost_SE1 = bougth_amount(years, "SE1")[2]
daily_cost_SE2 = bougth_amount(years, "SE2")[2]
daily_cost_SE3 = bougth_amount(years, "SE3")[2]
daily_cost_SE4 = bougth_amount(years, "SE4")[2]

daily_cost_sweden = combine_whole_amount(daily_cost_SE1, combine_whole_amount(daily_cost_SE2, combine_whole_amount(daily_cost_SE3, daily_cost_SE4)))

volume_SE1 = volume_amount(years, "SE1")[0]
volume_SE2 = volume_amount(years, "SE2")[0]
volume_SE3 = volume_amount(years, "SE3")[0]
volume_SE4 = volume_amount(years, "SE4")[0]

volume_sweden = combine_whole_amount(volume_SE1, combine_whole_amount(volume_SE2, combine_whole_amount(volume_SE3, volume_SE4)))

daily_avrage_price_sweden = daily_avrage_price(dict_to_list(volume_sweden), dict_to_list(daily_cost_sweden))
"""
#Finding daily avrage price for the netherlands
daily_cost_NL = bougth_amount(years, "NL")[2]
volume_NL = volume_amount(years, "NL")[0]


daily_avrage_price_NL = daily_avrage_price(dict_to_list(volume_NL), dict_to_list(daily_cost_NL))
daily_cloasing_price_NL = daily_cloasing(years, "NL")

#Finding daily avrage price for poland
daily_cost_PL = bougth_amount(years, "PL")[2]
volume_PL = volume_amount(years, "PL")[0]

daily_avrage_price_PL = daily_avrage_price(dict_to_list(volume_PL), dict_to_list(daily_cost_PL))


daily_cloasing_prices = daily_cloasing_several_areas(years, area)
norway_cloasing = daily_cloasing_several_areas(years, norway, agregate=True)
sweden_cloasing = daily_cloasing_several_areas(years, sweden, agregate=True)
denmark_cloasing = daily_cloasing_several_areas(years, denmark, agregate=True)
italy_cloasing = daily_cloasing_several_areas(years, italy, agregate=True)

daily_cloasing_prices["NO"] = norway_cloasing["NO"]
daily_cloasing_prices["SE"] = sweden_cloasing["SE"]
daily_cloasing_prices["DK"] = denmark_cloasing["DK"]
daily_cloasing_prices["IT"] = italy_cloasing["IT"]

area += ["NO", "SE", "DK", "IT"]

Print_volatility_of_prices(None, None, prices=daily_cloasing_prices)

######### PLOTING DATA ###################
#plt.plot(daily_avrage_price_PL)
#plt.plot(dict_to_list(daily_cloasing(years, "PL")))
#plt.plot(daily_avrage_price_NL)
#plt.plot()

#plt.plot(daily_avrage_price_norway)
#plt.show()

"""
plt.plot(daily_avrage_price_norway)
plt.show()

plt.plot(daily_avrage_price_NL)
plt.show()
"""
