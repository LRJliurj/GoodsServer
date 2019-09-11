#测试精准率
test_path = "D:\\opt\\data\\linear\\predict_test1\\"
import os
import math
def count_p ():
    files = os.listdir(test_path)
    i = 0.0
    j = 0.0
    for file in files:
        file_path = os.path.join(test_path,file)
        with open(file_path,'r') as f:
            lines = f.readlines()
            for line in lines:
                i+=1
                true_l = int(float(str(line).split(",")[0]))
                predict_l = int(math.floor(float(str(line).split(",")[1])))
                if true_l < 10 and abs(true_l-predict_l) <= 1:
                    j += 1
                elif  true_l >10 and abs(true_l-predict_l) <= int(true_l*0.05) :
                    j += 1

    print (i)
    print (j)
    print (float(j)/i)

if __name__=='__main__':
    count_p()