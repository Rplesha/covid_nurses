# covid_nurses
Application for checking the last time a given nurse had a covid patient. A charge nurse opens up the app and the first screen is date-stamped, so all the charge nurse needs to do is input a nurse's name to see the last time they had a covid patient. The app should do the rest of the work.

## Program Requirements:
- show each nurse (order of 100 nurses)
- show when the last time they had a covid patient
- ablity to easily update daily
- no patient information

## To run:
You will need to have python 3.6 or higher installed with the packages:
- numpy (v1.16.4)
- datetime
- pandas (v1.1.0)
- argparse (v1.1)

There are two argparse options to use with the python call
`python find_date_nurses.py -lookup` or `python find_date_nurses.py -l` will ask for a nurse's last name and produce the date and number of days since the last covid patient.
`python find_date_nurses.py -update` or `python find_date_nurses.py -u` will ask for a nurse's last name and add a date to nurses.csv.

You can also run the two together and both lookup nurses and update the file: `python find_date_nurses.py -u -l`
