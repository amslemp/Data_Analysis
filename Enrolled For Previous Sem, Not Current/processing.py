import pandas as pd

# Create function to feed in the unique term IDs and isolate the term for comparison
def select_term(df, term):
    """
    Parameters:
    
    df (pd.DataFrame): dataframe of the last five fall or spring semesters pulled from the "FAxx - 
                       FAxx CrHr Enrollment.xlsx" or "SPxx - SPxx CrHr Enrollment.xlsx" from each day's dashboard
                       update.
    term (int): The individual six digit integer representing the "upcoming" semester that we are seeing if students
                enrolled into.

    Returns:

    Dataframe of upcoming semester enrollments.
    
    """
    
    mask = df['TERM'] == term
    
    upcoming = df[mask].reset_index(drop = True)\
                       .rename(columns = {'RESD':'RESCODE'})
    
    return upcoming

def enrolled_for_upcoming(previous, upcoming):
    """
    Parameters:
    
    previous (pd.DataFrame): Dataframe of previous semester (semester that is in progress or just concluded).
    upcoming (pd.DataFrame): Dataframe of upcoming semester (semester that is about to start)

    Returns:
    Dataframe of students who are enrolled / not enrolled.
    
    """
    df = previous.copy()

    #Change all column headings in both datasets to lowercase.
    previous.columns = [i.lower() for i in previous.columns]
    upcoming.columns = [i.lower() for i in upcoming.columns]

    #Compare upcoming semester enrolled to previous semester enrolled, account 
    #for who is missing from upcoming that was enrolled for previous.
    up_ids = list(upcoming['id'])

    enrolled = ['Enrolled' if i in up_ids else 'Not Enrolled' for i in previous['id']]

    #Add enrolled column to previous dataframe (copy {df}).
    df['enrolled'] = enrolled
    
    return df

def final_df(main_df, phone):
    """
    Parameters:
    
    main_df (pd.DataFrame): Dataframe that compares enrollment from semester that just concluded or is still in progress
                            and upcoming semester.
    phone (pd.DataFrame): Dataframe of holds from Argos. These should be the holds from the semester that just concluded or is still
                          in progreess.

    Returns:
    
    pd.DataFrame: Dataframe that merges the active student holds with the combined dataframe that compares enrollment.
    
    """
    ##{'Descript10':'Hold-A/R Balance > $300', 'Descript_S':'Academic Suspension', 'Descript47':'Hold-TB/College Health'}
    holds = []

    for i, j, k, l in zip(phone['ARNOENRHOLD'], phone['SUSPHOLD'], phone['COLLHLTHHOLD'], phone['VPSSHOLD']):
        if i == 'Y':
            holds.append('A/R Hold')
        elif j == 'Y':
            holds.append('Acad Sus Hold')
        elif k == 'Y':
            holds.append('TB Test Hold')
        elif l == 'Y':
            holds.append('VP Stdt Svcs')
        else:
            holds.append("")

    phone['HOLDS'] = holds

    phone = phone[['ID', 'PRPHONE', 'BRPHONE', 'CARPHONE', 'EMAIL', 'OTHEREMAIL', 'HOLDS']]

    final = main_df.merge(phone, how = 'left', on = 'ID').drop_duplicates('ID')\
                   .reset_index(drop = True)
    return final
