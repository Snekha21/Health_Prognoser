import pickle 
import pandas as pd
import pathlib
data_dir = pathlib.Path("/home/snekha/datasets/MOCK_DATA.csv")
data1=pd.read_csv(data_dir)
model = pickle.load(open('fin_model.pkl','rb'))
if(model.predict(data1) == 1):
    print('You are depressed')
else:
    print('You are not depressed')