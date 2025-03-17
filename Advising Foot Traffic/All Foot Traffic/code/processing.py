import pandas as pd
import numpy as np

def modify_df(df, location):
    """
    Parameters:
        df (pd.DataFrame): Dataframe of each location loaded up from a csv.
        location (str): Three letter string (e.g. "BOA", "BOE", "BSC", "BOM") of the advising location.

    Returns:
        pd.DataFrame: Dataframe of each location cleaned and organized so that they can be concatenated.
        
    """

    #Modify headers and 'TIME IN colname
    df = (df.rename(columns = str.upper)
            .rename(columns = lambda x: x.replace('\n', ' '))
            .rename(columns = {'TIME IN':'TIME OF CONTACT'})
            .assign(LOCATION = location,
                    TIME_RANGE = '',
                    **({'ATHLETE':''} if 'ATHLETE' not in df.columns else {})) # add 'ATHLETE' col if missing
            .astype({'#':int}) # Converts "#" column to integer
            .rename(columns = {'TIME_RANGE':'TIME RANGE'})
         )
    
    #Reorganize columns
    cols = ['DATE', '#', 'NAME', 'TIME OF CONTACT', 'TIME RANGE', 'LOCATION',
            'APPT', 'DISTANCE', 'CURRENT STUDENT', 'NEW STUDENT', 'RETURNING STUDENT', 
            'HIGH SCHOOL', 'WORKFORCE', 'VETERAN', 'ENROLL','ADD/DROP', 'QUESTIONS', 
            'MAJOR CHANGE', 'DEGREE CHECK', 'SUSPENSION', 'ATHLETE', 'ADVISOR SIGN', 'ADV TIME']
    
    df = df[cols]

    #Sort through all rows and eliminate 'NaN'. More of an aesthetic thing for me.
    for i in list(df.columns[6:21]):
        temp = df[i]
        ls = []
        for j in list(temp):
            if j in ['x', 'X', 'Phone', 'In Person', 'Zoom', 'Email', 'Central Adv']:
                ls.append(j)
            else:
                ls.append('')
        df[i] = ls

    #Return modified df
    return df

def clean_location_data(all_location_df, saved_file_name):
    """
    Parameters:
        all_location_df (pd.DataFrame): Dataframe of combined locations.

    Returns:
        pd.DataFrame: Dataframe that is cleaned, dates set, days of weeks changed, months added.
        
    """
    #Convert 'DATE' column to datetime object. If you have errors thrown in reference to this
    #code, it is because the dates from one of your sites are not formatted correctly. If you wish
    #you can simply submit " errors = 'coerce' " after the fin_mashup['DATE'] in the to_datetime()
    #method. However, doing so will simply convert the dates Pandas cannot read to 'NaT', which 
    #is unhelpful. Better to go back in and fix the dates. 
    
    all_location_df = (all_location_df
                           .assign(
                               DATE = lambda df: pd.to_datetime(df['DATE'], errors = 'coerce'),
                               MONTH = lambda df: df['DATE'].dt.month.map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6:'Jun', 
                                                                           7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}),
                               DAY = lambda df: df['DATE'].dt.weekday.map({0: 'Mon', 1:'Tues', 2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 
                                                                            6:'Sun'})
                           )
                        )
                                                                               
    #Export mashup to csv
    mashup = all_location_df.to_csv(saved_file_name, index = False)

    return all_location_df

#The program below creates a new dataframe, aggregated by whatever column you insert.
def create_dataframe(df, column):
    """
    Parameters:
        df (pd.DataFrame): Combined dataframe of all advising locations.
        column (str): String name of column you wish to pull to make new dataframe.

    Returns:
        pd.DataFrame: Returns a dataframe that shows a count of students assisted with a column 
                      that shows the percent contribution of each line value. (i.e. $\frac{text{Value}}{text{sum(Value)}}$
                      
    """
    temp = (pd.DataFrame(df.groupby(column)[column].count())
            .rename(columns = {column:'Count'})
            .sort_values('Count', ascending = False)
            .reset_index()
            .assign(perc_cont = lambda df: round(df['Count'] / df['Count'].sum() * 100, 2))
            .rename(columns = {'perc_cont':'% Contribution'})
           )
    
    return temp

