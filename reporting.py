import pandas as pd
import utils


def daily_average(data: dict, monitoring_station: str, pollutant: str) -> list[float]:
    """
Returns a list containing the average value for the specified pollutant for each day of the year
Returns a list of 365 floats to 3dp, one for each day of the year.
If a value is 'no data' it is ignored when calculating the average for that day
If there is no data for the whole day, "N/A" is added to averages list

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         averages: list of average value 3dp for the specified pollutant each day of the year at the specified site

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("monitoring station invalid")

    averages = []  # list to store pollutant averages of each day
    for day in df.loc[0::24, "date"]:  # loops through each date in dataframe. Step 24 as each date repeated 24 times
        day_values = []
        try:
            for value in df.loc[df["date"] == day, pollutant]:
                try:
                    day_values.append(float(value))
                except ValueError:  # value contains 'no data' so not added to list
                    continue
            try:
                day_average = utils.meannvalue(day_values)
                averages.append(round(day_average, 3))  # adds average value rounded to 3dp to list of averages
            except ZeroDivisionError:  # no items in day_values
                averages.append("N/A")
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return averages


def daily_median(data: dict, monitoring_station: str, pollutant: str) -> list[float]:
    """
Returns a list containing the median value for the specified pollutant for every day of the year
Returns a list of 365 floats to 3dp, one for each day of the year
If a value is 'no data' it is ignored when calculating the median for that day
If there is no data for the whole day, "N/A" is added to medians list

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         medians: list of median value 3dp for the specified pollutant each day of the year at the specified site

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("Monitoring station invalid")

    medians = []
    for day in df.loc[0::24, "date"]:  # loops through each date in dataframe. Step 24 as each date repeated 24 times
        day_values = []
        try:
            for value in df.loc[df['date'] == day, pollutant]:
                try:
                    day_values.append(float(value))
                except ValueError:  # if value cannot be converted to float, ignore value
                    continue
            try:
                median_value = utils.median(day_values)
                medians.append(round(median_value, 3))  # adds median value rounded to 3dp to list of medians
            except IndexError:  # day_values has no elements
                medians.append("N/A")
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return medians


def hourly_average(data: dict, monitoring_station: str, pollutant: str) -> list[float]:
    """
Returns a list containing the average value to 3dp for a pollutant for each hour of the day at the specified
monitoring station.
If a value is 'no data' it is ignored when calculating the average for that hour
If there is no data on any day for that hour, "N/A" is added to hourly_averages list

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         hourly_averages: list of average value 3dp for the specified pollutant each day of the year at the specified site

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("Monitoring station invalid")

    hourly_averages = []
    for hour in range(1, 25):
        time = f"{hour:0>2}:00:00"

        hour_values = []
        try:
            for value in df.loc[df['time'] == time, pollutant]:  # for pollutant values for specified hour
                try:
                    hour_values.append(float(value))
                except ValueError:  # value contains 'no data' so not added to list
                    continue
            try:
                hour_average = utils.meannvalue(hour_values)
                hourly_averages.append(round(hour_average, 3))  # adds average for specified hour to 3dp
            except ZeroDivisionError:  # no items in hour_values
                hourly_averages.append("N/A")
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return hourly_averages


def monthly_average(data: dict, monitoring_station: str, pollutant: str) -> list[float]:
    """
Returns a list of the average pollutant value to 3dp for each month of the year for a specified monitoring station
Returns a list of 12 values each corresponding to the average for each month
If a value is 'no data' it is ignored when calculating the average for that month
If there is no data for the whole month, "N/A" is added to medians list

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         month_avg_list: list of average pollutant value to 3dp for each month at the specified site

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:  # the monitoring station inputted was invalid
        raise KeyError("Monitoring station invalid")

    month_avg_list = []
    for month in range(1, 13):
        month_df = df[pd.to_datetime(df['date']).dt.month == month]  # creates dataframe for specified month
        month_data = []
        try:
            for value in month_df.loc[:, pollutant]:
                try:
                    month_data.append(float(value))
                except ValueError:  # ignore if value is 'no data'
                    continue
            try:
                month_average = utils.meannvalue(month_data)
                month_avg_list.append(round(month_average, 3))
            except ZeroDivisionError:  # no items in month_average
                month_avg_list.append("N/A")
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return month_avg_list


def peak_hour_date(data: dict, date: str, monitoring_station: str, pollutant: str) -> (str, float):
    """
Returns a tuple (time, max_value) where 'time' is the time of the largest pollutant value and
'max_value' is the value of the largest pollutant value for the specified date
Returns None, None if no data is found for that day

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         date: str in the form YYYY-MM-DD
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         max_time, max_value: tuple of the largest value and the time of the largest value, both None if not data found

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("Monitoring station invalid")

    max_value = None
    max_time = None
    day_df = df.loc[df["date"] == date]  # creates dataframe only containing data for specified date
    if day_df.empty:
        return None, None
    for _, row in day_df.iterrows():
        try:
            if max_value is None or float(row[pollutant]) > max_value:  # if no maxvalue yet or value>maxvalue
                max_value = float(row[pollutant])  # update maxvalue to new largest value
                max_time = row["time"]  # update max_time to time of the largest value
        except ValueError:  # pollutant value is 'no data'
            continue
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return max_time, max_value  # if there is a value for maxvalue and max_time return values


def count_missing_data(data: dict,  monitoring_station: str, pollutant: str) -> int:
    """
Counts the number of values that contain 'no data' for a specified pollutant column at a specified monitoring station

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         count: number of times no data was found for pollutant

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("Monitoring station invalid")

    count = 0
    for _, row in df.iterrows():
        try:
            if row[pollutant] == "No data":
                count += 1
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return count


def fill_missing_data(data: dict, new_value: str,  monitoring_station: str, pollutant: str):
    """
Returns a copy of the dataframe for the specified monitoring station where 'No data' values in the
pollutant column have been replaced by 'new_value'

     Args:
         data: dictionary containing the monitoring sites as keys with their associated dataframes as the values
         new_value: value that replaces any values that are 'no data'
         monitoring_station: Name of monitoring station
         pollutant: code for pollutant to be used

     Returns:
         df: pandas dataframe where 'no data' values have been replaced

     Raises:
         KeyError: Invalid monitoring station or pollutant entered
     """
    try:
        df = data[monitoring_station]  # gets dataframe for location
    except KeyError:
        raise KeyError("Monitoring station invalid")

    for _, row in df.iterrows():
        try:
            if row[pollutant] == "No data":
                row[pollutant] = new_value
        except KeyError:
            raise KeyError("Invalid pollutant code")
    return df
