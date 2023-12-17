import json
import math
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import requests
from PIL import Image, ImageTk
from io import BytesIO


class Main():
    def __init__(self, root):
        self.currentDate = datetime.now()
        self.root = root
        self.root.title("Weather App || Design by ABC ltd.")
        self.root.geometry('350x350+500+200')
        self.root.resizable(False, False)
        self.root.bind("<Return>", lambda event: self.searchTemperature())

        self.title1 = "Python Weather App"
        self.title2 = "Real-time Weather Updates with Tkinter GUI"
        self.customFont = ('aerial', 12, 'bold')
        self.customFontSmall = ('aerial', 9, 'bold')
        self.customFontMedium = ('aerial', 20, 'bold')

        self.LabelCity = Label(self.root, text=self.title1, font=self.customFont)
        self.LabelCity.pack()
        self.LabelCity1 = Label(self.root, text=self.title2, font=self.customFontSmall)
        self.LabelCity1.pack()

        self.entryCity = Entry(self.root, font=('aerial', 12), relief=GROOVE,
                               bg='#d2fadd')
        self.entryCity.place(x=10, y=50, width=200, height=35)

        self.searchButton = Button(self.root, text="Search", command=self.searchTemperature, font=self.customFont,
                                   cursor='hand2', relief=GROOVE, bg='#24b54b', fg='white')
        self.searchButton.place(x=220, y=50, width=120, height=35)

        self.darkBackground = '#4e5561'
        self.daylabelBackground = '#282829'
        self.unit = '°C'

        self.FrameWeather = Frame(self.root, bg=self.darkBackground)
        self.FrameWeather.place(x=10, y=100, width=330, height=240)

        self.CityName = Label(self.FrameWeather, font=self.customFontMedium, bg=self.darkBackground,
                              fg='white')
        self.CityName.place(x=10, y=10)

        self.dayLabel = Label(self.FrameWeather, text="Today", bg=self.daylabelBackground, font=self.customFont,
                              fg='white')
        self.dayLabel.place(x=10, y=50, width=80, height=35)

        self.dayName = Label(self.FrameWeather, bg=self.darkBackground, font=self.customFontSmall,
                             fg='white')
        self.dayName.place(x=100, y=50)
        self.timeLabel = Label(self.FrameWeather, bg=self.darkBackground, font=self.customFontSmall,
                               fg='white')
        self.timeLabel.place(x=100, y=65)

        self.displayIcon = Label(self.FrameWeather, bg=self.darkBackground)
        self.displayIcon.place(x=30, y=90)
        self.displayIconDescription = Label(self.FrameWeather, bg=self.darkBackground,
                                            font=self.customFont, fg='white')
        self.displayIconDescription.place(x=55, y=190)

        self.displayFeels = Label(self.FrameWeather, text='Feels like ~', bg=self.darkBackground,
                                  font=self.customFontMedium, fg='white')
        self.displayFeels.place(x=170, y=10)

        self.displayTemperature = Label(self.FrameWeather, bg=self.darkBackground, font=('aerial', 80), fg='white')
        self.displayTemperature.place(x=170, y=40)

        self.displayTemperatureUnit = Label(self.FrameWeather, text=self.unit, bg=self.darkBackground,
                                            font=self.customFontMedium, fg='white')
        self.displayTemperatureUnit.place(x=290, y=60)

        self.displayPressure = Label(self.FrameWeather, bg=self.darkBackground,
                                     font=self.customFontSmall, fg='white')
        self.displayPressure.place(x=170, y=160)
        self.displayHumidity = Label(self.FrameWeather, bg=self.darkBackground,
                                     font=self.customFontSmall, fg='white')
        self.displayHumidity.place(x=170, y=180)
        self.displayWind = Label(self.FrameWeather, bg=self.darkBackground,
                                 font=self.customFontSmall, fg='white')
        self.displayWind.place(x=170, y=200)

    def loadImageUrl(self, iconName):
        self.weatherIconURL = f"https://openweathermap.org/img/wn/{iconName}@2x.png"
        self.response = requests.get(self.weatherIconURL)
        self.img_data = BytesIO(self.response.content)
        self.img = Image.open(BytesIO(self.response.content))
        return ImageTk.PhotoImage(self.img)

    def searchTemperature(self):
        self.search(self.entryCity.get())

    def search(self, item="Kathmandu"):
        try:
            if item == '':
                messagebox.showwarning('Error', 'Please! enter city', parent=self.root)
            elif item.isalpha():
                self.weatherData = self.getWeatherData(item)
                if 'main' in self.weatherData:
                    self._extracted_from_search_10()
                else:
                    messagebox.showwarning('Error', self.weatherData["message"], parent=self.root)
            else:
                messagebox.showwarning('Error', 'No, number and special character', parent=self.root)
        except KeyError:
            messagebox.showwarning('Error', 'Please enter city name correctly.', parent=self.root)

    def _extracted_from_search_10(self):
        self.icon = self.weatherData["weather"][0]["icon"]
        self.weatherIcon = self.loadImageUrl(self.icon)

        self.displayTemperature.config(text=int(math.floor(self.weatherData["main"]["temp"])))
        self.displayPressure.config(text=f'Pressure: {self.weatherData["main"]["pressure"]}')
        self.displayHumidity.config(text=f'Humidity: {self.weatherData["main"]["humidity"]}%')
        self.displayWind.config(text=f'Wind: {self.weatherData["wind"]["speed"]}km/hr')
        self.CityName.config(text=self.weatherData["name"])
        self.dayName.config(text=self.currentDate.strftime("%A"))
        self.timeLabel.config(text=self.currentDate.strftime("%I:%M:%S %p"))
        self.displayIcon.config(image=self.weatherIcon)
        self.displayIconDescription.config(text=self.weatherData["weather"][0]["main"])

    def getWeatherData(self, cityName):
        api_url = f'https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid=3906112ba835b33431dee8ab5ac98b25&units=metric'
        weatherData = requests.get(api_url)
        return json.loads(weatherData.text)


if __name__ == '__main__':
    root = Tk()
    newObj = Main(root)
    newObj.search()
    root.mainloop()