def new_dashboard_cleaned_dates(dashboard_df):
    """
    Parameters:
        dashboard_df (pd.DataFrame): Dataframe of advising foot traffic, combined from all sites.
                                     This is for the new dashboard setup from 2021 forward.

    Returns:
        pd.DataFrame: Dataframe of cleaned up dates, times, location, and creates a column with a 
                      unique ID. 
                      
    """
    #Change the '#' column to be the range of 1 to the end of the df. 
    dashboard_df['#'] = range(1,len(dashboard_df)+1)
    
    #Edit out all of the NaNs in the df. Again, an ascthetic thing for me.
    ls = []
    for i in dashboard_df['LOCATION'].unique():
        temp = dashboard_df[dashboard_df['LOCATION'] == i]
        ls.append(modify_df(temp, i))
    
    dash = pd.concat(ls)
    
    #Begin to make the individual id's for each student's sign in.
    #First we have to create an origin date.
    dash['ORIGIN DATE'] = '1/1/1900'
    
    #Second, we need to convert the 'DATE' and 'ORIGIN DATE' to a datetime object
    dash['ORIGIN DATE'], dash['DATE'] = pd.to_datetime(dash['ORIGIN DATE']), pd.to_datetime(dash['DATE'], format = 'mixed')
    
    #Now, to create the numerical day representation for the date as counted from 1/1/1900, 
    #we subtract the current date from the origin date.
    dash['NEW DATE'] = dash['DATE'] - dash['ORIGIN DATE']
    
    #To complete our id, we create a comprehension adding the numerical day with the '#' column.
    #This creates a unique id for every student who has walked into College Advising, either in person
    #or via phone, email, or zoom.
    ids = [str(dash['NEW DATE'][i].days) + str(dash['#'][i]) for i in range(len(dash['NEW DATE']))]
    
    #Create ID column with the new ids and drop the 'NEW DATE' and 'ORIGIN DATE'
    dash['ID'] = ids
    dash = dash.drop(['NEW DATE', 'ORIGIN DATE'], axis = 1)
    
    #First, convert 'Time of Contact' to datetime object. There are some debugging errors here.
    #We need to make sure that all the times are writen as timeframe objects in the csv. A simple
    #table creation in csv, filter, scroll to the bottom and any unique methods of entering times
    #will be revealed. Those all need to be identified and fixed. Where there are empty rows, 
    #typically this is where an advisor was entering a group enrollment and just didn't want to 
    #enter a bunch of times. In such cases, I copy the time closest to it and run with that.
    #usually somewhere in the neighborhood of 40 students. 
    dash['TIME OF CONTACT'] = pd.to_datetime(dash['TIME OF CONTACT'])

    dash = dash[dash['TIME OF CONTACT'].isnull() == False].reset_index(drop = True)
    
    #Insert 'TIME RANGE' column
    times = []
    for i in dash['TIME OF CONTACT']:
        times.append(str(i.hour) + ':00-' + str(i.hour) + ':59')
        
    #Add the times object as the column of 'TIME RANGE'. Now I have the complete dataset that I can
    #start altering into a usable dataset for a dashboard.
    
    dash['TIME RANGE'] = times

    return dash

#Set up the data to convert to a dashboard
def dashboard_setup(data, columns, col_name):
    """
    Parameters:
        data (pd.DataFrame): Dataframe of the enrollment data from all locations in a single csv file.
                             This is for the new dashboard setup from 2021 forward.
        columns (list): List of column names in all caps that need to be sifted through.
        col_name (str): This is the name of the new column that combines the content from the list of columns.

    Returns:
        pd.DataFrame: A new dataframe with consolidated information from the columns into col_names.
        
    """
    #Sort through the columns, identifying the index and replacing
    #the 'x'|'X' with column name. This for loop loops through each
    #individual column, then through each individual row of each 
    #column. The enumerate() creates a Series with each column that 
    #has an index and then the value. We convert the dict created with
    #each column to a data frame and then stack those data frames into
    #a list. 
    ls = []
    for i in columns:
        temp = data[i]
        ls2 = {}
        for j, k in enumerate(temp):
            if k == 'x' or k == 'X':
                ls2[j] = i
        df = pd.DataFrame.from_dict(ls2, orient = 'index')
        ls.append(df)
        
    #Now we use the pd.concat() to convert the list to a data frame. Drop
    #duplicates because some rows have multiple 'X's in them, which creates
    #two entries at the same location.
    df2 = (pd.concat(ls)
             .reset_index()
             .rename(columns = {0: col_name})
             .sort_values('index')
             .drop_duplicates('index')
          )
    
    #Now we need to identify and store all of the indeces that do not 
    #appear in the data frame created with df2. 
    missing = {}
    for i in list(data.index):
        if i not in list(df2['index']):
            missing[i] = ''
    
    #Convert the missing indeces to a dataframe that has the same
    #columns as df2.
    missing = (pd.DataFrame
                 .from_dict(missing, orient = 'index')
                 .rename(columns = {0: col_name})
                 .reset_index()
              )
    
    #Append the two data frames together, sort the values from 
    #lowest to highest by the 'index' column (not the .index())
    #then drop the 'index' column and reset_index().
    final = (pd.concat([df2, missing])
               .sort_values('index')
               .drop('index', axis=1)
               .reset_index(drop=True)
            )
    
    return final
