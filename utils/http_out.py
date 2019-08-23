import demjson

def result_success(data):
    error_dict={}
    errors = {}
    errors['returnCode']=0
    errors['returnMessage'] = "ok"
    error_dict['error']=demjson.encode(errors)
    error_dict['data']=demjson.encode(data)
    return demjson.encode(error_dict)

def result_failed():
    error_dict = {}
    errors = {}
    errors['returnCode'] = -1
    errors['returnMessage'] = "failed"
    error_dict['error'] = demjson.encode(errors)
    error_dict['data'] = ''
    return demjson.decode(error_dict)