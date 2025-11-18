from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import urllib.parse

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def getWeather():
    try:
        city = textfield.get().strip()

        if city == "":
            messagebox.showerror("Weather App", "Please enter a city name.")
            return

        # --- GEOLOCATION ---
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)

        if location is None:
            messagebox.showerror("Weather App", "City not found! Try another.")
            return

        # --- TIMEZONE ---
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        if result is None:
            messagebox.showerror("Weather App", "Timezone not found!")
            return

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # --- WEATHER API ---
        city_encoded = urllib.parse.quote(city)
        api_key = "166db791c3a44d1071f846cb61d105e5"
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}"

        json_data = requests.get(api_url).json()

        # Check API response
        if json_data.get("cod") != 200:
            messagebox.showerror("Weather App", "Weather data not found!")
            return

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        # Update UI
        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")

        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

    except Exception as e:
        messagebox.showerror("Weather App", f"Something went wrong!\n{e}")


# ---------------- UI ELEMENTS ----------------
Search_image = PhotoImage(file="Search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"),
                     bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="Search_box.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2",
                      bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

# Logo
Logo_image = PhotoImage(file="Logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom frame
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time Label
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Weather labels
t = Label(font=("arial", 70, "bold"))
t.place(x=400, y=150)

c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

# Bottom indicators
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'),
               fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'),
               fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'),
               fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'),
               fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

# Value labels
w = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
