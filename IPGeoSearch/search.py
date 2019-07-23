import pandas as pd
import json
import ast
import time
import requests

def search(ipList,path,key, **kwargs):
    try:
        ipList = ipList
    except:
        raise ValueError("IP list was not specified.")
    try:
        key = key
    except:
        raise ValueError("Key was not specified.")
        
    def flatten_json(nested_json):
        """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
        """
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(nested_json)
        return out
    def parseResult(ip,res, **kwargs):
        with open(path+ip+".json", 'w') as result:
            result.write(res)
            result.close()
            with open(path+ip+".json", 'r') as result:
                data = json.load(result)
                data = flatten_json(data)
                ipAddress = [""+ip+""]
                df = pd.Series(data).to_frame().T
                df['ip'] = ipAddress
                #processing and removing unnecessary fields from the result
                try:
                    if set(['city_names_en','subdivisions_0_names_en']).issubset(df.columns):
                        df = df[['ip','city_names_en','subdivisions_0_names_en','country_names_en','continent_names_en','location_latitude','location_longitude',
                        'autonomous_system_number','autonomous_system_organization','isp','organization','organization_type','isic_code','naics_code','connection_type'
                        ,'ip_routing_type', 'line_speed']]
                        df = df.rename(columns={'city_names_en':'City','subdivisions_0_names_en':'State/Province','country_names_en':'Country','continent_names_en':'Continent',
                        'location_latitude':'Latitude','location_longitude':'Longitude','autonomous_system_number':'ASN','autonomous_system_organization':'ASO',
                        'isp':'ISP', 'organization':'Organization','organization_type':'Organization Type','isic_code':'ISIC','naics_code':'NAICS'
                        ,'connection_type':'Connection Type','ip_routing_type':'IP Routing Type','line_speed':'Line Speed'})
                    elif 'city_names_en' in df:
                        df = df[['ip','city_names_en','country_names_en','continent_names_en','location_latitude','location_longitude',
                        'autonomous_system_number','autonomous_system_organization','isp','organization','organization_type','isic_code','naics_code','connection_type',
                        'ip_routing_type','line_speed']]
                        df = df.rename(columns={'city_names_en':'City','country_names_en':'Country','continent_names_en':'Continent',
                        'location_latitude':'Latitude','location_longitude':'Longitude','autonomous_system_number':'ASN','autonomous_system_organization':'ASO',
                        'isp':'ISP', 'organization':'Organization','organization_type':'Organization Type','isic_code':'ISIC','naics_code':'NAICS'
                        ,'connection_type':'Connection Type','ip_routing_type':'IP Routing Type','line_speed':'Line Speed'})
                    elif 'subdivisions_0_names_en' in df:
                        df = df[['ip','subdivisions_0_names_en','country_names_en','continent_names_en','location_latitude','location_longitude',
                        'autonomous_system_number','autonomous_system_organization','isp','organization','organization_type','isic_code','naics_code','connection_type',
                        'ip_routing_type','line_speed']]
                        df = df.rename(columns={'subdivisions_0_names_en':'State/Province','country_names_en':'Country','continent_names_en':'Continent',
                        'location_latitude':'Latitude','location_longitude':'Longitude','autonomous_system_number':'ASN','autonomous_system_organization':'ASO',
                        'isp':'ISP', 'organization':'Organization','organization_type':'Organization Type','isic_code':'ISIC','naics_code':'NAICS'
                        ,'connection_type':'Connection Type','ip_routing_type':'IP Routing Type','line_speed':'Line Speed'})
                    else:
                        df = df[['ip','country_names_en','continent_names_en','location_latitude','location_longitude',
                        'autonomous_system_number','autonomous_system_organization','isp','organization','organization_type','isic_code','naics_code','connection_type',
                        'ip_routing_type','line_speed']]
                        df = df.rename(columns={'country_names_en':'Country','continent_names_en':'Continent',
                        'location_latitude':'Latitude','location_longitude':'Longitude','autonomous_system_number':'ASN','autonomous_system_organization':'ASO',
                        'isp':'ISP', 'organization':'Organization','organization_type':'Organization Type','isic_code':'ISIC','naics_code':'NAICS'
                        ,'connection_type':'Connection Type','ip_routing_type':'IP Routing Type','line_speed':'Line Speed'})
                except:
                    raise RuntimeError("Something went really wrong. Either the IP does not exist in the database, server is down or "+
                    "another error occured. Check "+ip+".json for more details and file an issue if you are unable to solve the problem.")
                result.close()
        return df.to_csv(path_or_buf=path+ip+".csv", sep =',', index = False)
    if any(not isinstance(y,(str)) for y in ipList):
        raise TypeError("An entry in ipList is not a string at line and cannot be read by the server")

    url = 'https://ipgeo.azurewebsites.net/IPsearch'
    for ip in ipList:
        ipsearch = "{\n\t\"ip\":\""+ip+"\"\n}"
        authKey=key.replace('\n', '')
        authentication = {"x-api-key":authKey, 'Content-Type': "application/json"}
        res = requests.post(url, data=ipsearch, headers=authentication)
        res = res.text
        if res in ['{"message":"Your Key is invalid. Please purchase a key or start a trial."}\n']:
            raise RuntimeError('Your Key is Invalid. Please purchase a key or start a trial.')
        if res in ['{"message":"Your Trial Period has expired. Please purchase a key."}\n']:
            raise RuntimeError('Your Trial Period has expired. Please purchase a key.')
        if res in ['{"message":"Your Key has expired. Please purchase a new key."}\n']:
            raise RuntimeError('Your Key has expired. Please purchase a new key.')
        if res in ['{"message":"The Network you are using in unknown and key cannot be secured. Please change networks."}\n']:
            raise RuntimeError('The Network you are using in unknown and key cannot be secured. Please change networks.')
        if res in ['{"message":"Your Key is being used on a different network than it was registered on. Please use your original network or purchase a new key for this network."}\n']:
            raise RuntimeError('Your Key is being used on a different network than it was registered on. Please use your original network or purchase a new key for this network.')
        parseResult(ip, res)
