import json
import requests
import datetime
import os.path

api_token = 'cf643d95-16d1-414d-9b5a-c99346720e37'
mes_date = 'https://api.weather.yandex.ru/v1/forecast?limit=-7&lat=55.75396&lon=37.620393&extra=false'
req = requests.get(mes_date, headers = {'X-Yandex-API-Key':api_token})
json_data = json.loads(req.text)

def collect_weather(): # collect data for today to data.json
    data = {}
    data['forecast'] = []
    infoData = []

    for day in json_data['forecasts']:
        infoData.append({'date' : day['date'],
                'temp' : day['parts']['day']['temp_avg']})
    newForecast = {
        'date' : str(datetime.date.today()),
        'info' : infoData
     }
    data['forecast'].append(newForecast)

    if os.path.isfile('data.json'): # check if file exist
        with open('data.json', 'r+') as f:
            datastore = json.load(f)
            try:
                datastore['forecast'].append(newForecast)
                print(json.dumps(datastore, indent = 4, sort_keys = True))
                f.close()
                with open('data.json', 'w') as f:
                    json.dump(datastore, f, indent = 4, sort_keys = True)
            except:
                print('json file is broken')
    else: # if file doesn't exist create
        with open('data.json', 'w') as f:
            json.dump(data,f, indent = 4, sort_keys = True)

def temperature_different(current, forecast):
    if current > forecast:
        return(str( int( 100 - (forecast/current) * 100) ) + '%')
    elif forecast > current:
        return(str( int( (forecast/current) * 100) - 100 ) + '%')
    else:
        return('0 %')

def compare_forecast(): # function to compare a current weather with previous forecasts
    cur_date = datetime.date.today()
    cur_temp = json_data['forecasts'][0]['parts']['day']['temp_avg']
    counter = 1
    with open('data.json', 'r') as f:
        datastore = json.load(f)
        for day in reversed(datastore['forecast']):
            if str(day['date']) != str(cur_date):
                for date in day['info']:
                    if str(date['date']) == str(cur_date):
                        if counter == 1:
                            mes = '1 день'
                        elif counter == 2 or counter == 3 or counter ==4:
                            mes = '{} дня'.format(counter)
                        else:
                            mes = '{} дней'.format(counter)
                        print('Сегодняшняя погода отличается от предсказанной {} назад на {}'.format(mes, temperature_different(cur_temp, int(date['temp']))))
                        counter += 1
                        break
compare_forecast()
