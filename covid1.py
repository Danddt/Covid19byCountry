
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
                if item['popData2018'] not in pop:
                    pop.append(item['popData2018'])

        cases = [int(i) for i in cases] 
        deaths = [int(i) for i in deaths]
        pop = int(pop [0])
        country = str(country[0])

        tot_cases =sum((cases))
        tot_deaths = sum((deaths))
        per_cent_c =round((tot_cases/(pop)*100),2)
        per_cent_d = round((tot_deaths/(tot_cases)*100),2)



        final_str =  f'{country}\n\nRecorded cases: {tot_cases:,d} \n\nDeaths: {tot_deaths:,d}\n\nEstimated population in 2018: {pop:,d}\n\n% Cases in population: {per_cent_c}\n\n% Mortality in recorded cases: {per_cent_d}'
    except:
        final_str = 'There was a problem retrieving that information'

    return final_str

def get_data():
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    response = requests.get(url)
    source = response.json()
    
    label['text'] = format_response(source)



root = tk.Tk()
root.title('Covid19 by country')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage('background.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Data", font=40, command=get_data)
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font =  15 , anchor  = 'nw', justify ='left', bd = 5 )
label.place(relwidth=1, relheight=1)

root.mainloop()
