'''Updated version of bikeshare project, specifically converting from standard python to pandas.'''
from calendar import day_name, month_name
from datetime import datetime
from datetime import time as Time
import time
import pandas as pd
import matplotlib.pyplot as plt

def get_city():
    '''Returns city and filename (out of Chicago, New York and Washington) according to
       user input, while managing incorrect input.

    Args:
        none.
    Returns:
        city: (str) lowercase of input city.
        file: (str) corresponding csv filename.
    '''
    # Ask user for input while managing incorrect input
    while True:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York, or Washington?\n').lower()
        # Confirm if input string is one of the listed cities and ask again if not
        if city not in ('chicago', 'new york', 'washington'):
            print('\nYou didn\'t enter an availabe city. Please enter one of the cities listed.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Use the input to select a filename
    if city == 'chicago':
        file = 'chicago.csv'
    elif city == 'new york':
        file = 'new_york_city.csv'
    else:
        file = 'washington.csv'

    return city, file

def get_time_period():
    '''Allows the user to select a time filter, while managing incorrect input.

    Args:
        none.
    Returns:
        (str) inputted type of filter.
    '''
    # Ask user for input while incorrect input
    while True:
        time_period = input('\nWould you like to filter the data: by month, day, both or, '
                            'not at all? Type "none" for no time filter.'
                            '(This next step will take some time.)\n').lower()
        # Confirm if input string is one of the listed options and ask again if not
        if time_period not in ('month', 'day', 'both', 'none'):
            print('\nYou didn\'t enter an available filter. Please enter month, day, both or none.'
                  '\nReturning you to the original input request:')
        else:
            break
    # Return user input as (str) lower case
    return time_period

def get_month():
    '''Returns month between January and June, according to user input, while managing
       incorrect input.

    Args:
        none.
    Returns:
        (int) month as its index of month_name ('January' = 1)
    '''
    # Ask user for input while managing incorrect input
    while True:
        month = input('\nWhich month? January, February, March, April, May, or June?\n').title()
        # Confirm if input string is one of the listed months and ask again if not
        if month not in month_name[:7]:
            print('\nYou didn\'t enter an available month. Please enter one of the months listed.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Return user input as (str) title case
    return list(month_name).index(month)

def get_day():
    '''Asks the user for a day and returns the corresponding index, while managing
       for incorrect input.

    Args:
        none.
    Returns:
        (int) day of the week as its index of day_name ('Monday' = 0).
    '''
    # Ask user for input while managing incorrect input
    while True:
        day = input('\nWhich day? Please enter a day of the week from Sunday to Saturday.'
                    '\n').title()
        # Confirm if input string is one of the days of the week and ask again if not
        if day not in day_name:
            print('\nYou didn\'t enter an available day. Please enter one of the '
                  'days of the week.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Return (int) of day's index in day_name
    return list(day_name).index(day)

def print_header(city, filter_type, month_filter=None, day_filter=None):
    '''Prints header that indicatses city name and any filters used.

    Args:
        city: (str) city name.
        filter_type: (str) 'none', 'month', 'day', or 'both'.
        month_filter: (int) optional, index of selected month in month_name ('January' = 1).
        day_filter: (int) optional, index of selected day in day_name ('Monday' = 0).
    Returns:
        optional.
    '''
    if filter_type == 'none':
        print('\n--- Printing US Bikeshare Statistics for', city.title(), '---'
              '\n    (No filters used)\n')

    if filter_type == 'month':
        print('\n--- Printing US Bikeshare Statistics for', city.title(), '---'
              '\n    (Filter: Month - {})\n'.format(month_name[month_filter]))

    if filter_type == 'day':
        print('\n--- Printing US Bikeshare Statistics for', city.title(), '---'
              '\n    (Filter: Day - {})\n'.format(day_name[day_filter]))

    if filter_type == 'both':
        print('\n--- Printing US Bikeshare Statistics for', city.title(), '---'
              '\n    (Filters: Month - {}, Day - {})\n'.format(
                  month_name[month_filter], day_name[day_filter]))

def pie_chart(var_count, var_name, total_count, title):
    '''Creates a pie chart from two values.

    Args:
        var_count: (int) count of variable.
        var_name: (str) variable name.
        total_count: (int) total category count from which variable was selected.
        title: (str) title for chart.
    '''
    values = [var_count, total_count - var_count]
    labels = [var_name, 'Remainder']
    plt.subplots(figsize=(5, 5))
    plt.pie(x=values, labels=labels)
    plt.title(title)

def popular_month(df, city, trip_count, run_time_list):
    '''Prints the most popular start month, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal month
    df_time = df.dt.month
    pop_month = df_time.mode().loc[0]

    # Find count of modal month
    pop_month_count = df_time.value_counts().loc[pop_month]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular start month took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular month to start a trip:         {}  (Trips: {:,})"
        .format(month_name[pop_month], pop_month_count)
        )

    pie_chart(pop_month_count, month_name[pop_month], trip_count,
              "Trips Started in Most Popular Month for {}".format(city.title()))

    return run_time_list

def popular_day(df, city, trip_count, run_time_list):
    '''Prints the most popular start day, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal day
    pop_day = df.mode().loc[0]

    # Find count of modal day
    pop_day_count = df.value_counts().loc[pop_day]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular start day took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular day to start a trip:           {}  (Trips: {:,})"
        .format(day_name[pop_day], pop_day_count)
        )

    pie_chart(pop_day_count, day_name[pop_day], trip_count,
              "Trips Started on Most Popular Day for {}".format(city.title()))

    return run_time_list

def popular_hour(df, city, trip_count, run_time_list):
    '''Prints the most popular start hour, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal hour
    df_time = df.dt.hour
    pop_hour = df_time.mode().loc[0]

    # Convert to 12 hr time
    convert_hour = Time(hour=pop_hour)
    convert_hour = Time.strftime(convert_hour, '%#I %p')

    # Find count of modal hour
    pop_hour_count = df_time.value_counts().loc[pop_hour]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular start hour took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular hour to start a trip:          {}  (Trips: {:,})"
        .format(convert_hour, pop_hour_count)
        )

    pie_chart(pop_hour_count, convert_hour, trip_count,
              "Trips Started in Most Popular Hour for {}".format(city.title()))

    return run_time_list

def popular_start_station(df, city, trip_count, run_time_list):
    '''Prints the most popular start station, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal station
    pop_station = df.mode().loc[0]

    # Find count of modal station
    pop_start_count = df.value_counts().loc[pop_station]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular start station took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular start station:            {}  (Trips: {:,})"
        .format(pop_station, pop_start_count)
        )

    pie_chart(pop_start_count, pop_station, trip_count,
              "Trips Started from Most Popular Station for {}".format(city.title()))

    return run_time_list

def popular_end_station(df, city, trip_count, run_time_list):
    '''Prints the most popular end station, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal station
    pop_station = df.mode().loc[0]

    # Find count of modal station
    pop_start_count = df.value_counts().loc[pop_station]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular end station took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular end station:              {}  (Trips: {:,})"
        .format(pop_station, pop_start_count)
        )

    pie_chart(pop_start_count, pop_station, trip_count,
              "Trips Ended at Most Popular Station for {}".format(city.title()))

    return run_time_list

def popular_trip(df, city, trip_count, run_time_list):
    '''Prints the most popular trip, and its count, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find modal station
    pop_station = df.mode().loc[0]

    # Find count of modal station
    pop_start_count = df.value_counts().loc[pop_station]

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular trip took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular trip:            {}  (Trips: {:,})"
        .format(pop_station, pop_start_count)
        )

    pie_chart(pop_start_count, pop_station, trip_count,
              "Trips between Most Popular Station Pair for {}".format(city.title()))

    return run_time_list

