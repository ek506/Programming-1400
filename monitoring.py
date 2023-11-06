from matplotlib import pyplot as plt
import requests
import datetime
import utils
import numpy as np


def air_quality_indexes(site_code: str) -> dict[str: list]:
    """
Returns the air quality indexes for each pollutant measured at the specified site every day for the last 31 days
Returns a dictionary containing pollutant: indexes_list as key: value pairs
Indexes lists have air quality index from the furthest back date at the start of the list and the air quality index from
the most recent date at the end of the list
Adds "N/A" to a pollutants indexes list if there is no data for that day

    Args:
        site_code: string of code for the specified monitoring site e.g. MY1

    Returns:
        indexes: dictionary containing pollutant codes of pollutants measured at the site as keys and lists containing
         the air quality indexes for each day of the last 31 days as values

    """
    indexes = {}

    date = datetime.date.today() - datetime.timedelta(days=32)
    for day in range(31):
        date = date + datetime.timedelta(days=1)

        url = f"https://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/SiteCode={site_code}/Date={date}/Json"
        res = requests.get(url)
        try:
            live_data = res.json()  # dictionary returned by api containing live data
            for item in live_data["DailyAirQualityIndex"]["LocalAuthority"]["Site"]["Species"]:
                if indexes.get(item["@SpeciesCode"]) is None:  # if pollutant is not a key in indexes dictionary
                    indexes[item["@SpeciesCode"]] = [int(item["@AirQualityIndex"])]  # add pollutant as key with list
                else:
                    indexes[item["@SpeciesCode"]].append(int(item["@AirQualityIndex"]))
        except Exception:
            for pol_list in indexes.values():  # if no data for that day, add "N/A" to all lists
                pol_list.append("N/A")
    return indexes


def compare_sites(site1_code: str, site2_code: str, species_code: str) -> dict[str: tuple]:
    """
Calculates the mean, median and standard deviation for two different monitoring stations for the last week of data
Returns a dictionary where the keys are site1_code and site2_code and the values are tuples containing the mean, median
and standard deviation for these sites
    Args:
        site1_code: string of code for first monitoring site e.g. MY1
        site2_code: string of code for second monitoring site e.g. BL0
        species_code: string of code for a specific pollutant e.g. NO2

    Returns:
        site_analytics: dictionary with a site_code key and a tuple of (mean, median, SD) as the value

    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    sites_analytics = {site1_code: (), site2_code: ()}
    for i in range(1, 3):
        if i == 1:
            site_code = site1_code
        else:
            site_code = site2_code
        url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
        res = requests.get(url)
        live_data = res.json()  # dictionary returned by api containing live data

        values = []
        for item in live_data["RawAQData"]["Data"]:
            try:
                values.append(float(item["@Value"]))
            except ValueError:  # value is empty so ignored from list
                pass

        if utils.length(values) == 0:  # no data available for that site
            sites_analytics[site_code] = ("N/A", "N/A", "N/A")
        else:
            mean = round(utils.meannvalue(values), 3)
            median = utils.median(values)
            sd = round(int(np.std(np.array(values))), 3)
            sites_analytics[site_code] = (mean, median, sd)

    return sites_analytics


def monthly_average(site_code: str, species_code: str, year: str = None) -> list[float]:
    """
Calculates the monthly average for each month in the specified year for the desired site and species.
Displays a line graph of the monthly averages where any values that are "N/A" are removed from the graph
so the line travels straight between the two adjacent points
    Args:
        site_code: string of code for a specific monitoring site e.g. MY1
        species_code: string of code for a specific pollutant e.g. NO2
        year: string of year in the form YYYY

    Returns:
        month_averages: list containing the average pollutant values for each month of the year
    """

    if year is None:
        today = datetime.date.today()
        year = today.year

    month_averages = []
    for month in range(1, 13):
        start_date = np.datetime64(f'{year}-{month:0>2}-01')  # first day of month
        end_date = np.datetime64(f'{year}-{month:0>2}') + np.timedelta64(1, 'M') - np.timedelta64(1, "D")  # last day


        url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
        res = requests.get(url)
        live_data = res.json()  # dictionary returned by api containing live data

        values = []  # temporarily stores values for current month
        for item in live_data["RawAQData"]["Data"]:
            try:
                values.append(float(item["@Value"]))
            except ValueError:  # no data available for that time
                pass
        try:
            avg = utils.meannvalue(values)
            month_averages.append(round(avg, 3))
        except ZeroDivisionError:  # no values available for that month
            month_averages.append("N/A")

    graph_averages = []  # removes any data that is "N/A" from graph
    months = []
    for month, avg in zip([x for x in range(1, 13)], month_averages):
        if avg != "N/A":  # if month average is not "N/A" add the month and value to the graph lists
            graph_averages.append(avg)
            months.append(month)

    if utils.length(graph_averages) == 0:
        print("No data available")
    else:
        # Plot graph of monthly averages
        plt.plot(months, graph_averages)
        plt.title(f"{species_code} Monthly Averages in {year} for {site_code}")
        plt.xlabel("Months")
        plt.ylabel(f"{site_code} (μg)")
        plt.show()

    return month_averages


def year_objectives(site_code: str, year: str) -> tuple[list[tuple], float]:
    """
Finds the pollution objectives for a given site and a given year.
Returns a tuple containing a list of objectives and the completion rate of these objectives.
List of objectives contains tuples of (pollutant code, objective description, achieved) where achieved is "YES" or "NO"
    Args:
        site_code: string of code for a specific monitoring site e.g. MY1
        year: string of year in the form YYYY

    Returns:
        objective_list: list of tuples where each tuple describes an objective. First element is pollutant code,
        second element is a description of the objective and the third element is "Yes" or "No" indicating whether
        the objective was complete
        success_rate: a float representing the percentage of the objectives that were achieved
    Raises:
        ValueError: No data is available from the api
    """
    url = f"https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/SiteCode={site_code}/Year={year}/Json"
    res = requests.get(url)
    try:
        live_data = res.json()  # dictionary returned by api containing live data
    except Exception:
        raise ValueError

    objective_list = []
    objective_count = 0
    complete_count = 0
    for entry in live_data["SiteObjectives"]["Site"]["Objective"]:  # for each objective
        objective_list.append((entry["@SpeciesCode"], entry["@ObjectiveName"], entry["@Achieved"]))
        objective_count += 1
        if entry["@Achieved"] == "YES":
            complete_count += 1
    success_rate = 100 * complete_count / objective_count  # percentage of objectives complete
    return objective_list, success_rate

