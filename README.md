# IPGeo-Search

## About

IPGeo-Search is a python module which allows for easy use of the [IPGeo API](https://github.com/MatthiasRathbun/IPGeo). It allows both free and paid users to send requests to the server in just one line of code, allowing for customization of how IP lists are loaded. We offer a 5 day free trial for our API on [Our Webpage](http://ipgeo.azurewebsites.net/). To get the free trial API Key, contact our Lab and we will send it to you.

To Install IPGeoSearch, run

```cmd
pip install IPGeoSearch
```

## Requirements

Before running on your local computer, make sure you have `python 3.6+` with the latest version of `pandas` installed.

To Install Pandas, run:

```cmd
pip install pandas
```

## Usage

The `search` function takes in 3 arguments:

```txt
ipList: an Array of IP's where each IP is a string.

path: Where the result files are downloaded to.

key: The API Key sent to you.

```

### Example

To use the either version, you must supply your key to the server.

```python
from IPGeoSearch import search

with open('ipList.txt', 'r') as f:
    ip = [line.strip() for line in f]
    f.close()

with open('yourkey.key', 'r') as hashkey:
    key=hashkey.read().replace('\n', '')
    hashkey.close()

search.search(ipList=ip,path='',key=key)
```

#### Errors

Common Errors are:

```python
TypeError: "An entry in ipList is not a string at line and cannot be read by the server"
RuntimeError: "Your Key is Invalid. Please purchase a key or start a trial."
RuntimeError: "Your Trial Period has expired. Please purchase a key."
RuntimeError: "Your Key has expired. Please purchase a new key."
RuntimeError: "The Network you are using in unknown and key cannot be secured. Please change networks."
RuntimeError: "Your Key is being used on a different network than it was registered on. Please use your original network or purchase a new key for this network."
ValueError: "IP list was not specified."
ValueError: "Key was not specified."
```

If you receive an error like:

```python
RuntimeError: "Something went really wrong. Either the IP does not exist in the database, server is down, or another error occured. Check x.x.x.x.json for more details and file an issue if you are unable to solve the problem."
```

File an issue so our team can assist you.
