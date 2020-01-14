import pandas as pd
import numpy as np
from flask import Flask, render_template


master_file = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTtL1gD1bMJrarLZ46DtywkrO9cnPLRXjZiBX18pY1t4bPpUHu6J2LrSdIgTstReYqLz-Cdj5XkInYK/pub?output=csv'

def convert_date_to_string(entry):
    if np.isnan(entry):
        modified_str_date = 'No date available'
    else:
        str_date = str(int(entry))
        modified_str_date = str_date[:4] + '-' + str_date[4:6] + '-' + str_date[6:8]
    return modified_str_date

def convert_status(entry):
    status = 'Unknown, contact UVIT-POC'
    if entry == 'p':
        status = 'No merged L1 data yet available from ISRO'
    elif entry in ['n', 'w']:
        status = 'L2 pipeline processing issues, please contact UVIT-POC for details'
    elif entry == 'y':
        status = 'Both L1 & L2 has been sent to ISSDC, please check ISSDC AstroBrowse'
    elif pd.isnull(entry):
        status = 'No merged L1 data yet available from ISRO'
    return status


app = Flask(__name__)

@app.route('/l2stats')
def uvit_archive():
    df = pd.read_csv(master_file)
    df = df[df['PV'] != 'y'] # No need to display PV phase data.
    selected_df = df[['ObsID', 'date', '6.3 L2']]
    array = selected_df.values
    array[:, 1] = [convert_date_to_string(d) for d in array[:, 1]]
    array[:, 2] = [convert_status(d) for d in array[:, 2]]
    status_list = list(array)
    return render_template('data_table.html', status_list = status_list)

if __name__ == "__main__":
    app.run(host = '0.0.0.0')

