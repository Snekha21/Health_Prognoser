from flask import Flask, request, url_for, redirect, render_template
import pandas as pd
import json 
# from json import jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)
import pathlib
import pickle
import cv2

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('home'))
    # show the form, it wasn't submitted
    return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def about_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('About'))
    # show the form, it wasn't submitted
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('Login'))
    # show the form, it wasn't submitted
    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('Main'))
    # show the form, it wasn't submitted
    return render_template('Main.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('Contact'))
    # show the form, it wasn't submitted
    return render_template('contact.html')

# @app.route('/result', methods=['GET', 'POST'])
# def result_func():
#     if request.method == 'POST':
#         # do stuff when the form is submitted
#         # redirect to end the POST handling
#         # the redirect can be to the same route or somewhere else
#         return redirect(url_for('result'))
#     # show the form, it wasn't submitted
#     return render_template('result.html')

@app.route('/input', methods=['GET', 'POST'])
def test_func():
    if request.method == 'POST':
        # data = request.form.get("q1")
        # for key, value in request.form.items():
        #     print("key: {0}, value: {1}".format(key, value))

        # data=console.log(JSON.stringify(input))
        # data1 =json.loads(request.json)
        # data = request.form.get("q1")
        # data = request.json
        data= request.form
        # data = json.dump(request.get_json(force=True))
        # with open('file.json', 'w') as f:
        #   json.dump(request.get_json(force=True), f)
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        print(data)
        # print(data1)
        convertJsonToCsv(data)
        return redirect(url_for('result'))
        # return render_template('result.html')
    return render_template('index.html')
    # show the form, it wasn't submitted
    # return render_template('index.html')

@app.route("/image")
def image():
#   if request.method == "POST":
#     image = request.files.get('img', '')
#     image = request.form["img"]

#     print("img ",image)
#     return "<h1> yo! </h1>"
#   else:
    return render_template('image.html') 

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['File']
        # file = f.filename
        f.save(secure_filename("image.jpg"))
        return "File saved successfully"

@app.route("/test", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        return redirect(url_for('test'))
    
    return render_template('index.html')


def convertJsonToCsv(jsonData):
    dfs = []
    dfs.append(pd.DataFrame([jsonData]))
    df = pd.concat(dfs, ignore_index=True, sort=False)
    # df.drop(['userName'], 
    #     axis = 1, inplace = True)
    df.to_csv('input.csv',index=False)

@app.route("/result")
def result():
    data_dir = pathlib.Path("input.csv")
    data1=pd.read_csv(data_dir)
    # data1['Average'] = data1.mean(axis=1)
    # data1.drop(['Monday','Tuesday','Wednesday','Thursday','Friday'],axis = 1, inplace = True)
    # fmodel = pickle.load(open('fin_model.pkl','rb'))
    # model = pickle.load(open('fin_model.pkl','rb'))
    # if(model.predict(data1) == 0):
    #     return  {"output":"You are depressed"}
    # else:
    #     return {"output":"You are not depressed"}
    # data1 = data1.astype(float)
    model = pickle.load(open('lr_model.pkl','rb'))
    if(model.predict(data1) == 1):
        html_data= "You are depressed"
        result = "You are showing symptoms of depression"
        cmt= "You are adviced to contact your doctor and get treated asap"
    elif(model.predict(data1) == 0):
        html_data = "You are not depressed"
        result = "Congrats! You are not showing symptoms of depression"
        cmt = "Stay happy and healthy"
    print(model.predict(data1))
    return render_template("result.html", html_data = html_data , result=result, cmt=cmt)

@app.route("/img")
def mri():
      test=[]
      img_array=cv2.imread("image.jpg")
      CATEGORIES = ['healthy','depressed']
      class_num=CATEGORIES.index(category)
      new_array=cv2.resize(img_array,(100,100))
      test.append([new_array,class_num])
    # data1['Average'] = data1.mean(axis=1)
    # data1.drop(['Monday','Tuesday','Wednesday','Thursday','Friday'],axis = 1, inplace = True)
    # fmodel = pickle.load(open('fin_model.pkl','rb'))
    # model = pickle.load(open('fin_model.pkl','rb'))
    # if(model.predict(data1) == 0):
    #     return  {"output":"You are depressed"}
    # else:
    #     return {"output":"You are not depressed"}
    # data1 = data1.astype(float)
      model = pickle.load(open('image.pkl','rb'))
      if(model.predict(test) == 1):
        html_data= "You are depressed"
        result = "You are showing symptoms of depression"
        cmt= "You are adviced to contact your doctor and get treated asap"
      elif(model.predict(test) == 0):
        html_data = "You are not depressed"
        result = "Congrats! You are not showing symptoms of depression"
        cmt = "Stay happy and healthy"
      print(model.predict(test))
      return render_template("result.html", html_data = html_data , result=result, cmt=cmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)


    