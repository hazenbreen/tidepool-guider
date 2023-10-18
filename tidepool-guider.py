import requests
from bs4 import BeautifulSoup
from datetime import datetime
import inquirer


baseURL = "https://www.tide-forecast.com/locations/{}/tides/latest"
locations = [
    "Half-Moon-Bay-California", 
    "Huntington-Beach", 
    "Providence-Rhode-Island", 
    "Wrightsville-Beach-North-Carolina"
]

def getTideData(requestedLocation):
    """
    Scrapes the website and gathers the data for daytime low tides
    Args:
        requestedLocation (string): the location the user wants to learn about

    Ret:
        list of dictionaries containing a day and the corresponding tide data
    """

    page = requests.get(baseURL.format(requestedLocation))
    soup = BeautifulSoup(page.content, "html.parser")
    dayTables = soup.find_all("div", class_="tide-day")

    # Get all the low tide data and put it into list of dictionaries. 
    # Dictionary consists of day and corresponding data
    allDaylightLowTides = []
    for table in dayTables:
        date = table.find(class_="tide-day__date").text.split(':')[1].strip()

        # find sunrise and sunset
        sunMoonTable = table.find(class_="not-in-print tide-day__sun-moon")
        sunTimes = sunMoonTable.find_all(class_="tide-day__value")
        sunrise = sunTimes[0].text.strip()
        sunset = sunTimes[1].text.strip()
        sunriseTime = datetime.strptime(sunrise, '%I:%M%p').time()
        sunsetTime = datetime.strptime(sunset, '%I:%M%p').time()

        # find lowtide(s) that are during daylight
        tideTable = table.find(class_="tide-day-tides")
        singleDayDaylightLowTides = []
        for row in tideTable:
            if "Low Tide" in row.text:
                lowTides = row.find('b')
                for lowTide in lowTides:
                    try:
                        lowTideTime = datetime.strptime(lowTide.strip(), '%I:%M %p').time()
                    except ValueError:
                        # Catch an error where 00:00 to 01:00 is listed in 24hr format
                        lowTideTime = datetime.strptime(lowTide.split()[0].strip(), '%H:%M').time()

                    if sunriseTime <= lowTideTime <= sunsetTime:
                        tideHeight = row.find(class_="js-two-units-length-value__primary").text
                        singleDayDaylightLowTides.append({
                            "time": lowTideTime, 
                            "height": tideHeight
                        })

        allDaylightLowTides.append({
            "date": date,
            "lowTides": singleDayDaylightLowTides
        })

    return allDaylightLowTides


def printTides(allDaylightLowTides, requestedLocation, requestedDay):
    """
    Prints the low tides during daytime of a specified day
    Args:
        allDaylightLowTides (list): list of dictionaries containing a day 
            and the corresponding tide data
        requestedLocation (string): the location the user wants to learn about
        requestedDay (string): the day the user wants to learn about

    Ret:
        nothing, prints data to console
    """
    desiredDayData = []
    for day in allDaylightLowTides:
        if day["date"] == requestedDay:
            desiredDayData = day["lowTides"]

    print("For {} at {}:".format(requestedDay, requestedLocation))
    if desiredDayData:
        for lowTide in desiredDayData:
            print(lowTide["time"].strftime("%I:%M %p") + " at " + lowTide["height"])
    else:
        print("No low tides during daylight hours.")
    print('\n')



############## Run the script ##############

# get the location the user wants to examine
locationQuestion = [ 
    inquirer.List('locationVal',
        message="For which location do you want to see the daytime low tides?",
        choices=locations
    ),
]
desiredLocation = inquirer.prompt(locationQuestion)

# get the tide data
daylightLowTides = getTideData(desiredLocation["locationVal"])

# get the day the user wants to examine
dayQuestion = [ 
    inquirer.List('dayVal',
        message="For which day do you want to see the daytime low tides?",
        choices=[day["date"] for day in daylightLowTides]
    ),
]
desiredDay = inquirer.prompt(dayQuestion)

# print the desired data
printTides(daylightLowTides, desiredLocation["locationVal"], desiredDay["dayVal"])


