from bs4 import BeautifulSoup
import requests
import pandas as pd

#Extract all pages url's
page_urls = []
for i in range(1,25):
    link = 'https://www.dubicars.com/uae/new/mercedes-benz?page={}'.format(i)
    page_urls.append(link)
print("Page URL's \n", page_urls)

#Extract vehicle name, vehicle price, vehicle link from main page
VN = []
VP = []
VL = []
def main_page_details(page_url):
    page_response = requests.get(page_url)
    page_contents = page_response.text
    page_doc = BeautifulSoup(page_contents, "html.parser")
    
    #Vehicle Name
    vn_tag = page_doc.find_all("a", {"class":"title fw-600 mt-12 d-block"})
    for tag in vn_tag:
        VN.append(tag.text.strip())
    
    #Vehicle Price
    price_tag = page_doc.find_all("span", {"class":"price d-flex align-center space-between text-link"})
    for tag in price_tag:
        VP.append(tag.text.strip())
        
    #Vehicle Links
    vl_tag = page_doc.find_all("a", class_="image-container d-block")
    for tag in vl_tag:
        VL.append(tag["href"])

for link in page_urls:
    main_page_details(link)

print(len(VN))
print(len(VP))
print(len(VL))

#Extract each vehicle further details through each vehicle links
def general_vehicle_details(vehicle_link):
    vehicle_response = requests.get(vehicle_link)
    vehicle_page_content = vehicle_response.text
    vehicle_doc = BeautifulSoup(vehicle_page_content, "html.parser")
    
    #Model
    model_tag = vehicle_doc.find_all("li", class_="fd-col")
    model = model_tag[1].text.strip()
    
    #Vehicle Type
    vehicle_type = model_tag[4].text.strip()
    
    #Export status
    export_status = model_tag[5].text.strip()
    
    #Deales Name
    dealer_tag = vehicle_doc.find_all("strong", {"class":"d-block"})
    dealer_name = dealer_tag[1].text.strip()
    
     #Model year
    my_tag = vehicle_doc.find_all("li", class_="icon-calendar")
    model_year = my_tag[0].text.strip()
    
    #Location
    ln_tag = vehicle_doc.find_all("li", class_="icon-location")
    location = ln_tag[0].text.strip()
    
    #fuel type
    fuel_tag = vehicle_doc.find_all("li", class_="icon-fuel")
    if len(fuel_tag) !=0:
        fuel_type = fuel_tag[0].text.strip()
    else:
        fuel_type = "NaN"
    
    #mileage
    km_tag = vehicle_doc.find_all("li", class_="icon-gauge")
    mileage = km_tag[0].text.strip()
    
    #spec
    spec_tag = vehicle_doc.find_all("li", class_="icon-cog")
    spec = spec_tag[0].text.strip()
    
    
    return model, vehicle_type, export_status, dealer_name, model_year, location, fuel_type, mileage, spec

#Create Datadrames from the extracted datas
def create_dataframe(VN,VP,VL):
    vehicle_data =  pd.DataFrame({
        "vehicle_name":VN,
        "vehicle_price":VP,
        "vehicle_link":VL
    })
    return vehicle_data
    
basic_vehicle_data = create_dataframe(VN,VP,VL)

model = []
vehicle_type = []
export_status = []
dealer_name = []
MY = []
LN = []
fuel = []
mileage = []
spec = []
for link in basic_vehicle_data["vehicle_link"].tolist():
    general_details = general_vehicle_details(link)
    model.append(general_details[0])
    vehicle_type.append(general_details[1])
    export_status.append(general_details[2])
    dealer_name.append(general_details[3])
    MY.append(general_details[4])
    LN.append(general_details[5])
    fuel.append(general_details[6])
    mileage.append(general_details[7])
    spec.append(general_details[8])

vehicle_general_details = pd.DataFrame(
{
    "model":model,
    "vehicle_type":vehicle_type,
    "export_status":export_status,
    "dealer_name":dealer_name,
    "model_year":MY,
    "location":LN,
    "fuel_type":fuel,
    "mileage":mileage,
    "spec":spec
})

vehicle_details = pd.concat([basic_vehicle_data, vehicle_general_details], axis=1)