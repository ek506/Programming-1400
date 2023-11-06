import pandas as pd
import re
import datetime
from matplotlib import pyplot as plt
import reporting
import intelligence
import monitoring


def main_menu():
    """
Main function called when program starts up. Allows user to select which module they want to use
from reporting, intelligence, monitoring, about and quit.

Args:
    No arguments

Returns:
    No returns
    """
    reload = True  # Indicates whether Menu text should be reloaded onto screen
    while True:
        if reload is True:
            print("\n Main Menu")
            print("R - Pollution Reporting")
            print("I - Mobility Intelligence")
            print("M - Real-time Monitoring")
            print("A - About")
            print("Q - Quit")
            print("Please select an option: ", end="")
            reload = False
        keypress = input()
        if keypress.lower() == "r":
            reporting_menu()
            print("\nReturned to Main Menu ")
            reload = True
        elif keypress.lower() == "i":
            intelligence_menu()
            print("\nReturned to Main Menu ")
            reload = True
        elif keypress.lower() == "m":
            monitoring_menu()
            print("\nReturned to Main Menu ")
            reload = True
        elif keypress.lower() == "a":
            about()
            print("\nReturned to Main Menu ")
            reload = True
        elif keypress.lower() == "q":
            quit()
        else:
            print("Please enter valid option: ", end="")


def reporting_menu():
    """
Allows user to select a monitoring station, a function they would like to use and a pollutant. The
function is then called and the results are printed to terminal.

Args:
    No arguments

Returns:
    No returns
    """
    print("\n  Pollution Reporting:")
    print("0: Harlington")
    print("1: North Kensington")
    print("2: Marylebone Road")
    print("Please select a site to view: ", end="")

    site_selected = None
    while site_selected is None:
        site_num = input()
        if site_num == "0":
            site_selected = "Harlington"
        elif site_num == "1":
            site_selected = "N Kensington"
        elif site_num == "2":
            site_selected = "Marylebone Road"
        else:
            print("Invalid option, try again:", end="")
    print(f"\n{site_selected} selected")

    print("0: Daily Average")
    print("1: Daily Median")
    print("2: Hourly Averages")
    print("3: Monthly Averages")
    print("4: Peak Hour Data")
    print("5: Count Missing Data")
    print("6: fill Missing Data")
    print("q: Return to Main Menu")
    print("What function would you like to use: ", end="")

    keypress = ""
    while keypress.lower() != "q":
        keypress = input()
        if keypress == "0":  # Daily average
            pollutant = select_pollutant_reporting()
            avg = reporting.daily_average(LocationData, site_selected, pollutant)
            print(f"Average {pollutant} values at {site_selected} for everyday of the year:")
            print(avg)
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "1":  # Daily Median
            pollutant = select_pollutant_reporting()
            med = reporting.daily_median(LocationData, site_selected, pollutant)
            print(f"Median {pollutant} values at {site_selected} for everyday of the year:")
            print(med)
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "2":  # Hourly Averages
            pollutant = select_pollutant_reporting()
            avg = reporting.hourly_average(LocationData, site_selected, pollutant)
            print(f"Average {pollutant} values at {site_selected} for each hour of the day:")
            print(avg)
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "3":  # Monthly Averages
            pollutant = select_pollutant_reporting()
            avg = reporting.monthly_average(LocationData, site_selected, pollutant)
            print(f"Average {pollutant} values at {site_selected} for each Month of the year:")
            print(avg)
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "4":  # Peak Hour Data
            pollutant = select_pollutant_reporting()

            df = LocationData[site_selected]
            start_date = df["date"].iloc[0]  # gets first date in data
            start_date = datetime.date(datetime.datetime.strptime(start_date, "%Y-%m-%d"))  # converts string to date
            end_date = df["date"].iloc[-1]  # gets last date in data
            end_date = datetime.date(datetime.datetime.strptime(end_date, "%Y-%m-%d"))  # converts string to date

            print(f"Enter a date between {start_date} and {end_date} in the form yyyy-mm-dd")
            time, value, date = None, None, None  # so variables not referred to before assignment
            valid_date = False
            while valid_date is False:
                date = input()
                try:
                    date = datetime.date(datetime.datetime.strptime(date, "%Y-%m-%d"))
                    if start_date <= date <= end_date:  # checks data is within range
                        time, value = reporting.peak_hour_date(LocationData, str(date), site_selected, pollutant)
                        valid_date = True
                    else:
                        print("Date outside of range. Try again: ", end="")
                except ValueError:  # date entered is not valid
                    print("Invalid date entered. Try again: ", end="")
                except KeyError:  # pollutant entered is not valid
                    print("Invalid Pollutant. Try again: ", end="")

            if time is None and value is None:  # If no data found at that time
                print(f"No data found for '{pollutant}' at {site_selected} for {date}")
            else:
                print(f"Max '{pollutant}' value at {site_selected} for {date}:")
                print(f"{value} at {time[:-3]}")  # [:-3] removes seconds from time to only print HH:MM
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "5":  # Count Missing Data
            pollutant = select_pollutant_reporting()
            count = reporting.count_missing_data(LocationData, site_selected, pollutant)
            print(f"{count} occurrences of missing data for '{pollutant}' at {site_selected}")
            input("Enter any key to return to Menu: ")
            break
        elif keypress == "6":  # Fill Missing Data
            pollutant = select_pollutant_reporting()
            count = reporting.count_missing_data(LocationData, site_selected, pollutant)
            print(f"There are {count} occurrences of missing '{pollutant}' data at {site_selected}")
            new_value = input("What would you like to replace these values with: ")
            try:
                LocationData[site_selected] = reporting.fill_missing_data(LocationData, new_value, site_selected, pollutant)
                print("Data successfully updated")
            except Exception:
                print("Error has occurred. Data not updated")
            input("Enter any key to return to Menu: ")
            break
        else:
            print("Please select a valid option: ", end="")


