import pandas as pd
from datetime import datetime
import numpy as np
import argparse

#-------------------------------------------------------------------------------

def make_nurse_df(nurse_csv):
    all_nurses = pd.read_csv(nurse_csv)
    all_nurses = all_nurses.fillna('')

    melt_nurses = all_nurses.melt(var_name='name', value_name='date')
    melt_nurses['name'] = [n.lower() for n in melt_nurses['name']]

    return all_nurses, melt_nurses

#-------------------------------------------------------------------------------

def match_name(nurses):

    lowercase_names = [n.lower() for n in nurses]

    # making sure that a good name is entered
    bad_entry = True
    while bad_entry == True:
        name = input("Enter nurse's last name: ")
        split_name = name.split()

        if len(split_name) > 1:
            # assuming the person put the full name, take the last entry
            name = split_name[-1]

        name = name.lower()

        if name in lowercase_names:
            bad_entry = False
        else:
            print('No such nurse. Please enter a valid last name.')

    return name

#-------------------------------------------------------------------------------

def find_most_recent(nurse_df, nurse_name):

    dates = nurse_df['date'][nurse_df['name'] == nurse_name]
    dt_dates = [datetime.strptime(d, '%m/%d/%y') for d in dates if d != '']
    today = datetime.today()

    if len(dt_dates):
        most_recent = np.max(dt_dates)
        most_recent_str = datetime.strftime(most_recent, '%m/%d/%Y')
        message = f"has had {len(dt_dates)} covid patient(s) with the most recent on {most_recent_str} or {(today - most_recent).days} days ago."
    else:
        message = "has not had a covid patient."

    print(f"Nurse {nurse_name[0].upper()}{nurse_name[1:]} {message}")

#-------------------------------------------------------------------------------

def update_nurses(df, nurse_csv):

    update = True
    today = datetime.today()

    while update == True:
        nurse_name = match_name(list(df.keys()))
        case_nurse_name = f"{nurse_name[0].upper()}{nurse_name[1:]}"

        # making sure the date is in a format that datetime understands
        bad_entry = True
        while bad_entry == True:
            covid_date = input(f'Please enter date (mm/dd/yy) for nurse {case_nurse_name}: ')
            try:
                new_date = datetime.strptime(covid_date, '%m/%d/%y')
                entry_date = datetime.strftime(new_date, '%m/%d/%y')
                bad_entry = False
            except ValueError:
                print('Bad entry. Please make sure the date is in the format mm/dd/yy')

        # add the entry to the df for that nurse, filling in a blank row if it exists
        try:
            first_index = df[case_nurse_name][df[case_nurse_name] == ''].index[0]
            df[case_nurse_name][first_index] = entry_date
        except IndexError:
            # no blank entries for this nurse, so make a new row in the csv
            merge_df = pd.DataFrame([entry_date], columns=[case_nurse_name])
            df = pd.merge(df, merge_df, how='outer')
            df = df.fillna('')

        update_again = input('Add another date for another nurse? (y/n) ')
        if 'y' in update_again.lower():
            update = True
        else:
            update = False

    df.to_csv(nurse_csv, index=False)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--update", "-u", dest="update_nurses", action="store_true",
                        default=False, help="Use if you want to update the dates for nurses.")

    parser.add_argument("--lookup", "-l", dest="lookup_nurses", action="store_true",
                        default=False, help="Use if you want to look up the last date a nurse had a covid patient.")

    args = parser.parse_args()

    nurse_csv = 'nurses.csv'
    # as_is_df is non-melted df
    as_is_df, nurse_df = make_nurse_df(nurse_csv)

    if args.lookup_nurses:
        done = False
        while done == False:
            nurse_name = match_name(list(as_is_df.keys()))
            find_most_recent(nurse_df, nurse_name)

            search_again = input('Do you want to look up another nurse? (y/n) ')
            if 'y' in search_again.lower():
                done = False
            else:
                done = True

    print('*********** Update Information ***********')
    if args.update_nurses:
        update_nurses(as_is_df, nurse_csv)