"""
    if 'key' not in kwargs:
        url = 'https://ipgeo.azurewebsites.net/try'
        warnLimit(10)
        for ip in ipList:
            ipsearch = "{\n\t\"ip\":\""+ip+"\"\n}"
            authentication = {'Content-Type': "application/json"}
            res = requests.post(url, data=ipsearch, headers=authentication)
            res = res.text
            if res in ['{"message": "10 per 1 month"}\n']:
                raise RuntimeError('You Have Exceded your Monthly search Limit')
            parseResult(ip, res)
    else:
         
            if 'key_type' in kwargs and kwargs.get('key_type') in ['basic','premium','deluxe','ultra']:
                
                key_type = kwargs.get('key_type')
                key = kwargs.get('key')
                url = 'https://ipgeo.azurewebsites.net/'+key_type+''
                
                for ip in ipList:
                    if key_type == 'basic':
                        warnLimit(1000)
                    elif key_type == 'premium':
                        warnLimit(10000)
                    elif key_type == 'deluxe':
                        warnLimit(100000)
                    ipsearch = "{\n\t\"ip\":\""+ip+"\"\n}"
                    authKey=key.replace('\n', '')
                    authentication = {"x-api-key":authKey, 'Content-Type': "application/json"}
                    
                    res = requests.post(url, data=ipsearch, headers=authentication)
                    res = res.text
                    if res in ['{"message": "1000 per 1 month"}\n','{"message": "10000 per 1 month"}\n','{"message": "100000 per 1 month"}\n']:
                        raise RuntimeError('You Have Exceded your Monthly search Limit')

                    parseResult(ip, res)
            if 'key_type' in kwargs and kwargs.get('key_type') not in ['basic','premium','deluxe','ultra']:
                raise TypeError("A key type was inputed was not a valid key type. Valid Key types are: basic, premium, deluxe, and ultra")
            if 'key_type' not in kwargs:
                raise TypeError("A key was inputed but a valid key type was not specified. Valid Key types are: basic, premium, deluxe, and ultra")
"""     





