'''Final project version for Udacity's DAND Project 2: Explore US Bikeshare Data.'''

from calendar import day_name, month_name
from datetime import datetime
from datetime import time as Time
from operator import itemgetter
from csv import DictReader as dictr
import time

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) filename for a city's bikeshare data from input.
    '''
    # Ask user for input while managing incorrect input
    while True:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York, or Washington?\n')
        # Confirm if input string is one of the listed cities and ask again if not
        if city.lower() not in ('chicago', 'new york', 'washington'):
            print('\nYou didn\'t enter the correct input. Please enter one of the cities listed.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Use the input to select a filename
    city = city.lower()
    if city == 'chicago':
        return 'chicago.csv'
    elif city == 'new york':
        return 'new_york_city.csv'
    return 'washington.csv'

def get_time_period():
    '''Asks the user for a time period by which to filter the data and returns the specified filter.

    Args:
        none.
    Returns:
        (str) inputted type of filter.
    '''
    # Ask user for input while incorrect input
    while True:
        time_period = input('\nWould you like to filter the data: by month, day, both or, '
                            'not at all? Type "none" for no time filter.\n')
        # Confirm if input string is one of the listed options and ask again if not
        if time_period.lower() not in ('month', 'day', 'both', 'none'):
            print('\nYou didn\'t enter the correct input. Please enter month, day, both or none.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Return user input as (str) lower case
    return time_period.lower()

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (str) name of month from January to June.
    '''
    # Ask user for input while managing incorrect input
    while True:
        month = input('\nWhich month? January, February, March, April, May, or June?\n')
        # Confirm if input string is one of the listed months and ask again if not
        if month.title() not in month_name[:7]:
            print('\nYou didn\'t enter the correct input. Please enter one of the months listed.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Return user input as (str) title case
    return month.title()

def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) inputted day as its index of day_name (day_name[0] = 'Monday').
    '''
    # Ask user for input while managing incorrect input
    while True:
        day = input('\nWhich day? Please enter a day of the week from Sunday to Saturday.\n')
        # Confirm if input string is one of the days of the week and ask again if not
        if day.title() not in day_name:
            print('\nYou didn\'t enter the correct input. Please enter one of the '
                  'days of the week.\n'
                  'Returning you to the original input request:')
        else:
            break
    # Return (int) of day's index in day_name
    return list(day_name).index(day.title())

def fast_strptime(date):
    '''Reads a string of the format '%Y-%m-%d %H:%M:%S' and converts it to a datetime object.
    Args:
        (str) with format '%Y-%m-%d %H:%M:%S'.
    Returns:
        (datetime) object with format '%Y-%m-%d'.
    '''
    return datetime(
        int(date[:4]), # %Y
        int(date[5:7]), # %m
        int(date[8:10]), # %d
        )

def most_pop_count(data):
    '''Determines the most popular element in a list and its count.
    Args:
        list.
    Returns:
        most popular element, count as (int).
    '''
    count_dict = dict()
    # Create dict with items in data as the key and key count as the value
    for item in data:
        count_dict[item] = count_dict.get(item, 0) + 1
    return max(count_dict.items(), key=itemgetter(1))

def popular_month(data):
    '''Finds the most popular month in data['Start Time'] and returns the month
       and its count.

    Args:
        list of dictionaries with a key of 'Start Time'.
    Returns:
        (str) most popular month as month name, (int) count.
    '''
    # Create list of all months found in data[key] as (int)
    month_list = [int(element['Start Time'][5:7]) for element in data]
    # Determine the most popular month and count using most_pop_count
    my_month, count = most_pop_count(month_list)
    # Convert month as (int) to (str) for month name
    my_month = month_name[my_month]
    return my_month, count

def popular_day(data):
    '''Finds the most popular day in data['Start Time'] and returns the day
       and its count.

    Args:
        list of dictionaries with a key of 'Start Time'.
    Returns:
        (str) most popular day as weekday name, (int) count.
    '''
    # Create list of all days found in data[key] as (int) for weekday name
    day_list = [
        datetime.weekday(fast_strptime(element['Start Time']))
        for element in data
        ]
    # Determine the most popular day and count using most_pop_count
    my_day, count = most_pop_count(day_list)
    # Convert day as (int) to (str) for day name
    my_day = day_name[my_day]
    return my_day, count

def popular_hour(data):
    '''Finds the most popular hour in data['Start Time'] and returns the hour
       and its count.

    Args:
        list of dictionaries with a key of 'Start Time'.
    Returns:
        (str) most popular hour in 12 hr format , (int) count.
    '''
    # Create list of all hours found in data[key] as (int)
    hour_list = [int(element['Start Time'][11:13]) for element in data]
    # Determine the most popular hour and count using most_pop_count
    my_hour, count = most_pop_count(hour_list)
    # Convert hour to 12hr time
    my_hour = Time(hour=my_hour)
    my_hour = Time.strftime(my_hour, '%#I %p')
    return my_hour, count

def popular_element(data, key):
    '''Finds the most popular element within a dictionary key and its count.

    Args:
        list of dictionaries with the selected key.
    Returns:
        (str) most popular element, (int) count.
    '''
    # Create list of all elements
    element_list = [element[key]for element in data]
    # Return most popular element and count using most_pop_count
    return most_pop_count(element_list)

def popular_pair(data, first_key, second_key):
    '''Finds the most popular tuple of data from two dictionary keys and its count.
    Args:
        data: list of dictionaries with the keys below.
        first_key: key in dictionary.
        second_key: key in dictionary.
    Returns:
        (tuple) most popular tuple, (int) count.
    '''
    # Create a list of combined start and end stations
    start_list = [element[first_key] for element in data]
    end_list = [element[second_key] for element in data]
    trip_list = list(zip(start_list, end_list))
    # Return most popular trip and count using most_pop_count
    return most_pop_count(trip_list)

def trip_duration(data):
    '''Finds the total duration, average duration and, total number of trip times
       in data['Trip Duration'].

    Args:
        list of dictionaries with a key of 'Start Time'.
    Returns:
        (str) total trip duration, (str) average trip duration, (int) total trips.
    '''
    # Create list of element['Trip Duration'] as (float)
    duration_list = [float(element['Trip Duration']) for element in data]
    # Find total duration
    total_duration = sum(duration_list)
    # Find total number of trips
    element_count = len(duration_list)
    # Calculate average trip duration
    average_trip = total_duration/element_count

    # Convert total_duration to hr, min, sec format
    m, s = divmod(total_duration, 60)
    h, m = divmod(m, 60)
    total_duration = "{}hr {}min {}sec".format(int(h), int(m), round(s, 2))

    # Convert average_trip to hr, min, sec format
    m, s = divmod(average_trip, 60)
    h, m = divmod(m, 60)
    # Do not report hours if hours is 0
    if h == 0:
        average_trip = "{}min {}sec".format(int(m), round(s, 2))
    average_trip = "{}hr {}min {}sec".format(int(h), int(m), round(s, 2))

    return total_duration, average_trip, element_count

def info_type(data, key):
    '''Finds the types of elements and their counts in data[key].
    Args:
        list of dictionaries with specified key.
    Returns:
        sorted list of ((str) info type, (int) count).
    '''
    # Create list of items in key
    info_list = [element[key] for element in data]
    # Create dict with items in data as the key and key count as the value
    count_dict = dict()
    for item in info_list:
        count_dict[item] = count_dict.get(item, 0) + 1
    elements = [element for element in count_dict]
    count = [count_dict[element] for element in count_dict]
    count_list = sorted(list(zip(elements, count)))
    return count_list

def key_info(data, key):
    '''Confirms whether key is a key in dictionaries in data. If so,
       returns counts of each element type in the key using info_type function.
       Manages '' entries by converting them to 'Unknown'.
    Arg:
        list of dictionaries with specified key.
    Returns:
        if key is found: list of ((str) info type, (int) count).
        if key is not found: None.
    '''
    # Confirm presense of key
    if key not in data[0]:
        return None
    # Create count list for key type
    key_count = info_type(data, key)
    # Replace '' with 'Unknown'
    key_count = [
        ('Unknown', element[1]) if element[0] == '' else element
        for element in key_count]
    return key_count

def birth_year(data):
    '''Finds the birth date of the youngest and oldest user
       and the most popular birth year for users if 'Birth Year' key exists.
    Args:
        list of dictionaries.
    Returns:
        if 'Birth Year' exists: (int) year of birth of youngest user,
                                (int) year of birth of oldest user,
                                (int) most popular birth year for users,
                                (int) count of users for most popular birth year.
        if 'Birth Year' does not exist:
            None.
    '''
    # Confirm presence of 'Birth Year'
    if 'Birth Year' not in data[0]:
        return None
    # Create count list for 'Birth Year'
    year_list = info_type(data, 'Birth Year')
    # Create list of birth years, but excluding ''
    yo_old_list = [element[0] for element in year_list if element[0] != '']
    # Calculate birth years of oldest and youngest person
    yo_old_list = [int(float(element)) for element in yo_old_list]
    youngest = max(yo_old_list)
    oldest = min(yo_old_list)
    # Calculate most frequent birth year
    pop_count = max([element[1] for element in year_list if element[0] != ''])
    for element in year_list:
        if element[1] == pop_count:
            popular = int(float(element[0]))
    return youngest, oldest, popular, pop_count

def display_data(data):
    '''Provides the user the option of viewing five lines of data, repeating this upon request
       until the user responds with 'no'.
    Args:
        list of dictionaries.
    Returns:
        none.
    '''
    i = 0
    show_data = input('\nWould you like to see five lines of raw data? Type \'yes\' or \'no\'.\n')
    while show_data.lower() == 'yes':
        print(data[i:i + 5])
        i += 5
        show_data = input(
            '\nWould you like to see five more lines of raw data? Type \'yes\' or \'no\'.\n'
            )

def create_dict(csv_file):
    '''Creates a list of dictionaries from a csv file.

    Args:
        File name for csv file.
    Returns:
        List of dictionaries with key names as the first row of entries of the csv file.
        '''
    with open(csv_file) as f:
        list_dict = [{k: v for k, v in row.items()}
                     for row in dictr(f)]
    return list_dict

def filter_dict(data, filter_type, *filters):
    '''Creates a new list of dictionaries by filtering by selected month and/or day.

    Args:
        data: list of dictionaries with a 'Start Time' key.
        filter_type: 'month', 'day', or 'both'.
        filters:
            for filter_type = 'month': (str) name of a month.
            for filter_type = 'day': (int) representing day of week in .weekday.
            for filter_type = 'both': month filter as above, day filter as above.
    Returns:
        list of dictionaries.
    '''
    city_list = []
    # Manage filtering by month
    if filter_type == 'month':
        for element in data:
            # Determine the month of element in data
            month_index = int(element['Start Time'][5:7].strip("0"))
            # Compare the month name to month found in filters and add relevant entries to list
            if month_name[month_index] == filters[0]:
                city_list.append(element)
    # Manage filtering by weekday
    if filter_type == 'day':
        for element in data:
            # Determine the weekday as (int) of the element in orig_dict
            day_index = fast_strptime(element['Start Time']).weekday()
            # Compare day_index to day found in filters and add relevant entries to list
            if day_index == filters[0]:
                city_list.append(element)
    # Manage filtering by both month and weekday
    if filter_type == 'both':
        for element in data:
            # Determine the month of element in orig_dict
            month_index = int(element['Start Time'][5:7].strip("0"))
            # Determine the weekday as (int) of the element in orig_dict
            day_index = fast_strptime(element['Start Time']).weekday()
            # Compare the month name to month found in filters and add relevant entries to list
            # Compare day_index to day found in filters and add relevant entries to list
            # Add relevant entries to list
            if month_name[month_index] == filters[0] and day_index == filters[1]:
                city_list.append(element)
    return city_list

def month_info(data, run_time_list):
    '''Prints the most popular start month, and its count, in data.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Start Time' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    pop_month, pop_month_count = popular_month(data)
    run_time_list.append(
        "Calculating the most popular start month took %s seconds."
        % round((time.time() - start_time), 4)
    )
    print(
        "Most popular start month:              {}  (Trips: {})"
        .format(pop_month, pop_month_count)
        )
    return run_time_list