def monitoring_menu():
    """
Allows user to choose from one of four functions which use live data from London Air API. Results are printed
to the terminal

Args:
    No arguments

Returns:
    No returns
    """
    reload = True  # states whether options should be printed
    keypress = ""
    while keypress.lower() != "q":
        if reload is True:
            print("\n0: Pollution Objectives")
            print("1: Monthly Averages")
            print("2: Compare sites over last week")
            print("3: Air Quality Indexes")
            print("q: Return to Main Menu")
            print("Select an option: ", end="")
        keypress = input()
        reload = False

        if keypress == "0":  # Pollution objectives
            site_code = select_site()
            year = select_year()
            try:
                objectives, success_rate = monitoring.year_objectives(site_code, year)
                print(f"{site_code} achieved {success_rate:.2f}% of their objectives in {year}")

                show_objectives = input("Would you like to see the objectives? (y/n): ")
                while show_objectives.lower() != "n" and show_objectives.lower() != "y":
                    show_objectives = input("Please enter y or n: ")

                if show_objectives.lower() == "y":
                    for item in objectives:
                        print(f"{item[0]}: {item[1]}. Achieved: {item[2]}")
            except ValueError:
                print(f"No data available for {year}")
            input("press any key to return to menu: ")
            reload = True
        elif keypress == "1":  # Monthly Averages
            site_code = select_site()
            year = select_year()
            species_code = select_pollutant_monitoring()
            print(f"Here are the monthly {species_code} averages at {site_code} in {year}")
            month_averages = monitoring.monthly_average(site_code, species_code, year)
            print(month_averages)

            input("press any key to return to menu: ")
            reload = True
        elif keypress == "2":  # Compare sites
            print("\nThis function allows you to compare the mean, median and standard deviation of two sites over the"
                  " last week of data")
            print("Please select two sites to compare")
            site1_code = select_site()
            site2_code = select_site()
            species_code = select_pollutant_monitoring()

            sites_analytics = monitoring.compare_sites(site1_code, site2_code, species_code)
            print(sites_analytics)
            site1_analytics = sites_analytics[site1_code]
            site2_analytics = sites_analytics[site2_code]
            print(f"For {species_code}: ")
            print(f"{site1_code}: mean: {site1_analytics[0]} median: {site1_analytics[1]} SD: {site1_analytics[2]}")
            print(f"{site2_code}: mean: {site2_analytics[0]} median: {site2_analytics[1]} SD: {site2_analytics[2]}")

            input("press any key to return to menu: ")
            reload = True
        elif keypress == "3":  # Air Quality Indexes
            print("See the air quality indexes for the last 31 days")
            site_code = select_site()
            indexes = monitoring.air_quality_indexes(site_code)
            for pollutant, values in indexes.items():
                print(f"{pollutant}: {values} ")

            input("press any key to return to menu: ")
            reload = True
        else:
            print("Please select a valid option: ", end="")


