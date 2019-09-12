import requests
def put(url,querystr,header):
    if querystr!=None and querystr!="":
        # data=eval(querystr)
        res=requests.put(url,header=header,data=querystr)
        result=res.text
        print(result)
        res=requests.put(url)
        result=res.text
        print(result)

if __name__=='__main__':
    #curl -X PUT -d'{"upc":"123","xmin":830,"ymin":1555,"xmax":968,"ymax":2128"}'  'http://192.168.1.60:8001/api/shelfgoods/54380/'
    url = 'http://192.168.1.60:8001/api/shelfgoods/54380/'
    header = {
    'Content-Type: application/json',}
    querystr = '{"upc":"123","xmin":830,"ymin":1555,"xmax":968,"ymax":2128"}'
    put(url,querystr,header)