def day_info(data, run_time_list):
    '''Prints the most popular start day, and its count, in data.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Start Time' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    pop_day, pop_day_count = popular_day(data)
    run_time_list.append(
        'Calculating the most popular start day took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    print('Most popular start month:              {}  (Trips: {})'.format(pop_day, pop_day_count))
    return run_time_list

def hour_info(data, run_time_list):
    '''Prints the most popular start hour, and its count, in data.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Start Time' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    pop_hour, pop_hour_count = popular_hour(data)
    run_time_list.append(
        'Calculating the most popular start hour took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    print('Most popular start time:               {}  (Trips: {})'.format(pop_hour, pop_hour_count))
    return run_time_list

def duration_info(data, run_time_list):
    '''Prints total and average trip duration and total trips taken.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Trip Duration' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    tot_duration, av_duration, n_count = trip_duration(data)
    run_time_list.append(
        'Calculating the trip duration info took %s seconds.' % round((time.time() - start_time), 4)
    )
    print('Total trip duration:                   {}  (Total Trips Taken: {})'
          .format(tot_duration, n_count))
    print('Average trip duration:                 {}'.format(av_duration))
    return run_time_list

def station_info(data, run_time_list):
    '''Prints the most popular start and end stations, and their counts, in data.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Start Station' and 'End Station' keys.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    pop_start, pop_start_count = popular_element(data, 'Start Station')
    print(
        'Most popular start station:            {}  (Trips: {})'
        .format(pop_start, pop_start_count)
        )
    run_time_list.append(
        'Calculating the most popular start station took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    start_time = time.time()
    pop_end, pop_end_count = popular_element(data, 'End Station')
    run_time_list.append(
        'Calculating the most popular end station took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    print('Most popular end station:              {}  (Trips: {})'.format(pop_end, pop_end_count))
    return run_time_list

def trip_info(data, run_time_list):
    '''Prints the most popular trip, and it's count, in data.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Start Station' and 'End Station' keys.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    pop_trip, pop_trip_count = popular_pair(data, 'Start Station', 'End Station')
    run_time_list.append(
        'Calculating the most popular trip took %s seconds.' % round((time.time() - start_time), 4)
    )
    print(
        'Most popular trip:                     {} to {}  (Trips: {})'
        .format(pop_trip[0], pop_trip[1], pop_trip_count)
    )
    return run_time_list

def user_info(data, run_time_list):
    '''Prints the count for two or three user types and total number of users.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'User Type' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    info_type_list = (key_info(data, 'User Type'))
    if len(info_type_list) == 2:
        user_type_one, user_type_two = info_type_list
        type_one_type, type_one_count = user_type_one[0], user_type_one[1]
        type_two_type, type_two_count = user_type_two[0], user_type_two[1]
        print('Number of "{}" type users:       {}  (Total Users: {})\n'
              'Number of "{}" type users:     {}'
              .format(
                  type_one_type, type_one_count, type_one_count + type_two_count,
                  type_two_type, type_two_count
                  )
             )
    if len(info_type_list) == 3:
        user_type_one, user_type_two, user_type_three = info_type_list
        type_one_type, type_one_count = user_type_one[0], user_type_one[1]
        type_two_type, type_two_count = user_type_two[0], user_type_two[1]
        type_three_type, type_three_count = user_type_three[0], user_type_three[1]
        print('Number of "{}" type users:       {}  (Total Users: {})\n'
              'Number of "{}" type users:      {}\n'
              'Number of "{}" type users:     {}'
              .format(
                  type_one_type, type_one_count, type_one_count + type_two_count + type_three_count,
                  type_two_type, type_two_count,
                  type_three_type, type_three_count
                  )
             )
    run_time_list.append(
        'Calculating the user type counts took %s seconds.' % round((time.time() - start_time), 4)
    )
    return run_time_list

def gender_info(data, run_time_list):
    '''Checks data for a 'Gender' key.
       If 'Gender' key exists, it prints the count for three gender types in data.
       If not, prints a statement indicating this.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    if key_info(data, 'Gender') is None:
        print('There is no gender information for this set of data.')
    else:
        gender_type_one, gender_type_two, gender_type_three = key_info(data, 'Gender')
        type_one_type, type_one_count = gender_type_one[0], gender_type_one[1]
        type_two_type, type_two_count = gender_type_two[0], gender_type_two[1]
        type_three_type, type_three_count = gender_type_three[0], gender_type_three[1]
        print('Number of users of {} gender:     {}\n'
              'Number of users of {} gender:      {}\n'
              'Nubmer of users of {} gender:        {}'
              .format(
                  type_one_type, type_one_count,
                  type_two_type, type_two_count,
                  type_three_type, type_three_count
                  )
             )
    run_time_list.append(
        'Calculating the user gender counts took %s seconds.' % round((time.time() - start_time), 4)
        )
    return run_time_list

def birthyear_info(data, run_time_list):
    '''Checks data for a 'Birth Year' key.
       If 'Birth Year' key exists: Prints the count for three gender types.
       If not: Prints a statement indicating this.
       Appends 'run time info' to a list for future printing.

    Args:
        data: list of dictionaries with 'Birth Year' key.
        run_time_list: list.
    Returns:
        list.
    '''
    start_time = time.time()
    if key_info(data, 'Birth Year') is None:
        print('There is no birth year information for this set of data.')
    else:
        young_year, old_year, pop_year, pop_year_count = birth_year(data)
        print('Birth year of youngest user:           {}\n'
              'Birth year of oldest user:             {}\n'
              'Most frequent birth year:              {}  (Users: {})'
              .format(
                  young_year, old_year, pop_year, pop_year_count
                  )
             )
    run_time_list.append(
        'Calculating the user birth year counts took %s seconds.'
        % round((time.time() - start_time), 4)
    )
    return run_time_list

def print_trip_user_info(city_data, run_time_list):
    '''Combines functions duration_info, station_info, and trip_info under '---Trip Info---'
       and combines the functions user_info, gender_info, and birthyear_info under '---User Info---'
       Appends 'run time info' to a list for future printing.
    Args:
        list of dictionaries, list.
    Returns:
        list.
    '''
    print('\n---Trip Info---')
    run_time_list = duration_info(city_data, run_time_list)
    run_time_list = station_info(city_data, run_time_list)
    run_time_list = trip_info(city_data, run_time_list)
    print('\n---User Info---')
    run_time_list = user_info(city_data, run_time_list)
    run_time_list = gender_info(city_data, run_time_list)
    run_time_list = birthyear_info(city_data, run_time_list)
    return run_time_list

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period? (month, day, none)
    time_period = get_time_period()

    # Create list to collect run-time info
    run_time_info = []

    # Get statistics if no filter is used
    if time_period == 'none':
        # Create list of dictionaries based on selected city
        city_data = create_dict(city)
        # Print statistics and get run_time_info
        print('\n---Trip Start Info---')
        run_time_info = month_info(city_data, run_time_info)
        run_time_info = day_info(city_data, run_time_info)
        run_time_info = hour_info(city_data, run_time_info)
        run_time_info = print_trip_user_info(city_data, run_time_info)
        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_info:
            print(element)

    # Get statistics if month filter is used
    if time_period == 'month':
        # Find out which month
        selected_month = get_month()
        # Create new city_data based on selected month
        city_data = create_dict(city)
        city_data = filter_dict(city_data, time_period, selected_month)
        # Print statistics and get run_time_info
        print('\n---Trip Start Info---')
        run_time_info = day_info(city_data, run_time_info)
        run_time_info = hour_info(city_data, run_time_info)
        run_time_info = print_trip_user_info(city_data, run_time_info)
        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_info:
            print(element)

    # Get statistics if day filter is used
    if time_period == 'day':
        # Find out which day
        selected_day = get_day()
        # Create new city_data based on selected day
        city_data = create_dict(city)
        city_data = filter_dict(city_data, time_period, selected_day)
        # Print statistics and get run_time_info
        print('\n---Trip Start Info---')
        run_time_info = hour_info(city_data, run_time_info)
        run_time_info = print_trip_user_info(city_data, run_time_info)
        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_info:
            print(element)

    # Get statistics if both filter is used
    if time_period == 'both':
        # Find out which month
        selected_month = get_month()
        # Find out which day
        selected_day = get_day()
        # Create new city_data based on selected month and day
        city_data = create_dict(city)
        city_data = filter_dict(city_data, time_period, selected_month, selected_day)
        # Print statistics and get run_time_info
        print('\n---Trip Start Info---')
        run_time_info = hour_info(city_data, run_time_info)
        run_time_info = print_trip_user_info(city_data, run_time_info)
        # Print out the run_time_info
        print('\n---Run Time Info---')
        for element in run_time_info:
            print(element)

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_data)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
    statistics()