def trip_duration(df, trip_count, run_time_list):
    '''Prints the overall and average trip duration, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        run_time_list: (list).
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find total trip duration
    total_duration = df.sum()
    # Calculate average trip duration
    average_trip = total_duration/trip_count

    # Convert total trip duration to hours
    total_duration = round(total_duration/3600, 4)

    # Convert average_trip to hr, min, sec format
    m, s = divmod(average_trip, 60)
    h, m = divmod(m, 60)
    # Do not report hours if hours is 0
    if h == 0:
        average_trip = "{}min {}sec".format(int(m), round(s, 2))
    else:
        average_trip = "{}hr {}min {}sec".format(int(h), int(m), round(s, 2))

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the trip duration took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print('Total trip duration:                   {:,} hours'
          .format(total_duration))
    print('Average trip duration:                 {}'.format(average_trip))

    return run_time_list

def user_info(df, city, run_time_list):
    '''Prints the count for two or three user types and total number of users, from df.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        column: (str) column name.
        run_time_list: (list).
        city: (str) name of city for df.
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    # Find user types and counts
    user_count = df['user_type'].value_counts()
    user_index = user_count.index

    if user_index.nunique() == 2:
        user_one_type, user_two_type = user_index
        user_one_count = user_count.loc[user_one_type]
        user_two_count = user_count.loc[user_two_type]
        print('Number of "{}" type users:       {:,}\n'
              'Number of "{}" type users:     {:,}'
              .format(
                  user_one_type, user_one_count, user_two_type, user_two_count
                  )
             )

        values = [user_one_count, user_two_count]
        labels = [user_one_type, user_two_type]
        plt.subplots(figsize=(5, 5))
        plt.pie(x=values, labels=labels)
        plt.title("User Types for {}".format(city.title()))

    if user_index.nunique() == 3:
        user_one_type, user_two_type, user_three_type = user_index
        user_one_count = user_count.loc[user_one_type]
        user_two_count = user_count.loc[user_two_type]
        user_three_count = user_count.loc[user_three_type]
        print('Number of trips taken by "{}" type users:            {:,}\n'
              'Number of trips taken by "{}" type users:      {:,}\n'
              'Number of trips taken by "{}" type users:     {:,}'
              .format(
                  user_one_type, user_one_count,
                  user_two_type, user_two_count,
                  user_three_type, user_three_count
                  )
             )

        values = [user_one_count, user_two_count, user_three_count]
        labels = [user_one_type, user_two_type, user_three_type]
        plt.subplots(figsize=(5, 5))
        plt.pie(x=values, labels=labels)
        plt.title("Trips Taken by User Types for {}".format(city.title()))

    # Save run-time info and print stats
    run_time_list.append(
        "Calculating the most popular trip took %s seconds."
        % round((time.time() - start_time), 4)
    )

    return run_time_list

