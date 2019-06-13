import folium
import pandas as pd
import urllib.request
import json
import webbrowser
from urllib.parse import quote
from urllib.request import Request, urlopen


key = ''


def getGeoData(address):

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ quote(address) +'&key='+key+'&language=ko'

    req = Request(url,headers={ 'X-Mashape-Key': key })
    addr = {}
    jsonAddress = urlopen(req).read().decode('utf8')
    addr = json.loads(jsonAddress)
    addr_detail = addr['results'][0]['geometry']['location']
    print(addr_detail)

    latitude = addr_detail['lat']
    longitude = addr_detail['lng']


    return [latitude,longitude]




def main():


    map = folium.Map(location=[35.258837,129.092967], zoom_start=13)

    filename = '금정구무더위쉼터.csv'
    df = pd.DataFrame.from_csv(filename, encoding='CP949', index_col=0, header=0)
    geoData = []

    for index, row in df.iterrows():
        row['소재지도로명주소'] = row['소재지도로명주소'].split('(',1)[0]
        row['소재지도로명주소'] = row['소재지도로명주소'].split(',',1)[0]
        geoData = getGeoData(row['소재지도로명주소'])
        if geoData != None:
            folium.Marker(geoData, popup=row['소재지도로명주소'], icon=folium.Icon(color='red')).add_to(map)

    svFilename = 'guemjeong.html'
    map.save(svFilename)
    webbrowser.open(svFilename)

if __name__ == "__main__":
    main()
