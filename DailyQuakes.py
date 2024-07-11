from datetime import datetime, date, timedelta, timezone

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import requests
from shapely.geometry import Point

from config_logging import configure_logging, log_execution_time

logging = configure_logging()

@log_execution_time(message="Fetching earthquake data from USGS API.")
def fetch_earthquake_data(starttime : str, endtime : str) -> dict:
    """
    Fetches earthquake data from the USGS Earthquake Catalog API.

    Parameters:
        - starttime (str): The start time for the data query in ISO 8601 format. (YYYY-MM-DDTHH:MM:SS)
        - endtime (str): The end time for the data query in ISO 8601 format. (YYYY-MM-DDTHH:MM:SS)

    Returns:
        - dict: A dictionary containing the earthquake data in GeoJSON format.
    """

    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endtime}"
    response = requests.get(url)
    earthquake_json = response.json()

    return earthquake_json

@log_execution_time(message="Processing earthquake data.")
def process_earthquake_data(earthquake_json : dict) -> pd.DataFrame:
    """
    Processes earthquake data and returns it as a pandas DataFrame.

    Parameters:
        - earthquake_json (dict): Earthquake data in GeoJSON format.

    Returns:
        - pd.DataFrame: A DataFrame containing the time, magnitude, longitude, latitude, and depth of each earthquake.
    """

    time_list, mag_list, lon_list, lat_list, depth_list = [], [], [], [], []

    for feature in earthquake_json["features"]:
        properties = feature["properties"]
        if properties["type"] == "earthquake":

            # Convert Unix time to a readable format
            time = datetime.fromtimestamp(properties["time"]/ 1000, tz=timezone.utc).strftime('%H:%M:%S')
            mag = properties["mag"]
            geometry = feature["geometry"]
            lon, lat, depth = geometry["coordinates"]
            
            time_list.append(time)
            mag_list.append(mag)
            lon_list.append(lon)
            lat_list.append(lat)
            depth_list.append(depth)
            
    return pd.DataFrame({
        "Time": time_list,
        "Magnitude": mag_list,
        "Longitude": lon_list,
        "Latitude": lat_list,
        "Depth": depth_list
    })

@log_execution_time(message="Generating Twitter message for earthquake data.")
def twitter_message(df : pd.DataFrame, starttime : str) -> str:
    """
    Generates a message to be posted on Twitter based on the earthquake data.

    Parameters:
        - df (DataFrame): Contains earthquake data with 'Time', 'Magnitude', 'Longitude', 'Latitude', and 'Depth' columns.

    Returns:
        - str: A message summarizing the earthquake data.
    """

    parsed_date = datetime.strptime(starttime, "%Y-%m-%d")
    formatted_date = parsed_date.strftime("%B %d, %Y")

    num_earthquakes = len(df)
    minor_earthquakes = len(df[df["Magnitude"].between(0, 1)])
    small_earthquakes = len(df[df["Magnitude"].between(1, 3)])
    moderate_earthquakes = len(df[df["Magnitude"].between(3, 5)])
    strong_earthquakes = len(df[df["Magnitude"].between(5, 7)])
    major_earthquakes = len(df[df["Magnitude"] >= 7])

    message = f"🌍 Global Earthquakes on {formatted_date}:\n\n"
    message += f"🔍 {num_earthquakes} Earthquakes detected.\n"
    message += f"🟢 {minor_earthquakes} ({(minor_earthquakes*100/num_earthquakes):.1f}%) Minor earthquakes (0-1)\n"
    message += f"🟡 {small_earthquakes} ({(small_earthquakes*100/num_earthquakes):.1f}%) Small earthquakes (1-3)\n"
    message += f"🟠 {moderate_earthquakes} ({(moderate_earthquakes*100/num_earthquakes):.1f}%) Moderate earthquakes (3-5)\n"
    message += f"🔴 {strong_earthquakes} ({(strong_earthquakes*100/num_earthquakes):.1f}%) Strong earthquakes (5-7)\n"
    message += f"⚫️ {major_earthquakes} ({(major_earthquakes*100/num_earthquakes):.1f}%) Major earthquakes (7+)"

    return message


