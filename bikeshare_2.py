import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    cities = ['chicago', 'new york city', 'washington']



    inputCityMonthDay = input("Please enter the input according to this format => CITY, MONTH, DAY\nFor example: Chicago, June, All\n").lower()

    # Split string and assign city, month, day accordingly
    inputList = inputCityMonthDay.strip().split(',')

    while len(inputList) != 3:
        inputCityMonthDay = input("Input is entered incorrectly (either extra variables, or missing variables, have been entered)\nPlease enter the input according to this format => CITY, MONTH, DAY\nFor example: Chicago, June, All\n").lower()
        inputList = inputCityMonthDay.strip().split(',')


    city, month, day = inputList[0], inputList[1], inputList[2]


    # When user fails to enter values, they are then directed to enter the data they entered incorrectly seperately

    while city not in cities:
        city = input("The city you entered is not availible\nPlease enter the city you wish to view its data: (Options: Chicago, Washington, New York City) ").lower()



    while month not in months:
        month = input("Can not filter by specified value\nWould you like to filter by month or by day? (Answer by typing 'day' or 'month', if no filter is desired enter 'all')").lower()



    while day not in days:
        day = input("The day entered is not availible\nPlease enter the day where you wish to view the data: (Options: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)").lower()




    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Return the appropriate csv file
    df = pd.read_csv(CITY_DATA[city])

    # Convert the start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create month and day of week columns to better differntiate and filter the data
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Create a new filtered dataframe

        df = df[df['month'] == month]

    if day != 'all':

        # Create a new filtered dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print("Most popular month is ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day is ", popular_day)


    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour is ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]


    print("Most popular start station {}".format(popular_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most popular end station {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    # create a column displaying the full trip then proceed to find the mode of the newly created column
    df['Start End Station'] = df['Start Station'].map(str) + ' - '+ df['End Station'].map(str)
    popular_combination = df['Start End Station'].mode()[0]

    print("Most popular combination is {}".format(popular_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # For better visualization, total and avg times have been reduced to hours and minutes rather than seconds
    total_time_hrs = df['Trip Duration'].sum() // 3600
    avg_time_minutes = df['Trip Duration'].mean() // 60

    # display total travel time
    print('Total Travel Time {} hours'.format(total_time_hrs))

    # display mean travel time
    print('Average Travel Time {} minutes'.format(avg_time_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of user types in the database\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('Gender Counts\n', df['Gender'].value_counts())
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest birth year: {}'.format(int(df['Birth Year'].min())))
        print('Recent birth year: {}'.format(int(df['Birth Year'].max())))
        print('Earliest birth year: {}'.format(int(df['Birth Year'].mode()[0])))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

def view_users(df):
    """Displays individual informaion of bikeshare users."""

    print_sample = input("Would you like to view 5 rows of data for bikeshare users? (Enter 'yes' or 'no')").lower()


    # Check input validity
    while print_sample not in ['yes', 'no']:
        print_sample = input("The response is invalid, please enter either 'Yes' or 'No'\nWould you like to view 5 rows of data for bikeshare users? (Enter 'yes' or 'no')").lower()
    start_loc = 0
    # If user enters 'yes' proceed to create a dictionary from the dataframe and print index by index the rows into the console
    while print_sample != 'no':

        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        print_sample = input("Do you wish to continue?: ").lower()
        while print_sample not in ['yes', 'no']:
            print("The response is invalid, please enter either 'Yes' or 'No'")
            print_sample = input("Do you wish to continue?: ").lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_users(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
