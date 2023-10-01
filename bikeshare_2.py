"""
Project: Explore US Bikeshare Data
Description: This project make use of Python to explore data related to bike share systems for three major cities in the United States—Chicago,
             New York City, and Washington. Code was written to import the data and answer interesting questions about it by computing descriptive statistics.
Implemented By: Iva Tam
Date: 9/29/2023 

"""
import pandas as pd
import numpy as np
import datetime as dt
import time
import click

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' } 
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June') 
WEEKDAY = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')


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
    city = validate_numeric_input("\n Please select a city by entering its assigned number:\n\n" 
                        "[0] Chicago \n"
                        "[1] New York City\n"
                        "[2] Washington \n\n",0,2)

    # get user input for month (all, january, february, ... , june)  
    month = validate_numeric_input("\n Please select a month by entering its assigned number: \n\n"
                        "[0] All\n"
                        "[1] January\n"
                        "[2] February \n"
                        "[3] March \n"
                        "[4] April \n"
                        "[5] May \n"
                        "[6] June \n\n",0,6)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = validate_numeric_input("\n Please select a day by entering its assigned number: \n\n"
                        "[0] All\n"
                        "[1] Monday \n"
                        "[2] Tuesday \n"
                        "[3] Wednesday \n"
                        "[4] Thursday \n"
                        "[5] Friday \n"
                        "[6] Saturday \n"
                        "[7] Sunday \n\n",0,7)

    print('-' * 100)
    return city, month, day

