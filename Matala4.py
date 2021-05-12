# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:08:49 2021

@author: almog
"""
  
#places text
#Import the places text
places_Path="C:/Users/almog/Desktop/PythonMatalot/matala4/dests.txt"
places_text = open(places_Path,"r",encoding= "utf-8")
key=input('enter your API Key :')
import json
import requests

def get_distance_and_time(destenation):
    import requests
    start_point='תל אביב'
    url="https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s" % (start_point,destenation,key)
    try:
        response=requests.get(url)
        if not response.status_code==200:
            print("http error",response.status_code)
        else:
            try:
                response_data=response.json()
                dict_distance_time=dict()
                dict_distance_time['distance']=response_data['rows'][0]['elements'][0]['distance']['text']
                dict_distance_time['time']=response_data['rows'][0]['elements'][0]['duration']['text']
                return dict_distance_time
            except:
                print("response not in json format")
    except:
        print("something went worng with requests.get")
        
def get_lag_and_len(destenation):
    import requests
    url ="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(destenation,key)
    try:
        response=requests.get(url)
        if not response.status_code==200:
            print("http error",response.status_code)
        else:
            try:
                data_from_response=response.json()
                geo_dict = dict()
                geo_dict['lat'] = data_from_response['results'][0]['geometry']['location']['lat']
                geo_dict['lng'] = data_from_response['results'][0]['geometry']['location']['lng']
                return geo_dict
            except:
                print("response not in json format")
    except:
        print("something went worng with requests.get")

def create_tupels_for_place(place):#create a function for tupels
    try:
        distance=('Distance: ',(get_distance_and_time(place)['distance']))
        distance=''.join(distance)
        time=('Time: ',(get_distance_and_time(place)['time']))
        time=''.join(time)
        lng=('Length: ',str((get_lag_and_len(place)['lng'])))
        lng=''.join(lng)
        lat=('Latitude: ',str((get_lag_and_len(place)['lat'])))
        lat=''.join(lat)    
        return distance,time,lng,lat
    except:
        return ['not a real place'] #if its not a real place

places_dictionary=dict()#creating the full data dictionary 
find_farest_places=dict()
for place in places_text:
    if place not in places_dictionary:
        try:
            places_dictionary[place.rstrip()]=(create_tupels_for_place(place))
            find_farest_places[place.rstrip()]=(places_dictionary[place.rstrip()][0])
        except: 
            places_dictionary[place.rstrip()]=[]
            find_farest_places[place.rstrip()]=[]
    else: continue  
        
for place in places_dictionary: #print the dictinary city after city
    print(place,':' ,places_dictionary[place])
    
#print(places_dictionary) #print the full dictinary

#find the 3 farest from tel aviv
tmp=list() 
for k,v in find_farest_places.items():
    if 'not a real place'in v:continue
    else:
        tmp.append((v,k))    
tmp=sorted(tmp)[len(tmp)-3:] #taking the farest 3
count=1
for i in tmp:
    print("place:", count, "the city -", i[1] ,"with " , i[0] ," from Tel Aviv")
    count=count+1
     