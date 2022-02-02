
import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

washington_miss=7

def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    Run=1
    while Run==1 :
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city=input('Would you like to see data for chicago ,new york city or washington\n') 
        city=city.lower()
        if city in CITY_DATA.keys():
            if city !='washington':
                global washington_miss
                washington_miss=9
            while True:
                ans=input('Would you like to filter the data by month, day, both or not at all ? type"non" for no at all \n')  
                ans=ans.lower()
    # get user input for month (all, january, february, ... , june)
                if ans == "month" :
                    month=input('which month ? january , february , march , april , may , june ?\n')
                    month=month.lower()
                    day="none-specified"
                    Run=0
                    break
    # get user input for day of week (all, monday, tuesday, ... sunday)
                if ans == "day" :
                    day=input('which day ? response in intger-Form (sunday=1)\n')
                    day=day.lower()
                    month="none-specified"
                    Run=0
                    break
                if ans == "both" :    
                    month=input('which month ? january , february , march , april , may , june ?\n')
                    day=input('which day ? response in intger-Form (sunday=1)\n')
                    month=month.lower()
                    day=day.lower()
                    Run=0
                    break
                if ans=='non':
                    print('OK .. No Filter Is applied')
                    month="none-specified"
                    day="none-specified"
                    Run=0
                    break
                else:
                    print("Invalid Input ... Please TryAgain!")
                    continue
        else:
             print("Invalid Input ... Please TryAgain!")
             continue
         
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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'none-specified':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'none-specified':
        # filter by day of week to create the new dataframe
        Days = {1 :'Sunday',2 : 'Monday', 3 :'Tuesday', 4 :'Wednesday', 5 :'Thursday', 6 :'Friday', 7 :'Saturday'}
        df = df[df['day_of_week'] == Days[int(day)]]

    return df
        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    MostCommon=df.iloc[:,[washington_miss ,washington_miss+1 , washington_miss+2]].mode()  
    Month_No= {1: 'january', 2: 'february',3: 'march', 4: 'april', 5: 'may', 6: 'june'}
    Month=Month_No[int(MostCommon.iloc[0,0])] 
    # display the most common month
    print('Most Common Month is {}\n'.format(Month))
    # display the most common day of week
    print('Most Common Day is {}\n'.format(MostCommon.iloc[0,1]))
    # display the most common start hour
    print('Most Common Hour is {}\n'.format(MostCommon.iloc[0,2]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print('Most commonly used start station is : ' , df['Start Station'].mode().values )
    # display most commonly used end station
    print('\nMost commonly used end station is : ' , df['End Station'].mode().values)
    # display most frequent combination of start station and end station trip
    frequent_combination= df[['Start Station' ,'End Station' ]].mode()
    print('\nMost frequent combination of start station and end station trip is "{}" and "{}"  \n'.format(frequent_combination.iloc[0,0],frequent_combination.iloc[0,1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    print('\nTotal travel time is : {} Hours'.format(df['Trip Duration'].sum()/3600))
    # display mean travel time
    print('\nAverage travel time is : {} Hours '.format(df['Trip Duration'].mean()/3600))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    Types=df['User Type'].value_counts()
    print(Types)
    print('\n','-'*40)
    if 'Gender' in df.keys():
    # Display counts of gender
    # Adding an exception for washington city since it has no gender nor birthyear
        Genders=df['Gender'].value_counts()
        print(Genders)
        print('\n','-'*40)
    else:
        print('No Gender Information is acquired')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.keys():
        BirthYear=df['Birth Year']
        Most_Common=BirthYear.mode()
        print('Earliest BirthYear is : ' ,int(BirthYear.dropna().min()))
        print('Most recent BirthYear is : ' ,int(BirthYear.dropna().max()))
        print('Most common BirthYear is : ' ,int(Most_Common.values))
    else:
        print('No Birth Year Information is acquired')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_rawdata(df):
      """Displays Raw Data for the User"""
      df.drop(columns=['month','Hour'] , inplace=True)
      count=0
      raw_data=input('Would you like to see some raw date ?\n')
      while True:
            raw_data=raw_data.lower()
            if raw_data == 'yes' :
                for count in range (count ,count+5 ):
                    print(df.iloc[count,:] , '\n')
                    print('-'*40)
                count+=1
                print('5 rows of raw data have been printed\n')
            elif raw_data=='no' :
                return
            else:
                print("Invalid Input ... Please TryAgain!")  
            raw_data=input('Would you like to see more rows of raw date ?\n')
       
 
def main():
    print(pd.__version__)
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()



