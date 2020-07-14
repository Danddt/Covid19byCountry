#packages
import tkinter as tk
import requests
import json

HEIGHT = 500
WIDTH = 600


def format_response(source):
    state = entry.get()
    #state = state.upper()
    try:
        country =[]
        cases = []
        deaths = []
        pop =[]
        for item in source['records']:
            if item['geoId'] == state.upper():

                cases.append(item['cases'])
                deaths.append(item['deaths'])
                if item['countriesAndTerritories'] not in country:
                    country.append(item['countriesAndTerritories'])
                if item['popData2019'] not in pop:
                    pop.append(item['popData2019'])

        cases = [int(i) for i in cases]
        negs =[]
        for i in cases:
            if i <0:
                i = 0
                negs.append(i)
            else:
                negs.append(i)
        
        deaths = [int(i) for i in deaths]
        pop = int(pop [0])
        country = str(country[0])

        tot_cases =sum((negs))
        tot_deaths = sum((deaths))
        per_cent_c =round((tot_cases/(pop)*100),2)
        per_cent_d = round((tot_deaths/(tot_cases)*100),2)



        final_str =  f'{country}\n\nRecorded cases: {tot_cases:,d} \n\nDeaths: {tot_deaths:,d}\n\nEstimated population in 2019: {pop:,d}\n\n% Cases in population: {per_cent_c}\n\n% Mortality in recorded cases: {per_cent_d}'
    except:
        final_str = 'There was a problem retrieving that information'

    return final_str

def get_data():
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'
    response = requests.get(url)
    source = response.json()
    
    label['text'] = format_response(source)



root = tk.Tk()
root.title('Covid 19 data by country')


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg = '#a9dbe7')
canvas.pack()

canvas.create_text(220,40,fill="#262262",font="Times 10 italic bold",
                        text="Enter country/state code e.g UK for United Kingdom.")

canvas.create_text(220,450,fill="black",font="Times 10 italic bold",
                        text="Source: https://opendata.ecdc.europa.eu/covid19")



frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.85, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Data", font=40, command=get_data)
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.85, relheight=0.6, anchor='n')


label = tk.Label(lower_frame, font =  15 , anchor  = 'nw', justify ='left', bd = 5 )
label.place(relwidth=1, relheight=1)
w = tk.Label(root, text="Hello Tkinter!")

root.mainloop()