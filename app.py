from flask import Flask,request,render_template,url_for,redirect
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def hello_world():
    return render_template("forest.html")
@app.route('/')
def contact():
    return render_template("Contact.html")

@app.route('/Home.html')
def home():
    return render_template("Home.html")
@app.route('/analysis.html')
def analysis():
    return render_template("analysis.html")
@app.route('/about.html')
def about():
    return render_template("about.html")



@app.route('/predict_crime',methods=['POST','GET'])
def predict_crime():
    features =[]
    days     = {"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5,"Saturday":6,"Sunday":7}
    district = {'NORTHERN': 1,'PARK': 2,'INGLESIDE': 3,'BAYVIEW': 4,'RICHMOND': 5,'CENTRAL': 6,'TARAVAL': 7,
                'TENDERLOIN':8,'MISSION': 9,'SOUTHERN': 10}
    op = {26:'ARSON', 8:'ASSAULT', 36:'BAD CHECKS', 29:'BRIBERY', 18:'BURGLARY', 25:'DISORDERLY CONDUCT', 
          22:'DRIVING UNDER THE INFLUENCE', 14:'DRUG/NARCOTIC', 12:'DRUNKENNESS', 30:'EMBEZZLEMENT', 34:'EXTORTION',
          27:'FAMILY OFFENSES', 13:'FORGERY/COUNTERFEITING', 19:'FRAUD', 35:'GAMBLING', 20:'KIDNAPPING',
          3: 'LARCENY/THEFT', 28:'LIQUOR LAWS', 32:'LOITERING', 18:'MISSING PERSON', 6:'NON-CRIMINAL',2:'OTHER OFFENSES',
          39:'PORNOGRAPHY/OBSCENE MAT', 24:'PROSTITUTION', 38:'RECOVERED VEHICLE', 7:'ROBBERY', 21:'RUNAWAY', 
          16:'SECONDARY CODES', 23:'SEX OFFENSES FORCIBLE', 33:'SEX OFFENSES NON FORCIBLE', 15:'STOLEN PROPERTY', 
          31:'SUICIDE', 11:'SUSPICIOUS OCC', 37:'TREA', 17:'TRESPASS', 5:'VANDALISM', 4:'VEHICLE THEFT', 1:'WARRANTS', 
          9:'WEAPON LAWS'}
    for x in request.form.values():
        if x in days.keys():
            features.append(days[x])
        elif x in district.keys():
            features.append(district[x])
        else:
            features.append(float(x))
    
    final = np.array(features)
    final = final.reshape(1,-1)

    prediction=model.predict(final)

    # return render_template('forest.html',pred="There's a probability of {}".format(prediction))
    
    if prediction[0] in op.keys():
        return render_template('forest.html',pred="There's a probability of {} at given place".format(op[prediction[0]]))


if __name__ == '__main__':
    app.run(debug=True)