def create_geodataframe(df : pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Converts a pandas DataFrame containing earthquake data into a GeoDataFrame.

    Parameters:
        - df (DataFrame): A pandas DataFrame with columns 'Longitude' and 'Latitude'.

    Returns:
        - GeoDataFrame: A geopandas GeoDataFrame with the specified CRS and geometry column.
    """

    earthquakes_geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

    return gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=earthquakes_geometry)

@log_execution_time(message="Plotting earthquake data on a world map.")
def plot_earthquakes(df : pd.DataFrame, filename : str) -> None:
    """
    Plots earthquake data on a world map and saves the figure.

    Parameters:
    - df (DataFrame): Contains earthquake data with 'Longitude', 'Latitude', and 'Magnitude' columns.
    - filename (str): Path and name of the file to save the plot.
    """

    # Define custom color map for earthquake magnitudes
    colors = ["white", "yellow", "#CD0000","#430000"]
    n_bins = 10
    cmap_name = "custom_hot"
    custom_hot = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

    # Create a plot with a Robinson projection
    fig, ax = plt.subplots(facecolor='black', subplot_kw={'projection': ccrs.Robinson()}, figsize=(20, 20))
    ax.patch.set_facecolor('black')

    # Plot earthquake data as scatter points
    scatter = ax.scatter(df["Longitude"], df["Latitude"], transform=ccrs.PlateCarree(),
                        s=30, c=df["Magnitude"], cmap=custom_hot, vmin=0, vmax=10, alpha=1, edgecolors='none')
    
    # Add land and borders with custom styling
    ax.add_feature(cfeature.LAND, edgecolor='white', facecolor='none', linewidth=0.75)
    ax.add_feature(cfeature.BORDERS, edgecolor='white', facecolor='none', linewidth=0.75)
    
    # Customize plot appearance
    plt.setp(ax.spines.values(), color='black')
    plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
    ax.set_xlim(-15000000, 15000000)
    ax.set_ylim(-7000000, 9000000)

    # Add and customize colorbar
    cbar = plt.colorbar(scatter, fraction=0.015, pad = 0.03)
    cbar.set_label('Magnitude', color='white', fontname='Inter', fontsize=12, labelpad=-15)
    plt.setp(cbar.ax.get_yticklabels(), color='white', fontname='Inter', fontsize=12)
    cbar.set_ticks([0, 10])  
    cbar.set_ticklabels(['0', '10'])  

    # Add text annotations
    fig.text(0.83, 0.675, "Earthquakes", color="white", ha="left", va="bottom", fontsize=18, fontname="Inter")
    fig.text(0.83, 0.663, datetime.strptime(filename, "%Y-%m-%d").strftime("%B %d, %Y"), color="white", ha="left", va="bottom", fontsize=12, fontname="Inter")
    fig.text(0.83, 0.647, "Data Source - USGS", color="white", ha="left", va="bottom", fontsize=10)
    fig.text(0.83, 0.637, "@TodayQuakes", color="white", ha="left", va="bottom", fontsize=10)

    # Save the figure
    plt.savefig(f"outputs/{filename}.png", dpi=300, bbox_inches='tight', facecolor='black')

def main():

    # Calculate the dates for fetching earthquake data
    today = date.today()
    yesterday = today - timedelta(1)
    starttime = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
    endtime = f"{today.year}-{today.month}-{today.day}"

    # Fetch and process earthquake data
    earthquake_json = fetch_earthquake_data(starttime=starttime, endtime=endtime)
    df = process_earthquake_data(earthquake_json=earthquake_json)
    earthquakes_geodata = create_geodataframe(df)
    plot_earthquakes(df, filename=starttime)

    logging.info(f"Earthquake data for {starttime} processed successfully. Saving to CSV at 'data/{starttime}.csv'.")
    df.to_csv(f"data/{starttime}.csv", index=False)

    logging.info(f"DailyQuakes.py executed successfully.")

if __name__ == "__main__":
    main()