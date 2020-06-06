'''need to destroy graphs after generation'''


import tkinter as tk

import requests
import json


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np



def data(source):
    
    state = entry.get()
    state= state.upper()   

    
    
    country =[]
    cases = []
    deaths = []
    pop =[]
    date =[]

    for item in source['records']:
        if item['geoId'] == state:
            date.append(item['dateRep'])
            cases.append(item['cases'])
            deaths.append(item['deaths'])
            if item['countriesAndTerritories'] not in country:
                country.append(item['countriesAndTerritories'])
            if item['popData2018'] not in pop:
                pop.append(item['popData2018'])
        
            

    cases = [int(i) for i in cases]
    
    for n, i in enumerate(cases):
        if i < 0:
            cases[n] = 0

    deaths = [int(i) for i in deaths]

    pop = int(pop [0])
    country= str(country[0])


    tot_cases =sum((cases))
    tot_deaths = sum((deaths))
    per_cent_c =round((tot_cases/(pop)*100),2)
    per_cent_d = round((tot_deaths/(tot_cases)*100),2)

    cases_r = cases[::-1]
    
    start = next(x[0] for x in enumerate(cases_r) if x[1] > 0)
    cases_ro = cases_r[start:]
    deaths_r = deaths[::-1]
    deaths_ro = deaths_r[start:]
    date_r =  date[::-1]
    date_ro = date_r[start:]
    
    

    
    global figure1
    global bar1
    
    canvas_1 = tk.Canvas(root, bg = 'white')
    canvas_1.pack()
    
    figure1 = plt.Figure(figsize=(6,5), dpi=100)

    ax1 = figure1.add_subplot(111)

    p1 = ax1.bar(date_ro,cases_ro)
    p2= ax1.bar(date_ro,deaths_ro)
    ax1.set_xticks(np.arange(0,len(date), step=(len(date))/5))
    ax1.legend((p1[0], p2[0]), ('Recorded Cases', 'Deaths') )
    ax1.set_xlabel('date format : day/month/year')
    ax1.set_ylabel('Cases')
    ax1.set_title(country)
    
    
    bar1 = FigureCanvasTkAgg(figure1, canvas_1)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    bar1.draw()
    
    def quit():

        canvas_1.destroy()

    
    button_1 = tk.Button(canvas_1, text="Clear Graph", font=40, command= quit)
    button_1.pack(side= tk.RIGHT)
  
    
    return f'{country}\n\nRecorded cases: {tot_cases:,d} \n\nDeaths: {tot_deaths:,d}\n\nEstimated population in 2018: {pop:,d}\n\n% Cases in population: {per_cent_c}\n\n% Mortality in recorded cases: {per_cent_d}\n\n\n source: www.ecdc.europa.eu'




def get():
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    response = requests.get(url)
    source = response.json()
    
    label['text'] = data(source)
        
HEIGHT = 400
WIDTH = 600

root= tk.Tk() 
root.title('Covid19 Data')
root.configure(bg='white')


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg = 'white')
canvas.pack()
canvas.create_text(220,30,fill="#262262",font="Times 10 italic bold",
                        text="Enter country/state code e.g UK for United Kingdom.")
frame = tk.Frame(canvas, bg='#99dcec', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1.2)


button = tk.Button(frame, text="Get Data", font=40, command= get)
button.place(relx=0.7, relheight=1.2, relwidth=0.3)

lower_frame =  tk.Frame(canvas, bg='#99dcec', bd=5)
lower_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.8, anchor='n')

label = tk.Label(lower_frame, font =  15 , anchor  = 'nw', justify ='left', bd = 5 )
label.place(relwidth=1, relheight=1)



root.mainloop()