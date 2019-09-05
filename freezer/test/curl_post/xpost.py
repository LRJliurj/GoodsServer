import os
import subprocess
import time
jpg_path = "D:\\opt\\data\\freezer\\20190902\\20190902_15\\"

paths = os.listdir(jpg_path)
for path in paths :
    j_p = os.path.join(jpg_path,path)
    for jpg in os.listdir(j_p):
        file= os.path.join(j_p,jpg)
        curl_shell = 'curl -XPOST "http://ai.fastxbox.cn/api/freezerimage/" -F"source=@'+file+'" -F"deviceid=123"'
        print (curl_shell)
        return_code = subprocess.call(curl_shell, shell=True)
        print(return_code)
        time.sleep(3)

