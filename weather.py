from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim 
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz 
from PIL import Image, ImageTk
import json

root = Tk()
root.title("Weather App")
root.geometry("890x470+300+200")
root.configure(bg="#57adff")
root.resizable(False, False)

def getWeather():
    try:
        city = textfield.get()
        geolocator = Nominatim(user_agent="MyWeatherApp123", timeout=10)
        location = geolocator.geocode(city)
        
        if not location:
            messagebox.showerror("Error", "City not found!")
            return
            
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        timezone.config(text=result)
        long_lat.config(text=f"{round(location.latitude, 4)}°N,{round(location.longitude, 4)}°E")
        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        
        # Current weather API
        current_api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&units=metric&appid=9ea35f88596c416324dc657306c76c8b"
        current_response = requests.get(current_api)
        current_data = current_response.json()
        
        # Forecast API
        forecast_api = f"https://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&units=metric&appid=9ea35f88596c416324dc657306c76c8b"
        forecast_response = requests.get(forecast_api)
        forecast_data = forecast_response.json()
        
        # Current weather
        temp = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        pressure = current_data['main']['pressure']
        wind = current_data['wind']['speed']
        description = current_data['weather'][0]['description']
        
        t.config(text=(temp, "°C"))
        h.config(text=(humidity,"%"))
        p.config(text=(pressure,"hPa"))
        w.config(text=(wind,"m/s"))
        d.config(text=description)
        
        # First cell (Today)
        firstdayimage = current_data['weather'][0]['icon']
        img1 = Image.open(f"icon/{firstdayimage}@2x.png")
        img1 = img1.resize((100, 100))
        photo1 = ImageTk.PhotoImage(img1)
        firstimage.config(image=photo1)
        firstimage.image = photo1
        
        temp_day = current_data['main']['temp']
        temp_night = current_data['main']['feels_like']
        day1temp.config(text=f"Day: {temp_day:.1f}°C\nNight: {temp_night:.1f}°C")
        
        # Calculate days and set their names
        today = datetime.now()
        days = []
        for i in range(7):  # 0 to 6 for all seven days
            next_day = today + timedelta(days=i)
            days.append(next_day)
        
        # Set day names
        day1.config(text=days[0].strftime("%A"))  # Today
        day2.config(text=days[1].strftime("%A"))  # Tomorrow
        day3.config(text=days[2].strftime("%A"))
        day4.config(text=days[3].strftime("%A"))
        day5.config(text=days[4].strftime("%A"))
        day6.config(text=days[5].strftime("%A"))
        day7.config(text=days[6].strftime("%A"))
        
        # Process forecast data
        daily_forecasts = []
        current_date = None
        for item in forecast_data['list']:
            forecast_date = datetime.fromtimestamp(item['dt']).date()
            if forecast_date != current_date:
                daily_forecasts.append(item)
                current_date = forecast_date
            if len(daily_forecasts) >= 6:  # Get 6 days of forecast
                break
        
        # Update cells 2-7 with forecast data
        for i, forecast in enumerate(daily_forecasts):
            frame_index = i + 2  # Start from second frame
            
            # Get the weather icon
            icon = forecast['weather'][0]['icon']
            img = Image.open(f"icon/{icon}@2x.png")
            img = img.resize((50, 50))
            photo = ImageTk.PhotoImage(img)
            
            # Update the appropriate frame
            if frame_index == 2:
                secondimage.config(image=photo)
                secondimage.image = photo
                day2temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
            elif frame_index == 3:
                thirdimage.config(image=photo)
                thirdimage.image = photo
                day3temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
            elif frame_index == 4:
                fourthimage.config(image=photo)
                fourthimage.image = photo
                day4temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
            elif frame_index == 5:
                fifthimage.config(image=photo)
                fifthimage.image = photo
                day5temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
            elif frame_index == 6:
                sixthimage.config(image=photo)
                sixthimage.image = photo
                day6temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
            elif frame_index == 7:
                seventhimage.config(image=photo)
                seventhimage.image = photo
                day7temp.config(text=f"Day: {forecast['main']['temp']:.1f}°C\nNight: {forecast['main']['feels_like']:.1f}°C")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Icon
image_icon = PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

Round_box = PhotoImage(file="Images/Rounded Rectangle 1.png")
Label(root, image=Round_box, bg="#57adff").place(x=30, y=110)

# Labels
label1 = Label(root, text="Temperature", font=('Helvetica', 11), fg="white", bg="#203243")
label1.place(x=50, y=120)

label2 = Label(root, text="Humidity", font=('Helvetica', 11), fg="white", bg="#203243")
label2.place(x=50, y=140)

label3 = Label(root, text="Pressure", font=('Helvetica', 11), fg="white", bg="#203243")
label3.place(x=50, y=160)

