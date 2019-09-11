import os
def save_test_dataRdd(test_feature,label,file):
    if os.path.exists(file):
        os.remove(file)
    for feature,label in zip(test_feature.collect(),label.collect()):
        shop_id = int(feature[0])
        upc = int(feature[1])
        ai_weekday = int (feature[2])
        ai_day = str(feature[3])
        ai_nextday = str(feature[4])
        ai_day_nums = int(feature[5])
        ai_next_nums = int(feature[6])
        predict = label[0]
        line = str(shop_id)+","+str(upc)+","+str(ai_weekday)+","+str(ai_day)+","+str(ai_nextday)+","+str(ai_day_nums)+","+str(ai_next_nums)+","+str(predict)
        with open(file,'a+') as f :
            f.write(line+"\n")