def intelligence_menu():
    """
Allows user to select an option. The corresponding function is then called and the image is shown

Args:
    No arguments

Returns:
    No returns
    """
    reload = True  # states whether options should be printed
    keypress = ""
    while keypress.lower() != "q":
        if reload is True:
            print("0: Find red pixels")
            print("1: Find cyan pixels")
            print("2: Find connected components")
            print("q: Return to Main Menu")
            print("Select an option: ", end="")
        keypress = input()
        reload = False

        if keypress == "0":  # Find red pixels
            print("Please wait for image of red pixels")
            img = intelligence.find_red_pixels("./data/map.png")
            plt.imshow(img, cmap="Greys")
            plt.show()
            print("Image saved to 'map-red-pixels.jpg'\n")
            reload = True
        elif keypress == "1":  # Find cyan pixels
            print("Please wait for image of cyan pixels")
            img = intelligence.find_cyan_pixels("./data/map.png")
            plt.imshow(img, cmap="Greys")
            plt.show()
            print("Image saved to 'map-cyan-pixels.jpg'\n")
            reload = True
        elif keypress == "2":  # connected components
            print("Please wait for image of two largest connected components in red map")
            try:
                mark = intelligence.detect_connected_components("map-red-pixels.jpg")
                top2 = intelligence.detect_connected_components_sorted(mark)
                plt.imshow(top2, cmap="Greys")
                plt.show()
                print("Image saved to 'cc-top-2.jpg'")
                print("List of connected components saved to cc-output-2a.txt")
                print("Sorted list of connected components saved to cc-output-2b.txt\n")
            except FileNotFoundError:
                print("Please run 'Find red pixels' first to generate map-red-pixels.jpg")
                input("Enter any key to return: ")
            reload = True
        else:
            print("Please select a valid option: ", end="")


def select_pollutant_reporting() -> str:
    """
Prints a menu of the pollutants for the reporting module and asks the user to select one via keyboard input

Args:
    No arguments

Returns:
    pollutant: the code for the pollutant selected
    """

    print("\n0: Nitrous Oxide (no)")
    print("1: inhalable particulate matter ≤ 10µm (pm10) ")
    print("2: inhalable particulate matter ≤ 2.5µm (pm25) ")
    print("Please select a pollutant:", end="")
    pollutant = None
    while pollutant is None:
        keypress = input()
        if keypress == "0":
            pollutant = "no"
        elif keypress == "1":
            pollutant = "pm10"
        elif keypress == "2":
            pollutant = "pm25"
        else:
            print("Please select a valid option: ", end="")
    print(f"    '{pollutant}' selected")
    return pollutant


def select_year() -> str:
    """
Asks for user to enter a valid year from 1998-today. Keeps asking until user enters a valid year

    Returns:
        year: string of a valid year in the form YYYY

    """
    import datetime
    print("Please select a year from 1998-now: ", end="")
    current_year = datetime.date.today().year

    while True:  # loops until a valid year is entered
        year = input()
        if re.search("^\d{4}$", year) is not None:  # checks year contains 4 digits [0-9]
            if 1997 < int(year) <= current_year:
                return year
        print("Please enter a valid year: ", end="")


def select_site() -> str:
    """
Allows user to select a site code from the list of valid codes

Args:
    No arguments

Returns:
    site: Code for the monitoring site selected
    """
    sites = ["BX1", "BL0", "KC1", "MY1"]
    print("\nBX1: Bexley")
    print("BL0: Camden")
    print("KC1: Kensington & Chelsea")
    print("MY1: Westminster")
    site = input("Please enter a site code: ")
    while True:
        if site in sites:
            return site
        site = input("Please enter a valid site code: ")


def select_pollutant_monitoring():
    """
Allows user to select a pollutant for the monitoring module from the list of valid codes

Args:
    No arguments

Returns:
    pollutant: the code for the pollutant selected
    """
    pollutants = ["CO", "NO2", "PM10", "SO2"]
    print("\nCO: carbon monoxide")
    print("NO2: Nitrogen dioxide")
    print("PM10: Particulates < 10 micrometers")
    print("SO2: Sulfur dioxide")
    pollutant = input("Please enter a pollutant code: ")
    while True:
        if pollutant in pollutants:
            return pollutant
        pollutant = input("Please enter a valid pollutant code: ")


def about():
    """
Prints information to terminal

Args:
    No arguments

Returns:
    No returns
    """
    print("\n About:")
    print("     Module code: ECM1400")
    print("     Candidate number: 249140")
    keypress = input("Press q to return to Main menu: ")
    while keypress.lower() != "q":  # once q is pressed, function ends
        keypress = input()


def quit():
    """
Exits program when run

Args:
    No arguments

Returns:
    No returns
    """
    print("\n~~~|Terminating Program|~~~")
    exit()


if __name__ == '__main__':
    LocationData = {"Harlington": None,
                    "Marylebone Road": None,
                    "N Kensington": None}  # dictionary containing data about each location

    # adds dataframe for each location to LocationData dictionary
    for key in LocationData:  # for each location
        dataframe = pd.read_csv(f"./data/Pollution-London {key}.csv")
        LocationData[key] = dataframe

    main_menu()

