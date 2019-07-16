# IPGeo-Search

## About

IPGeo-Search is a python module which allows for easy use of the IPGeo API. It allows both free and paid users to send requests to the server in just one line of code, allowing for customization of how IP lists are loaded. We offer both a paid and free versions of our API on [Our Webpage](http://ipgeo.azurewebsites.net/).

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

The `search` function takes in 4 arguments:

```txt
ipList: an Array of IP's where each IP is a string

path: Where the result files are downloaded to

key(optional): The API Key if you use the paid version.

key_type(optional): Specifies what type of API key you are using
```

### Examples

#### Free Version

The IP List in this example is generated from a text document with an IP Address on each line.

```python
from IPGeoSearch import search
with open('ipList.txt', 'r') as f:
    ips = [line.strip() for line in f]
    f.close()

search.search(ipList=ips,path='path/for/download')
```

You can also have run a preprocessing script before which returns IP's into an IP list.

```python
ips = []

'''
Preprocessing Script that appends to ips
'''

search.search(ipList=ips,path='path/for/download')
```

#### Paid Version

To use the paid version, you must supply your key to the server as well as specify the key type.

```python
from IPGeoSearch import search

with open('ipList.txt', 'r') as f:
    ips = [line.strip() for line in f]
    f.close()

search.search(ipList=ips,path='path/for/download',key='key',key_type='key_type)
```

Valid Key types are `basic, premium, deluxe, or ultra`.

#### Errors

Common Errors are:

```python
TypeError: "An entry in ipList is not a string at line and cannot be read by the server"
ValueError: "Your IP List is longer than (10,1000,10000,100000) entires, which is more than alloted for your version. Sending it would result in an error from the server. Please shorten your list so that all your IP's may be processed."
RuntimeError: "You Have Exceded your Monthly search Limit"
TypeError: "A key type was inputed was not a valid key type. Valid Key types are: basic, premium, deluxe, and ultra"
TypeError: "A key was inputed but a valid key type was not specified. Valid Key types are: basic, premium, deluxe, and ultra"
```

If you receive an error like:

```python
RuntimeError: "Something went really wrong. Either the IP does not exist in the database, they key is not valid, server is down, or another error occured. Check x.x.x.x.json for more details and file an issue if you are unable to solve the problem."
```

File an issue so our team can assist you.
