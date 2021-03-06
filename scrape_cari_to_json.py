import requests
import json
from bs4 import BeautifulSoup

#loop through the catalog pages to get all the possible aesthetic url slugs

url_slug_list = []

keep_looping = True

base_url = "https://api.cari.institute/api/v1/aesthetic/findForList"

page_number = 0

while keep_looping == True:
        
    payload = {'page': page_number, 'sortField' : "name", 'asc' : True}
    
    results = requests.get(base_url, params=payload)
    
    data = json.loads(results.text)
                
    if data["empty"] == False:
        
        for aesthetic in data["content"]:
                    
            url_slug_list.append(aesthetic["urlSlug"])
            
        page_number = page_number + 1
        
    elif data["empty"] == True:
                
        keep_looping = False

#loop through each aesthetic page to get relevant data

aesthetics_list = []

for aesthetic_slug in url_slug_list:
    
    base_url = f"https://api.cari.institute/api/v1/aesthetic/findForPage/{aesthetic_slug}"

    payload = {'includeSimilarAesthetics': True}

    results = requests.get(base_url, params=payload)

    data = json.loads(results.text)

    #add data to dictionary
    
    aesthetic_data = (
        {"ID" : data["aesthetic"],
         "Name" : data["name"],
         "Description": None,
         "Start_Year": data["startYear"],
         "End_Year": None,
         "Link": "https://cari.institute/aesthetics/" + aesthetic_slug,
         "Image": data["displayImage"]["url"],
         "Similar_Aesthetics": []}
        ) 
    
    if "description" in data:
        
        description_with_html = data["description"]
        
        parsed_description = BeautifulSoup(description_with_html,features="html.parser")
        
        aesthetic_data.update({"Description": parsed_description.get_text(strip=True)})
    
    if "endYear" in data: 
        
         aesthetic_data.update({"End_Year": data["endYear"]})
    
    if "similarAesthetics" in data:
        
        for similar_aesthetic in data["similarAesthetics"]:
            
            aesthetic_data["Similar_Aesthetics"].append(similar_aesthetic["aesthetic"])

    aesthetics_list.append(aesthetic_data)
    
with open("cari_data.json", "w") as json_file:
    
    json.dump(aesthetics_list,json_file)

