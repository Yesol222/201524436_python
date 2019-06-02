# 금정구 무더워 쉼터 지도

## 정보컴퓨터공학부 / 201524436 / 김예솔


## 프로젝트 개요
무더운 여름을 대비해서 집에 에어컨이 없거나 쉴 곳을 찾기 힘든 어르신들을 위해서 금정구에 존재하는 무더위 쉼터 위치를 지도로 표현하는 프로그램을 만들었습니다. 파이썬 pandas를 이용해 data.go.kr에 있는 금정구 무더위 쉼터 데이터를 가져왔고 구글 지오 api로 주소 데이터를 위도, 경도 좌표로 바꿨습니다. 이를 folium 이라는 지도를 그려주는 라이브러리를 이용해 지도로 표현하였습니다.

## 사용한 공공 데이터

[데이터보기](https://www.data.go.kr/dataset/15019137/fileData.do)

## 소스
<pre><code>
import folium
import pandas as pd
import urllib.request
import json
import webbrowser
from urllib.parse import quote
from urllib.request import Request, urlopen


key = 'AIzaSyC_vmcG8ZjXFYmD9pDhWr72vT-NNz6gHS8'


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

</code></pre>