label4 = Label(root, text="Wind Speed", font=('Helvetica', 11), fg="white", bg="#203243")
label4.place(x=50, y=180)

label5 = Label(root, text="Description", font=('Helvetica', 11), fg="white", bg="#203243")
label5.place(x=50, y=200)

# Search box
search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
Label(root, image=search_image, bg="#57adff").place(x=270, y=120)

# Weather image
weather_image = PhotoImage(file="Images/Layer 7.png")
Label(root, image=weather_image, bg="#203243").place(x=290, y=127)

textfield = tk.Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
textfield.place(x=370, y=130)
textfield.focus()

search_icon = PhotoImage(file="Images/Layer 6.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
myimage_icon.place(x=645, y=125)

# Bottom box
frame = Frame(root, width=900, height=180, bg="#212120")
frame.pack(side=BOTTOM)

# Bottom boxes
firstbox = PhotoImage(file="Images/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
Label(frame, image=secondbox, bg="#212120").place(x=300, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=400, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=500, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=600, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=700, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=800, y=30)

# Clock
clock = Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=30, y=20)

# Timezone
timezone = Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone.place(x=700, y=20)

long_lat = Label(root, font=("Helvetica", 10), fg="white", bg="#57adff")
long_lat.place(x=700, y=50)

# thpwd
t = Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
t.place(x=150, y=120)
h = Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
h.place(x=150, y=140)
p = Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
p.place(x=150, y=160)
w = Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
w.place(x=150, y=180)
d = Label(root, font=("Helvetica", 11), fg="white", bg="#203243")
d.place(x=150, y=200)

# First cell
firstframe = Frame(root, width=230, height=132, bg="#282829")
firstframe.place(x=35, y=315)

day1 = Label(firstframe, font="arial 20", bg="#282829", fg="#fff")
day1.place(x=100, y=5)

firstimage = Label(firstframe, bg="#282829")
firstimage.place(x=1, y=15)

day1temp = Label(firstframe, bg="#282829", fg="#57adff", font="arial 15 bold")
day1temp.place(x=100, y=50)

# Second cell
secondframe = Frame(root, width=70, height=115, bg="#282829")
secondframe.place(x=305, y=325)

day2 = Label(secondframe, bg="#282829", fg="#fff")
day2.place(x=10, y=5)

secondimage = Label(secondframe, bg="#282829")
secondimage.place(x=7, y=20)

day2temp = Label(secondframe, bg="#282829", fg="#fff")
day2temp.place(x=2, y=70)

# Third cell
thirdframe = Frame(root, width=70, height=115, bg="#282829")
thirdframe.place(x=405, y=325)

day3 = Label(thirdframe, bg="#282829", fg="#fff")
day3.place(x=10, y=5)

thirdimage = Label(thirdframe, bg="#282829")
thirdimage.place(x=7, y=20)

day3temp = Label(thirdframe, bg="#282829", fg="#fff")
day3temp.place(x=2, y=70)

# Fourth cell
fourthframe = Frame(root, width=70, height=115, bg="#282829")
fourthframe.place(x=505, y=325)

day4 = Label(fourthframe, bg="#282829", fg="#fff")
day4.place(x=10, y=5)

fourthimage = Label(fourthframe, bg="#282829")
fourthimage.place(x=7, y=20)

day4temp = Label(fourthframe, bg="#282829", fg="#fff")
day4temp.place(x=2, y=70)

# Fifth cell
fifthframe = Frame(root, width=70, height=115, bg="#282829")
fifthframe.place(x=605, y=325)

day5 = Label(fifthframe, bg="#282829", fg="#fff")
day5.place(x=10, y=5)

fifthimage = Label(fifthframe, bg="#282829")
fifthimage.place(x=7, y=20)

day5temp = Label(fifthframe, bg="#282829", fg="#fff")
day5temp.place(x=2, y=70)

# Sixth cell
sixthframe = Frame(root, width=70, height=115, bg="#282829")
sixthframe.place(x=705, y=325)

day6 = Label(sixthframe, bg="#282829", fg="#fff")
day6.place(x=10, y=5)

sixthimage = Label(sixthframe, bg="#282829")
sixthimage.place(x=7, y=20)

day6temp = Label(sixthframe, bg="#282829", fg="#fff")
day6temp.place(x=2, y=70)

# Seventh cell
seventhframe = Frame(root, width=70, height=115, bg="#282829")
seventhframe.place(x=805, y=325)

day7 = Label(seventhframe, bg="#282829", fg="#fff")
day7.place(x=10, y=5)

seventhimage = Label(seventhframe, bg="#282829")
seventhimage.place(x=7, y=20)

day7temp = Label(seventhframe, bg="#282829", fg="#fff")
day7temp.place(x=2, y=70)

root.mainloop()