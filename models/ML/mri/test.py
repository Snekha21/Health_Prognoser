# Import libraries
from crypt import methods
import numpy as np
from flask import Flask, render_template, request, redirect, jsonify, redirect, url_for, flash, session
import pickle
import os
import tensorflow as tf
from tensorflow import keras
from werkzeug.utils import secure_filename
import os
import shutil
import time


from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

app = Flask(__name__)
app.secret_key = 'super secret key'


from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

# Load the model
#path_to_model = pickle.load(open('./mlruns/1/ea6f72cc45764f50828f57af62db9faf/artifacts/model/model.pkl','rb'))


model = tf.keras.models.load_model('mri_model',custom_objects={'f1_m':f1_m,'precision_m':precision_m,'recall_m':recall_m})

UPLOAD_PATH = "static/"
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        print("POST")
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return url_for("predict",filename=filename)

        fil = "./static/" + filename 

        # fil = "/home/snekha/tact/datasets/test/AIS001.jpg"

        img = tf.keras.utils.load_img(
            fil, target_size=(256, 256)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        class_names=["Depressed","Healthy"]
        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(class_names[np.argmax(score)], 100 * np.max(score))
        # )
        #session['pred'] = '"This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))'
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
        #pred = "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
        return redirect(url_for("show_result"))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html")



@app.route("/result",methods=["GET","POST"])
def show_result():
    pred = session.get('pred', None)
    return render_template("result.html",result=pred)


if __name__ == '__main__':


    app.run(port=5050, debug=True)
