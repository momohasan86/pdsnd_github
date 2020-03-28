"""
Rideshare data analysis based on interactive inputs.
Using version control (git) and github as remote repository

Written By - Muhammad Hasan
Date - 04.03.20

"""

# Library imports
import time
import pandas as pd
import numpy as np

# Variable outlining csv file names
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Variables to check against if user input is acceptable
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to
                      apply no month filter
        (str) day - name of the day of week to filter by, or "all"
                    to apply no day filter
    """
    print('Hi! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    city = input('Which city - Chicago, New York or Washington? ').lower()
    # Exception handle user input
    city = user_input_validation('City', city)

    # Get user input for month (all, january, february, ... , june)
    month = input('Which month - January, February, March, April, May, June '
                  'or All? ').lower()
    # Exception handle user input
    month = user_input_validation('Month', month)

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week or All? ').lower()
    # Exception handle user input
    day = user_input_validation('Day', day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                      no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # Add columns to dataframe
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # Filter month in dataframe as per user input
    if month != 'all':
        df = df[df['month'] == months.index(month)+1]

    # Filter day in dataframe as per user input
    if day != 'all':
        df = df[df['day_of_week'] == days.index(day)]

    return(df)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common day of week
    cmn_day = int(df['day_of_week'].mode()[0])
    print('The most common day is: {} \n'.format(days[cmn_day].title()))

    # Display the most common start hour
    cmn_hour = int(df['hour'].mode()[0])
    print('The most common hour is: {} \n'.format(cmn_hour))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0].title()
    print('The most common start staion is: {} \n'.format(start_station))

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0].title()
    print('The most common end staion is: {} \n'.format(end_station))

    # Display most frequent combination of start station and end station trip
    station_comb = df['Start Station'] + ' to ' + df['End Station']
    station_comb = station_comb.mode()[0]
    print('The most common station combination is: {} \n'.format(station_comb))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    tvl_time_total = df['Trip Duration'].sum()

    # Break total travel time into days, hours, mins and secs
    day = int(tvl_time_total//86400)


    # Display total travel time
    print('Total travel time is {} days, {} hrs, {} mins and {} '
          'secs \n'.format(day))

    # Calculate mean travel time
    tvl_time_mean = df['Trip Duration'].mean()

    # Break mean travel time into days, hours, mins and secs
    day = int(tvl_time_mean//86400)


    # Display mean travel time
    print('Mean travel time is {} days, {} hrs, {} mins and {} '
          'secs \n'.format(day))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts of user types
    users = df.groupby('User Type', as_index=False).count()
    print('User types & count: \n')

    # Display user types and counts of user types
    for i in range(len(users)):
        print('{} - {}'.format(users['User Type'][i], users['Start Time'][i]))

    # Exception should there be no gender information
    if 'Gender' not in df:
        print('\nThere is no Gender information')
    # Calculate and print gender and counts of gender
    else:
        gender = df.groupby('Gender', as_index=False).count()
        print('\nGender types & count: \n')
        for i in range(len(gender)):
            print('{} - {}'.format(gender['Gender'][i],
                                   gender['Start Time'][i]))

    # Exception should there be no birth year information
    if 'Birth Year' not in df:
        print('\nThere is no Birth Year information \n')
    # Calculate the most common, earliest and recent year
    else:
        cmn_yr = int(df['Birth Year'].mode()[0])
        max_yr = df['Birth Year'].idxmax()
        min_yr = df['Birth Year'].idxmin()
        # Display earliest, most recent, and most common year of birth
        print('\nThe most common birth year: {}\n'.format(cmn_yr))
        print('The most recent birth year: {}\n'.format(int(df['Birth Year']
                                                              [max_yr])))
        print('The earliest birth year: {}\n'.format(int(df['Birth Year']
                                                           [min_yr])))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def display(df):
    """Displays individual trips 5 lines at a time"""

    srt_pos = 0  # Start index position
    end_pos = 5  # End index position
    remaining_rows = int(-1*(df['Start Time'].count() % 5))

    # Dataframe added columns removed as no longer needed
    df.drop(['month', 'day_of_week', 'hour'], axis=1, inplace=True)

    # Print how many individual trips there are
    print('\nThere are {} individual trips'.format(df['Start Time'].count()))

    # Ask user if they wish to see individual trip data
    user_input = input('\nDo you want to see the individual trip data? '
                       'Enter Y or N: ').lower()

    # Exception handle user input
    user_input = user_input_validation('IndividualTrip', user_input)

    if user_input == 'y':
        # In there are less than 5 trips initially, print these here and break
        if df['Start Time'].count() <= 5:
            print('\n')
            print(df.iloc[srt_pos:end_pos, :])
            return
        # While more than 5 trips, print in batches of 5 lines at a time
        while end_pos <= df['Start Time'].count():
            print('\n')
            print(df.iloc[srt_pos:end_pos, :])
            # Udpate the position indexes
            srt_pos += 5
            end_pos += 5
            # Ask if the user still wants to continue
            user_input = input('\nDo you wish to continue?'
                               'Enter Y or N: ').lower()
            # Exception handle user input
            user_input = user_input_validation('IndividualTrip', user_input)
            # Break should user choose 'No'
            if user_input == 'n':
                return
        # After looping through the dataframe, print any remaining trips
        print('\n')
        print(df.iloc[remaining_rows:, :])


def user_input_validation(type, user_input):
    """
    Exception handling for user input

    Args:
        (str) type - which user input to exception handle
        (str) user_input - string user has input
    Returns:
        (str) user_input - string that is an acceptable user input
"""
    # Exception handle when inputting individual trip data view
    if type == 'IndividualTrip':
        # While loop till correct input registered
        while user_input not in ['y', 'n', 'yes', 'no']:
            user_input = input('Input invalid! Please enter Y or N: ').lower()
        if user_input == 'yes':
            user_input = 'y'
        elif user_input == 'no':
            user_input = 'n'
    # Exception handle when inputting city filter
    elif type == 'City':
        # While loop till correct input registered
        while user_input not in CITY_DATA.keys():
            user_input = input('Input invalid! Please pick from Chicago, '
                               'New York, Washington: ').lower()
    # Exception handle when inputting month filter
    elif type == 'Month':
        # While loop till correct input registered
        while user_input not in months:
            user_input = input('Input invalid! Please pick from January, '
                               'February, March, April, May, June or '
                               'All: ').lower()
    # Exception handle when inputting day filter
    elif type == 'Day':
        # While loop till correct input registered
        while user_input not in days:
            user_input = input('Input invalid! Please pick from Monday, '
                               'Tuesday, Wednesday, Thursday, Friday, '
                               'Saturday, Sunday or All: ').lower()

    return(user_input)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)

        restart = input('\nWould you like to restart? Enter Y or N: ').lower()
        # Exception handle user input
        restart = user_input_validation('IndividualTrip', restart)
        if restart != 'y':
            break


if __name__ == "__main__":
    main()