def gender_info(df, column, city, run_time_list):
    '''Checks df for column.
       If column exists, prints the count for three gender types in data.
       If not, prints a statement indicating this.

    Args:
        df: Pandas DataFrame.
        column: (str) column name.
        city: (str) name of city for df.
        run_time_list: (list).
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    if column not in df:
        print('There is no gender information for this set of data.')
    else:
        # Fill missing values
        df[column].fillna('Unknown', inplace=True)
        # Find user types and counts
        gender_count = df[column].value_counts()
        gender_index = gender_count.index

        gender_type_one, gender_type_two, gender_type_three = gender_index
        gender_one_count = gender_count.loc[gender_type_one]
        gender_two_count = gender_count.loc[gender_type_two]
        gender_three_count = gender_count.loc[gender_type_three]

        print('Number of trips taken by users of {} gender:     {:,}\n'
              'Number of trips taken by users of {} gender:      {:,}\n'
              'Nubmer of trips taken by users of {} gender:        {:,}'
              .format(
                  gender_type_one, gender_one_count,
                  gender_type_two, gender_two_count,
                  gender_type_three, gender_three_count
                  )
             )

        values = [gender_one_count, gender_two_count, gender_three_count]
        labels = [gender_type_one, gender_type_two, gender_type_three]
        plt.subplots(figsize=(5, 5))
        plt.pie(x=values, labels=labels)
        plt.title("Trips Taken by Genders for {}".format(city.title()))

    run_time_list.append(
        'Calculating the user gender counts took %s seconds.' % round((time.time() - start_time), 4)
        )

    return run_time_list

def birth_year_info(df, column, city, run_time_list):
    '''Checks df for column.
       If column exists, prints oldest and youngest user, and most common birth year.
       If not, prints a statement indicating this.

    Args:
        df: Pandas DataFrame.
        column: (str) column name.
        city: (str) name of city for df.
        run_time_list: (list).
    Returns:
        run_time_list: (list) collection of run-time info.
    '''
    start_time = time.time()

    if column not in df:
        print('There is no birth year information for this set of data.')
    else:
        # Drop missing values
        df[column].dropna(inplace=True)

        # Find youngest user with 'reality' check
        young = df[column].max().astype(int)
        if (2016 - young) < 5:
            alt_young = pd.Series(df.birth_year.unique()).nlargest(n=2).iloc[1].astype(int)
            print('Birth year of youngest user:           {} '
                  '\n(Age: {} - This result may be due to user data entry error. '
                  'The next youngest birth year is {})'
                  .format(young, 2016 - young, alt_young))
        else:
            print('Birth year of youngest user:           {} (Age: {})\n'
                  .format(young, 2016 - young))

        # Find youngest user with 'reality' check
        old = df[column].min().astype(int)
        if (2016 - old) > 90:
            alt_old = pd.Series(df.birth_year.unique()).nsmallest(n=2).iloc[1].astype(int)
            print('Birth year of oldest user:           {} '
                  '\n(Age: {} - This result may be due to user data entry error. '
                  'The next oldest birth year is {})'
                  .format(old, 2016 - old, alt_old))
        else:
            print('Birth year of youngest user:           {} (Age: {})\n'
                  .format(old, 2016 - old))

        plt.subplots(figsize=(5, 5))
        df[column].hist()
        plt.title("User Birth Years for {}".format(city.title()))

        # Find most common birth year
        pop_year = df[column].mode().loc[0].astype(int)

        # Find count of modal birth year
        pop_year_count = df[column].value_counts().loc[pop_year]

        print('Most frequent birth year:              {}  (Users: {:,})'
              .format(pop_year, pop_year_count))

    run_time_list.append(
        'Calculating the user birth year counts took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    return run_time_list

def print_trip_info(df, city, trip_count, run_time_list):
    '''Combines functions duration_info, station_info, and trip_info under '---Trip Info---'.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        city: (str) name of city for df.
        trip_count: (int) number of rows in df.
        run_time_list: (list).
    Returns:
        run_time_list: (list).
    '''
    print('\n---Trip Info---')
    run_time_list = popular_start_station(df.start_station, city, trip_count, run_time_list)
    run_time_list = popular_end_station(df.end_station, city, trip_count, run_time_list)
    run_time_list = popular_trip(df.trip, city, trip_count, run_time_list)
    run_time_list = trip_duration(df.trip_duration, trip_count, run_time_list)

    return run_time_list

def print_user_info(df, column1, column2, city, run_time_list):
    '''Combines functions user_info, gender_info, and birth_year_info under '---User Info---'.
       Appends 'run time info' to a list for future printing.

    Args:
        df: Pandas DataFrame.
        column1: (str) column name for gender_info().
        column2: (str) column name for birth_year_info().
        city: (str) name of city for df.
        run_time_list: (list).
    Returns:
        run_time_list: (list).
    '''
    print('\n---User Info---')
    run_time_list = user_info(df, city, run_time_list)
    run_time_list = gender_info(df, column1, city, run_time_list)
    run_time_list = birth_year_info(df, column2, city, run_time_list)

    return run_time_list

def display_data(df):
    '''Provides the user the option of viewing five lines of data, repeating this upon request
       until the user responds with 'no'.

    Args:
        Pandas DataFrame.
    Returns:
        none.
    '''
    i = 0
    show_data = input('\nWould you like to see five lines of raw data? Type \'yes\' or \'no\'.\n')
    while show_data.lower() == 'yes':
        print(df.iloc[i:i + 5])
        i += 5
        show_data = input(
            '\nWould you like to see five more lines of raw data? Type \'yes\' or \'no\'.\n'
            )

def main():
    '''Provides statistics on start times, trips and users for bikeshare data from
       Chicago, New York and Washington based on user input.
    Args:
        none.
    Returns:
        none.
    '''
    city, file = get_city()
    time_period = get_time_period()

    df = pd.read_csv(file)
    df.rename(columns={'Start Time': 'start_time', 'End Time': 'end_time',
                       'Trip Duration': 'trip_duration', 'Start Station': 'start_station',
                       'End Station': 'end_station', 'User Type': 'user_type', 'Gender': 'gender',
                       'Birth Year': 'birth_year'}, inplace=True)

    df['start_time'] = pd.to_datetime(df.start_time)
    df['weekday'] = df.start_time.apply(datetime.weekday)
    df['trip'] = df.start_station + " to " + df.end_station

    # Create list to collect run-time info
    run_time_list = []

    if time_period == 'none':
        trip_count = df.shape[0]
        print_header(city, time_period)
        # Show Start Time stats
        print('---Trip Start Info---'
              '\nTotal Trips: {:,}'.format(trip_count))
        run_time_list = popular_month(df.start_time, city, trip_count, run_time_list)
        run_time_list = popular_day(df.weekday, city, trip_count, run_time_list)
        run_time_list = popular_hour(df.start_time, city, trip_count, run_time_list)

        # Show Trip stats
        run_time_list = print_trip_info(df, city, trip_count, run_time_list)

        # Show User start_stats
        run_time_list = print_user_info(df, 'gender', 'birth_year', city, run_time_list)

        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_list:
            print(element)

        plt.show()

    if time_period == 'month':
        month = get_month()
        # Update the dataframe according to the filter
        df = df.loc[df.start_time.dt.month == month]
        trip_count = df.shape[0]

        print_header(city, time_period, month_filter=month)
        # Show Start Time stats
        print('---Trip Start Info---'
              '\nTotal Trips: {:,}'.format(trip_count))
        run_time_list = popular_day(df.weekday, city, trip_count, run_time_list)
        run_time_list = popular_hour(df.start_time, city, trip_count, run_time_list)

        # Show Trip stats
        run_time_list = print_trip_info(df, city, trip_count, run_time_list)

        # Show User start_stats
        run_time_list = print_user_info(df, 'gender', 'birth_year', city, run_time_list)

        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_list:
            print(element)

        plt.show()

    if time_period == 'day':
        # Update the dataframe according to the filter
        day = get_day()
        df = df.loc[df.weekday == day]

        trip_count = df.shape[0]
        print_header(city, time_period, day_filter=day)
        # Show Start Time stats
        print('---Trip Start Info---'
              '\nTotal Trips: {:,}'.format(trip_count))
        run_time_list = popular_hour(df.start_time, city, trip_count, run_time_list)

        # Show Trip stats
        run_time_list = print_trip_info(df, city, trip_count, run_time_list)

        # Show User start_stats
        run_time_list = print_user_info(df, 'gender', 'birth_year', city, run_time_list)

        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_list:
            print(element)

        plt.show()

    if time_period == 'both':
        # Update the dataframe according to the filter
        month = get_month()
        day = get_day()
        df = df.loc[df.start_time.dt.month == month]
        df = df.loc[df.weekday == day]
        trip_count = df.shape[0]

        print_header(city, time_period, month_filter=month, day_filter=day)
        # Show Start Time stats
        print('---Trip Start Info---'
              '\nTotal Trips: {:,}'.format(trip_count))
        run_time_list = popular_hour(df.start_time, city, trip_count, run_time_list)

        # Show Trip stats
        run_time_list = print_trip_info(df, city, trip_count, run_time_list)

        # Show User start_stats
        run_time_list = print_user_info(df, 'gender', 'birth_year', city, run_time_list)

        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_list:
            print(element)

        plt.show()

    # Display five lines of data at a time if user specifies that they would like to
    display_data(df)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        main()


if __name__ == "__main__":
    main()
