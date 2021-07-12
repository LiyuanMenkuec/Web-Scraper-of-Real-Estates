import requests, pandas
from bs4 import BeautifulSoup

base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0,30,10):
    req=requests.get(base_url+str(page)+".html",
    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    con=req.content
    soup=BeautifulSoup(con,"html.parser")
    listOfItem=[]

    for item in soup.find_all("div",{"class":"propertyRpw"}):
        dic={}
        print(item.find_all("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ",""))
        dic["Price"]=item.find_all("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        dic["Adress"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        dic["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        try:
            dic["Beds"]=item.find("span",{"class","infoBed"}).find("b").text
        except:
            dic["Beds"]=None

        try:
            dic["Full Beaths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
        except:
            dic["Full Beaths"]=None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class":"featureName"}) ):
                print(feature_group.text,feature_name.text)
        listOfItem.append(dic)

print(len(listOfItem))
#print(soup.prettify())
df=pandas.DataFrame(listOfItem)
df.to_csv("output.csv")