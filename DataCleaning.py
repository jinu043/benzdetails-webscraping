import pandas as pd
import numpy as np
import re

#Import Raw Datas
path = "D:\\pythonProject\\webscraping\\Extracted_Raw_Data"
toyota = pd.read_excel(path+"\\Toyota_newcar_details_all.xlsx", index_col=0)
benz =  pd.read_excel(path+"\\Benz_newcar_details_all.xlsx", index_col=0)
hyundai = pd.read_excel(path+"\\Hyundai_newcar_details_all.xlsx", index_col=0)
kia = pd.read_excel(path+"\\Kia_newcar_details_all.xlsx", index_col=0)
lexus = pd.read_excel(path+"\\Lexus_newcar_details_all.xlsx", index_col=0)
mitsubishi = pd.read_excel(path+"\\mitsubishi_newcar_details_all.xlsx", index_col=0)
nissan = pd.read_excel(path+"\\Nissan_newcar_details_all.xlsx", index_col=0)
suzuki = pd.read_excel(path+"\\Suzuki_newcar_details_all.xlsx", index_col=0)
volkswagen = pd.read_excel(path+"\\Volkswagen_newcar_details_all.xlsx", index_col=0)

#Handle witn NaN Values
nan_details = pd.DataFrame([toyota.isna().sum(), benz.isna().sum(), hyundai.isna().sum(),
             kia.isna().sum(), lexus.isna().sum(), mitsubishi.isna().sum(), 
              nissan.isna().sum(), suzuki.isna().sum(), volkswagen.isna().sum()]).T
nan_details.columns = ["toyota", "benz", "hyundai", "kia", "lexus", "mitsubishi", "nissan", "suzuki", "volkswagen"]

print(nan_details.T)

toyota.dropna(inplace=True)
benz.dropna(inplace=True)
volkswagen.dropna(inplace=True)

#Combine all vehicles data
raw_data = pd.concat([toyota, benz, hyundai, kia, lexus, mitsubishi, nissan, suzuki, volkswagen]).reset_index(drop=True)

#Data Cleaning
def remove_titles(data, model="model", vt="vehicle_type", 
                 es="export_status", my="model_year", loc="location", ft="fuel_type", mil="mileage", spec="spec"):
    data[model]=data[model].str.replace("Model", "")
    data[vt]=data[vt].str.replace("Vehicle type", "")
    data[es]=data[es].str.replace("Export status", "")
    data[my]=data[my].str.replace("Model Year", "")
    data[my]=data[my].str.replace("NEW!", "")
    data[my]=data[my].apply(lambda x:re.sub(r"[\([{})\]]", "", x)).astype(int)
    data[loc]=data[loc].str.replace("Location", "")
    data[ft]=data[ft].str.replace("Fuel Type", "")
    data[mil]=data[mil].str.replace("Kilometers", "")
    data[mil]=data[mil].str.replace("Km", "")
    data[spec]=data[spec].str.replace("Specs", "")

data_names = [toyota, benz, hyundai, kia, lexus, mitsubishi, nissan, suzuki, volkswagen]
for data in data_names:
    remove_titles(data)

def engine_capacity(data, col="vehicle_name"):
    data["engine_capacity"]=data[col].str.extract(r"(\d\.\d)")
    data["engine_capacity"] = data["engine_capacity"].astype("float")

for data in data_names:
    engine_capacity(data)

toyota["vehicle_name"]="toyota"
benz["vehicle_name"] =  "benz"
hyundai["vehicle_name"] = "hyundai"
kia["vehicle_name"] = "kia"
lexus["vehicle_name"] = "lexus"
mitsubishi["vehicle_name"] = "mitsubishi"
nissan["vehicle_name"] = "nissan"
suzuki["vehicle_name"] = "suzuki"
volkswagen["vehicle_name"] = "volkswagen"

def get_price(data, col="vehicle_price"):
    data[col]=data[col].str.replace(",", "")
    data["price_emi"] = data[col].str.findall("(\d+)")
    data["price"] = data["price_emi"].str[0].astype("float")
    data["emi"]=data["price_emi"].str[1].astype("float")

for data in data_names:
    get_price(data)

def fillna(data, col="price"):
    data["price_availability"] = data[col].fillna(0)

def price_check(data, col="price_availability"):
    data[col] = data[col].apply(lambda x:np.where(x>0, "Yes", "No"))

for data in data_names:
    fillna(data)

for data in data_names:
    price_check(data)

cleaned_data = pd.concat(data_names)

def del_columns(data):
    del data["vehicle_price"]
    del data["vehicle_link"]
    del data["price_emi"]
    del data["emi"]

for data in data_names:
    del_columns(data)

print(cleaned_data.sample(10))