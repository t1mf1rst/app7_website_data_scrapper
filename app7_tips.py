# create new jupyter notebook: jupyter notebook
import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content

soup = BeautifulSoup(c, "html.parser")
# print in human readable structure
# print(soup.prettify())
all = soup.find_all("div", {"class": "propertyRow"})
all[0].find("h4", {"class": "propPrice"}).text.strip()
page_nr = soup.find_all("a", {"class": "Page"})[-1].text
soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("div", {"class": "propertyRow"})
l = []
for item in all:
    d = {}
    d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
    try:
        d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
    except:
        d["Locality"] = None
    d["Price"] = item.find("h4", {"class", "propPrice"}).text.strip()
    try:
        d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
    except:
        d["Beds"] = None
    try:
        d["Area"] = item.find("span", {"class", "infoSqFt"}).find("b").text
    except:
        d["Area"] = None
    try:
        d["Full Baths"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
    except:
        d["Full Baths"] = None
    try:
        d["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
    except:
        d["Half Baths"] = None
    for column_group in item.find_all("div", {"class": "columnGroup"}):
        for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
            if "Lot Size" in feature_group.text:
                d["Lot Size"] = feature_name.text
    l.append(d)
df = pandas.DataFrame(l)
df.to_csv("output.csv")