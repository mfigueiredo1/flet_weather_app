import flet as ft
import requests
from api_key import API_KEY

# Build out the API and get a response
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
MAP_URL = "https://www.openstreetmap.org/export/embed.html?bbox=lon1,lat1,lon2,lat2&layer=mapnik"

def get_weather(city):
    params = {"q":city, "appid": API_KEY, "units": "metric"} # Use metric for Celsius
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "city" : data["name"],
            "temp" : data["main"]["temp"],
            "humidity" : data["main"]["humidity"],
            "weather" : data["weather"][0]["description"],
            "lat" : data["coord"]["lat"],
            "lon" : data["coord"]["lon"]
        }
    return None

       
#print(get_weather("paris")) # Example call to the function to test it

def main(page: ft.Page):
    page.title = "Flet my Weather"
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700

    city_input = ft.TextField(
        label = "Enter City", 
        width=300,
        bgcolor=ft.colors.WHITE,
        color=ft.colors.BLACK,
        border_radius=10

    )

    results_text = ft.Text("",size=18,weight=ft.FontWeight.BOLD,color=ft.colors.WHITE) # Text widget to show results
 
    # Call and get the weather data
    def search_weather(e):
        city=city_input.value.strip() # Get the value from the TextField and strip any extra spaces
        if not city:
            results_text.value = "Please enter a city name..."
            page.update()
            return
        weather_data = get_weather(city)

        if weather_data:
            results_text.value = f"City: {weather_data['city']}\nTemperature: {weather_data["temp"]}°C\nHumidity: {weather_data['humidity']}%\nWeather: {weather_data["weather"]}"

        else:
            results_text.value = "City not found. Try again..."

        page.update() # Update the page to reflect the changes in results_text

        



    # Search Button

    search_button = ft.ElevatedButton(
        "Search",
        on_click=search_weather, # Bind the search_weather function to the button click
        bgcolor=ft.colors.BLUE_500, # Button color
        color=ft.colors.WHITE, # Text color
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=10)
    )

    # Container to hold my UI
    container = ft.Container(
        content=ft.Column(

            alignment=ft.MainAxisAlignment.CENTER, # Center align the column
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Center align the items horizontally
            controls=[
                ft.Text("Flet my Weather", size=30, weight=ft.FontWeight.BOLD,color=ft.colors.WHITE),
                city_input, # TextField for city input
                search_button, # Search button
                results_text # Text widget to show results

            ],
        ),
        alignment = ft.alignment.center,
        padding=20,
        border_radius=15,
        bgcolor=ft.colors.BLUE_GREY_800, # Background color of the container
        shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color=ft.colors.BLACK12) # Shadow effect for the container

    )

    # Add the container to the page
    page.add(container)




if __name__ == "__main__":
    """
    Entry point for the Flet application.
    """
    # Start the Flet app
    ft.app(target=main) # This will start the Flet application with the main function as the entry point




# Build out the API and 