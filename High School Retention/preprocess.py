import os
import pandas as pd

# Retrieve CSV files
def fetch_and_combine_csv_files(directory):
    """
    This function retrieves all CSV files in a specified directory,
    reads them into dataframes, and combines them using pd.concat().

    Parameter:
        directory (str): Path to the directory containing the files.

    Returns:
        pd.DataFrame: A single dataframe containing the combined data from all CSV files.
        
    """
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    dataframes = [pd.read_csv(file) for file in csv_files]
    combined_dataframe = (pd.concat(dataframes, ignore_index=True)
                            .rename(columns = {'STDTID':'ID',
                                               'TERMENTERED':'TERM'})
                            .rename(columns = str.lower)
                         )

    # Convert hsgraddte to datetime format
    combined_dataframe['hsgraddte'] = pd.to_datetime(combined_dataframe['hsgraddte'])

    # make a grad_year column
    combined_dataframe['grad_year'] = combined_dataframe['hsgraddte'].dt.year.fillna(0).astype(int)
    
    return combined_dataframe

def add_hs_matriculation(hs_enrollment_df):
    """
    Parameters:
        hs_enrollment_df (pd.DataFrame): High school dataframe that combines last five fall semesters of enrollment data.
                                         Data comes from Demographic Data in Argos.

    Returns:
        pd.DataFrame: Dataframe with new feature created that records if a student has matriculated
                      directly out of high school into college or not.
                      
    """
    # Create hs matriculation column
    fall_hs = []
    
    for i in hs_enrollment_df['term'].unique():
        temp = hs_enrollment_df[hs_enrollment_df['term'] == i].reset_index(drop=True)
        for j in range(len(temp)):
            if str(i)[:4] in str(temp['term'].iloc[j]) and str(temp['grad_year'].iloc[j]) == str(i)[:4]:
                fall_hs.append('From HS')
            else:
                fall_hs.append('Not From HS')

    hs_enrollment_df['hs_matriculation'] = fall_hs

    return hs_enrollment_df
