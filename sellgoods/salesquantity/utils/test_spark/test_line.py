from sellgoods.salesquantity.linear_regression import Linear
from set_config import config
from sellgoods.salesquantity.utils.test_spark import rdd
import os

num_iter_first=config.linear_params['num_iter_first']
step_size=config.linear_params['step_size']
mini_batch_frction=config.linear_params['mini_batch_frction']
num_iter_alter = config.linear_params['mini_batch_frction']

linear = Linear()
label_features,sc = rdd.filter()
model = linear.get_model(label_features,1000,step_size,mini_batch_frction)
print (model.weights)
model_path = "linear.pkl"
if os.path.exists(model_path):
    os.removedirs(model_path)
else :
    model.save(sc,"linear.pkl")

