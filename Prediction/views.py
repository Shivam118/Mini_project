from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib


def home(request):
    return render(request, 'Home.html')


def donate(request):
    return render(request, 'Donate.html')


def Hospitals(request):
    return render(request, 'BestHospitals.html')


def Check(request):
    return render(request, 'PredictionPage.html')


def Prediction(request):
    model = joblib.load('PredictionModel.sav') # Model Load using joblib
    
    age = request.GET.get('age','30')
    gender = request.GET.get('gender',2)
    height = request.GET.get('height','146')
    weight = request.GET.get('weight','60.0')
    ap_hi = request.GET.get('ap_hi','120')
    ap_lo = request.GET.get('ap_lo','80')
    chol = request.GET.get('chol',1)
    glucose = request.GET.get('glucose',1)
    smoke = request.GET.get('smoke',0)
    alco = request.GET.get('alcohol',0)
    active = request.GET.get('active',1)
    
    x_new = [age,gender,height,weight,ap_hi,ap_lo,chol,glucose,smoke,alco,active]
    # p_sample  = p_input(age,gender,height,weight,ap_hi,ap_lo,chol,glucose,smoke,alco)
    x_new[0] = int(age) # Age
    # Gender
    if gender=='m_gender':
        x_new[1] = 2
    elif gender=='f_gender':
        x_new[1] = 1

    x_new[2] = int(height) # Height
    x_new[3] = float(weight) # Weight
    x_new[4] = int(ap_hi)  # AP_hi
    x_new[5] = int(ap_lo)  # AP_lo
    # Cholestrol
    if chol=='n_chol':
        x_new[6] = 1
    elif chol=='an_chol':
        x_new[6] = 2
    elif chol=='wan_chol':
        x_new[6] = 3
    # Glucose
    if glucose=='n_glu':
        x_new[7] = 1
    elif glucose=='an_glu':
        x_new[7] = 2
    elif glucose=='wan_glu':
        x_new[7] = 3
    # Smoke
    if smoke=='yes_smoke':
        x_new[8] = 1
    elif smoke=='no_smoke':
        x_new[8] = 0
    # Alcohol 
    if alco=='no_alco':
        x_new[9] = 0
    elif alco=='yes_alco':
        x_new[9] = 1
    # Activity
    if active=='no_active':
        x_new[10] = 0
    elif active=='yes_active':
        x_new[10] = 1
    
    # x_new = np.array(x_new).reshape(-1, 10)
    p_sample=[]
    p_sample.append(x_new)

    final_pred = model.predict(p_sample)
    print(p_sample)
    print(final_pred)
    if final_pred[0] == 0:
        pred = {'Title':'Healthy','Desc': "You don't have any Heart-related Problems."}
    elif final_pred[0] == 1:
        pred = {'Title':'Not-Healthy','Desc': "High chances of you, might having Heart-Related Diseases ."}
    return render(request, 'PredictionOut.html', pred)


def graph(request): 
    drate = request.GET.get('death_rate')
    grate = request.GET.get('growth_rate')
    country_name = request.GET.get('country','india')
    if country_name == 'india':
        NoneParams={ 'CountryGraphNone': "Default Choosen - INDIA" }
    else:
        NoneParams={ 'CountryGraphNone': country_name }

    file_path = f'Prediction\\static\\GraphPlotting\\DeathAndGrowthRate.csv\\{country_name.upper()}.csv'
    data = pd.read_csv(file_path)
    year = data['Year']
    death_rate = data['Death Rate']
    growth_rate = data['Growth Rate']

    if drate is None and grate is None:
        return render(request, 'GraphNone.html',NoneParams)
    
    else:
        
        if drate=='on' and grate=='on':
            year = year.to_numpy()
            death_rate = death_rate.to_numpy()
            growth_rate = growth_rate.to_numpy()
            plt.clf()
            # Plotting Graph
            fig, gph = plt.subplots()
            gph.plot(year, death_rate, label="Death Rate", linewidth="1", color='r')
            gph.plot(year, growth_rate, label="Growth Rate", linewidth="1", color='g')
            gph_title = 'Life in ' + country_name
            gph.legend()  # Units
            gph.set_title(gph_title)  # Title of Graph
            gph.xaxis.set_label_text('Year')   # X-Axis Label
            gph.yaxis.set_label_text("RATE (in %age)")   # Y-Axis Label
            plt.savefig('Prediction\\Static\\Files\\plot.png', dpi=100)

        elif drate=='on':
            year = year.to_numpy()
            death_rate = death_rate.to_numpy()
            plt.clf()
            # Plotting Graph
            plt.plot(year,death_rate,label="Death Rate",linewidth="1",color='r')
            plt_title = 'Deaths in ' + country_name
            plt.legend()  # Units
            plt.title(plt_title)  # Title of Graph
            plt.xlabel('Year')   # X-Axis Label
            plt.ylabel("RATE (in %age)")   # Y-Axis Label
            plt.savefig('Prediction\\Static\\Files\\plot.png', dpi=100)

        elif grate=='on':
            year = year.to_numpy()
            growth_rate = growth_rate.to_numpy()
            plt.clf()
            # Plotting Graph
            plt.plot(year,growth_rate,label="Growth Rate",linewidth="1",color='g')
            plt_title = "Growth's in " + country_name
            plt.legend()  # Units
            plt.title(plt_title)  # Title of Graph
            plt.xlabel('Year')   # X-Axis Label
            plt.ylabel("RATE (in %age)")   # Y-Axis Label
            plt.savefig('Prediction\\Static\\Files\\plot.png', dpi=100)

        return render(request, 'Graph.html')

