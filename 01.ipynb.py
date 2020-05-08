#!/usr/bin/env python
# coding: utf-8

# # Import Package

# In[29]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import folium
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors
from geopy.geocoders import Nominatim


# # Request Data From Website, and Append Data To Different List

# In[7]:


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(source, 'lxml')
body = soup.find('tbody')
tags = body('td')
postal_code =list()
borough = list()
neigh = list()
a = 2
for tag in tags:
    a = a+1
    tag=str(tag)
    x = re.findall('^<td>(.+)', tag)
    if a%3 == 0:
        postal_code.append(x)
    elif a%3 == 1:
        borough.append(x)
    elif a%3 == 2:
        neigh.append(x)


# # Convert List of List to The List Of String

# In[8]:


postal_code = [''.join(x) for x in postal_code]
borough = [''.join(x) for x in borough]
neigh = [''.join(x) for x in neigh]


# # Build A DataFrame

# In[9]:


df = {'Postal Code': postal_code,
     'Borough': borough,
     'Neighborhood': neigh}
df = pd.DataFrame(df)
df.head()


# # Clean Empty Data

# In[10]:


empty = df[df['Borough'] == 'Not assigned'].index
df.drop(empty, inplace = True)


# In[11]:


df.reset_index(inplace = True, drop =True)
df.head()


# In[12]:


df.shape


# In[13]:


coord = pd.read_csv('C:\\Users\\vv123\\Desktop\\projects\\Coursera_Capstone\\Geospatial_Coordinates.csv')


# In[14]:


coord.head()


# In[15]:


df = pd.merge(df, coord, on = 'Postal Code')


# In[16]:


df.head()


# In[17]:


downtownt_df = df[df['Borough']=='Downtown Toronto'].reset_index(drop = True)


# In[18]:


centralt_df = df[df['Borough']=='Central Toronto'].reset_index(drop = True)


# In[19]:


eastt_df = df[df['Borough']=='East Toronto'].reset_index(drop = True)


# In[20]:


westt_df = df[df['Borough']=='West Toronto'].reset_index(drop = True)


# In[26]:


Toronto_dataframe = westt_df.append(eastt_df).append(centralt_df).append(downtownt_df).reset_index(drop = True)


# In[33]:


Toronto_dataframe.head()


# In[32]:


address = 'Toronto'

geolocator = Nominatim(user_agent="Toronto_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[34]:


map_Toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(Toronto_dataframe['Latitude'], Toronto_dataframe['Longitude'], Toronto_dataframe['Borough'], Toronto_dataframe['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Toronto)  
    
map_Toronto


# In[ ]:




