import pandas as pd
import json
import ast
import pandas as pd
import time
import requests

def search(ipList,path, **kwargs):
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
    def warnLimit(limit):
        if len(ipList) > limit:
            print("Your IP List is longer than "+str(limit)+" entires, which is more than alloted for your version. Sending it would result in an error from the server.")
            print("Please shorten your list so that all your IP's may be processed.")
            exit()
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
                    raise RuntimeError('IP does Not Exist Check '+ip+'.json for more details.')
                result.close()
        return df.to_csv(path_or_buf=path+ip+".csv", sep =',', index = False)
    
    if 'key' not in kwargs:
        url = 'https://ipgeo.azurewebsites.net/try'
        warnLimit(10)
        for ip in ipList:
            ipsearch = "{\n\t\"ip\":\""+ip+"\"\n}"
            authentication = {'Content-Type': "application/json"}
            res = requests.post(url, data=ipsearch, headers=authentication)
            res = res.text
            if res in ['{"message": "10 per 1 month"}\n']:
                raise RuntimeError('You Have Exceded your search limit Monthly Limit')
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
                        raise RuntimeError('You Have Exceded your search limit Monthly Limit')

                    parseResult(ip, res)
            if 'key_type' in kwargs and kwargs.get('key_type') not in ['basic','premium','deluxe','ultra']:
                raise TypeError("A key type was inputed was not a valid key type. Valid Key types are: basic, premium, deluxe, and ultra")
            if 'key_type' not in kwargs:
                raise TypeError("A key was inputed but a valid key type was not specified. Valid Key types are: basic, premium, deluxe, and ultra")
        