def get_city_name(argument):
    if argument == 0:
            return "chicago"
    elif argument == 1:
            return "new york city"
    elif argument == 2:
            return "washington"

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
    start_time = time.time() 
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[get_city_name(city)])
    
    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] =  df['Start Time'].dt.month 
    df['Week Day'] =  df['Start Time'].dt.day
    df['Start Hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 0: 
    # filter by month to create the new dataframe
        df = df[df['Month'] == month] 
  
    if day != 0: 
    # filter by day of week to create the new dataframe
       df = df[df['Week Day'] ==  day] 

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-' * 100)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.""" 

    start_time = time.time()
    print('\nDisplaying the statistics on the most frequent times of travel\n')

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ' + str(MONTHS[most_common_month-1]).title() )

    # display the most common day of week
    most_common_day = df['Week Day'].mode()[0]
    print('The most common day of the week is: ' + str(most_common_day) )

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' + str(most_common_hour) )  
 
    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-' * 100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most commonly used start station is: " +  most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most commonly used end station is: " + most_common_end_station)

    # display most frequent combination of start station and end station trip 
    most_frequent_combination = str((df['Start Station'] + ' - ' + df['End Station']).mode()[0])
    print("The most frequent combination of start station and end station trip is: " + most_frequent_combination)

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-' * 100)
 
 
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.""" 
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    seconds_in_day = 86400
    seconds_in_hr = 3600
    seconds_in_min = 60

    # Tabulate total travel time
    total_travel_time_second = df['Trip Duration'].sum()
    total_travel_time = "" 
    
    total_day = int(total_travel_time_second/seconds_in_day)
    total_hr = int((total_travel_time_second % seconds_in_day)//seconds_in_hr)
    total_m = int(((total_travel_time_second % seconds_in_day) % seconds_in_hr)//seconds_in_min)
    total_s = int(((total_travel_time_second % seconds_in_day) % seconds_in_hr) % seconds_in_min)

    if (total_day > 0):
        total_travel_time += str(total_day) + 'd '
    if (total_hr > 0):
        total_travel_time += str(total_hr) + 'h '
    if (total_m > 0):
        total_travel_time += str(total_m) + 'm '
    if (total_s > 0):
        total_travel_time += str(total_s) + 's '

    # Tabulate mean travel time
    mean_travel_time_second = df['Trip Duration'].mean()

    mean_day = int(mean_travel_time_second/seconds_in_day)
    mean_hr = int((mean_travel_time_second % seconds_in_day)//seconds_in_hr)
    mean_m = int(((mean_travel_time_second % seconds_in_day) % seconds_in_hr)//seconds_in_min)
    mean_s = int(((mean_travel_time_second % seconds_in_day) % seconds_in_hr) % seconds_in_min)

    mean_travel_time = ""
    if (mean_day > 0):
        mean_travel_time += str(mean_day) + 'd '
    if (mean_hr > 0):
        mean_travel_time += str(mean_hr) + 'h '
    if (mean_m > 0):
        mean_travel_time += str(mean_m) + 'm '
    if (mean_s > 0):
        mean_travel_time += str(mean_s) + 's ' 
    
    # Display total travel time
    print("The total trip duration is ", total_travel_time )
    print("The average trip duration is ", mean_travel_time )  
    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-' * 100) 

def trip_duration_by_gender_subscriber(df):
    try: 
        """This function returns the mean and total duration grouped by user type and gender"""
        print('\nCalculating Trip Duration By Gender and User Type...\n')
        start_time = time.time()
        df_gen_user_trip_mean = df.groupby(['User Type','Gender'])[['Trip Duration']].mean().reset_index()
        df_gen_user_trip_total = df.groupby(['User Type','Gender'])[['Trip Duration']].sum().reset_index()
        seconds_in_day = 86400
        seconds_in_hr = 3600
        seconds_in_min = 60

        for index, row in df_gen_user_trip_total.iterrows():
            total_travel_time_second = row['Trip Duration'] 
            total_travel_time = "" 
            
            total_day = int(total_travel_time_second/seconds_in_day)
            total_hr = int((total_travel_time_second % seconds_in_day)//seconds_in_hr)
            total_m = int(((total_travel_time_second % seconds_in_day) % seconds_in_hr)//seconds_in_min)
            total_s = int(((total_travel_time_second % seconds_in_day) % seconds_in_hr) % seconds_in_min)

            if (total_day > 0):
                total_travel_time += str(total_day) + 'd '
            if (total_hr > 0):
                total_travel_time += str(total_hr) + 'h '
            if (total_m > 0):
                total_travel_time += str(total_m) + 'm '
            if (total_s > 0):
                total_travel_time += str(total_s) + 's '
            
            df_gen_user_trip_total.at[index, 'Trip Duration'] = total_travel_time

        print("The total duration by gender and subscriber is as follows:\n")
        print(df_gen_user_trip_total)

        for index, row in df_gen_user_trip_mean.iterrows():
            mean_travel_time_second = row['Trip Duration'] 
            mean_travel_time = "" 
            
            mean_day = int(mean_travel_time_second/seconds_in_day)
            mean_hr = int((mean_travel_time_second % seconds_in_day)//seconds_in_hr)
            mean_m = int(((mean_travel_time_second % seconds_in_day) % seconds_in_hr)//seconds_in_min)
            mean_s = int(((mean_travel_time_second % seconds_in_day) % seconds_in_hr) % seconds_in_min)

            if (mean_day > 0):
                mean_travel_time += str(mean_day) + 'd '
            if (mean_hr > 0):
                mean_travel_time += str(mean_hr) + 'h '
            if (mean_m > 0):
                mean_travel_time += str(mean_m) + 'm '
            if (mean_s > 0):
                mean_travel_time += str(mean_s) + 's '
            
            df_gen_user_trip_mean.at[index, 'Trip Duration'] = mean_travel_time

        print("\nThe mean duration by gender and subscriber is as follows:\n")
        print(df_gen_user_trip_mean)
        print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
        print('-' * 100) 
    except:
        print("Unable to compute the trip duration by user type and gender due to insufficient data.")
        print('-' * 100) 


def user_stats(df):  
    """Displays statistics on bikeshare users.""" 
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types 
    num_user_types = df['User Type'].value_counts().to_string()  
    print("The count of user types:\n")
    print(num_user_types) 

    # Display counts of gender 
    try:
        gender_distribution = df['Gender'].value_counts().to_string()  
        print("\nThe count of each gender: \n")
        print(gender_distribution)
    except:
        print("\nMetrics on gender are not available!")     

    # Display earliest, most recent, and most common year of birth 
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe oldest person to ride a bike was born in: ", earliest_birth_year)

        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("\nThe youngest person to ride a  bike was born in: " , most_recent_birth_year)

        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("\nThe most common year of birth among riders is: " ,most_common_birth_year) 
    except:
        print("\nMetrics on riders' year of birth are not available!")   

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-' * 100) 


# This function validates user input
def validate_numeric_input(prompt, start, end): 
    input_number = 0 
    while True:
        try:
            input_number = int(input(prompt)) 
            if ( input_number < start or input_number > end): 
                prompt = "Invalid selection. Please try again!\n"
            else: 
                break
        except: 
            prompt = "Invalid selection. Please try again!\n"
    
    return input_number

def validate_text_input(prompt, options):  
    possible_options = options.lower().strip().split(',') 
    while True:
        try:
            selected_option =  input(prompt).strip().lower() 
            
            if (selected_option not in possible_options): 
                    prompt = "Invalid selection. Please try again!\n"
            else:
                break       
        except:
            prompt = "Invalid selection. Please try again!\n"
   
    return selected_option

# Display raw data upon request by the user
def display_records(df):
    counter = 0 
 
    for i in range(counter, len(df.index)):
        
        print(df.iloc[counter:counter + 5, ].to_string()) 
        counter += 5
        print("\n")
        if validate_text_input ("Would you like to view the next 5 rows of raw data? Please select\n\n[y] Yes\n[n] No\n\n", "y,n") == 'y':
            continue
        else:
            break 

def main():
  load_new_data  = True
  while True:
        
        if (load_new_data):
            city, month, day = get_filters()
            df = load_data(city, month, day)
            # Once the data is loaded, we default to False because we want users to select option #7 below if they want to switch city. 
            # This helps so users can look at all other stats options below on a selected city. We do not want to ask users to pick a
            # city for every stats option. 
            load_new_data = False 
 
        selected_option = validate_numeric_input("\nPlease select one of the numeric options below to view specific metrics:\n\n "
                                  "[1] Statistics on the most frequent times of travel\n "
                                  "[2] Statistics on the most popular stations and trip\n "
                                  "[3] Statistics on on the total and average trip duration\n "
                                  "[4] Statistics on on bikeshare users\n "
                                  "[5] Statistics on on average trip duration by gender and subscriber\n "
                                  "[6] Display records\n "  
                                  "[7] Select another city, month and weekday\n "  
                                  "[8] Exit \n\n", 1,8 ) 
        
        if selected_option ==  1:
            time_stats(df)
       
        elif selected_option == 2:
            station_stats(df)
         
        elif selected_option == 3:
            trip_duration_stats(df) 

        elif selected_option == 4:
            user_stats(df)

        elif selected_option == 5:
            trip_duration_by_gender_subscriber(df)
       
        elif selected_option == 6:
            display_records(df)  

        elif selected_option == 7: 
            load_new_data = True
            
        elif selected_option == 8:  
            restart = validate_text_input("\nAre you sure you want to exit? Please specify:\n\n[y] Yes\n[n] No\n\n", "y,n")
            if restart.lower() == 'y':
               break
        else:
            load_new_data = False 

if __name__ == "__main__":
	main()
