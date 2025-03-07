#Source: https://newtransparency.entsoe.eu/market/energyPrices

import requests
import xmltodict
import os
import matplotlib.pyplot as plt
import numpy as np

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
    
    #file_name = "Domain_"+domain+"_start_"+period_start+"_end_"+period_end+".xml"
    
    #f = open("Data_entsoe/"+file_name,"w")
    #f.write(respons)
    #f.close
    
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



def daily_cloasing(year, area):
    
    respons = {year: {}}
    path = "Data_entsoe/Price_data/"+area+"/"+year+"/"
    
    for q in os.listdir(path):
        
        respons[year][q] = []
        price_data = open(os.path.join(path, q), "r")
        dict = xmltodict.parse(price_data.read())
        price_data.close()
    
        i = 0
        for day in dict["Publication_MarketDocument"]["TimeSeries"]:
            
            if i+1 == len(dict["Publication_MarketDocument"]["TimeSeries"]):
                break
            
            respons[year][q].append(float(day["Period"]["Point"][-1]["price.amount"]))
        
            i+=1
                    
    
    return respons



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
        for year in years:
            quarter_list.append(request_data_for_year(year,domain, doc_type=data_type))
        respons[area] = quarter_list
        
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
            
            prices[year][q] = []
            price_data = open(os.path.join(dir_price_data, q), "r")
            price_dict = xmltodict.parse(price_data.read())
            price_data.close()
            
            for day in price_dict["Publication_MarketDocument"]["TimeSeries"]:
                i=1
                for price in day["Period"]["Point"]:
                    i += 1
                    prices[year][q].append(float(price["price.amount"]))
                
                #this is for adding in data where it is missing
                if i < 24:
                    for _ in range(24-i):
                        #what data should be subistuded should be thought more about later.
                        #just appening a zero for now.
                        prices[year][q].append(0)
                
                    
            
            
            for point in load_dict["GL_MarketDocument"]["TimeSeries"]["Period"]["Point"]:
                loads[year][q].append(int(point["quantity"]))
            
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
            
            for point in dict["GL_MarketDocument"]["TimeSeries"]["Period"]["Point"]:
                loads[year][q].append(int(point["quantity"]))
                
            
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
    

# combine_amount will add the elements on the same index of two lists with eachother and append it to a new list, which is retuned.           
def combine_amount(amount1, amount2):
    
    combined = []
    
    if len(amount1) == len(amount2):
        for i in range(len(amount1)):
            combined.append(amount1[i]+amount2[i])
    
    return combined

# combine_whole_amount will do the same as combine_amount, but will do so for all years and quarters for two provided dicts (of the dict{year}{quarter}[data] format)            
def combine_whole_amount(dict1, dict2):
    
    combined = []
    
    if len(dict1) == len(dict2):
        for year in dict1:
            for q in dict1[year]:
                combined.append(combine_amount(dict1[year][q], dict2[year][q]))
    
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
            


##################_MAIN_CODE_##########################


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


daily_avrage_price = daily_avrage_price(daily_volum_NO2, daily_cost_NO2)

daily_closing_price = daily_cloasing("2024", "NO2")

print(len(daily_avrage_price))

plt.plot(dict_to_list(daily_closing_price))



plt.plot(daily_avrage_price)

plt.show()

#make plots for daily payed, daily avrage prices, and daily cloasing prices for NO2

#Find correlation between amount payed in Norway for NO2 and NO1


#dict = xmltodict.parse(respons)
