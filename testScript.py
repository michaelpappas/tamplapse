import requests
import os
import datetime
import pytz
import time
from astral.sun import sun
from astral import LocationInfo

def download_image(url, save_folder):
    """
    Download an image from the given URL and save it to the specified folder
    with an incremented file name.

    Parameters:
    - url: The URL of the image to download.
    - save_folder: The folder where the image will be saved.
    """
    try:
        # Get the number of already existing files
        num_files = sum(1 for _ in os.listdir(save_folder) if _.startswith("image"))

        # Construct the file name with an incremented number
        file_name = f"image_{num_files + 1}.jpg"
        save_path = os.path.join(save_folder, file_name)

        # Send a GET request to the URL to fetch the image
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a file in binary write mode and write the content of the response
            with open(save_path, 'wb') as f:
                f.write(response.content)

            print(f"Image downloaded successfully and saved to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage:
    image_url = "https://cameras.alertcalifornia.org/public-camera-data/Axis-TamEast/latest-frame.jpg"
    save_folder = "./images"  # Save images in a folder named "images" within the current directory

    # Ensure the save folder exists, if not, create it
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Define the timezone (PST for this example)
    timezone = pytz.timezone('America/Los_Angeles')

    # Loop to execute every 30 seconds while there is daylight
    while True:
        # Get the current date and time in UTC
        current_time_utc = datetime.datetime.now(pytz.utc)

        # Convert the current time to the specified timezone
        # current_time = current_time_utc.astimezone(timezone)
        current_time = current_time_utc - datetime.timedelta(hours=7)

        # Get location information for calculating sunrise and sunset times
        city_info = LocationInfo("Your City", "Your Country", 'Your/Timezone')

        # Compute sunrise and sunset times
        s = sun(city_info.observer, date=current_time.date())

        # Convert sunrise and sunset times to UTC
        sunrise_utc = s["sunrise"].astimezone(pytz.utc)
        sunset_utc = s["sunset"].astimezone(pytz.utc)

        # Adjust the time range for downloading images (start 20 minutes before sunrise and end 20 minutes after sunset)
        start_time = sunrise_utc - datetime.timedelta(hours=1) + datetime.timedelta(hours=1)
        end_time = sunset_utc + datetime.timedelta(hours=2)

        # Check if the current time is within the time range for downloading images
        if start_time < current_time < end_time:
            # Download the image
            download_image(image_url, save_folder)
            print("current time-", current_time)
            print("start time-", start_time)
            print("end time-", end_time)
            time.sleep(30)  # Sleep for 30 seconds before downloading the next image
        else:
            print("It's not time to download images. Sleeping for 30 seconds...")
            print("current time-", current_time)
            print("start time-", start_time)
            print("end time-", end_time)
            time.sleep(30)  # Sleep for 30 seconds before checking again


