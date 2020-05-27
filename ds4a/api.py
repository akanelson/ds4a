import os
import sys
from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.formula.api as smf

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Add directory where we have our configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + '/..')) + '/initial_exploratory_analysis/')
# Now we can import our modulue
from practicum_utils import get_loggi_files, global_connect, run_query, explained_time, careful_query

# db connect
db = global_connect()

agencies = ['6e7dacf2149d053183fe901e3cfd8b82', '58cfe3b975dd7cbd1ac84d555640bfd9']
# --------------------------------
# hard coded holidays just for now
# --------------------------------
holidays = [
    ('2019-01-01', 'New Year Day'),
    ('2019-03-04', 'Carnival'),
    ('2019-03-05', 'Carnival'),
    ('2019-05-01', 'Labour Day'),
    ('2019-09-07', 'Independece Day'),
    ('2019-12-25', 'Christmas Day'),
    ('2019-12-31', 'Last Year Day'),
    ('2020-01-01', 'New Year Day'),
    ('2020-01-25', 'Sao Paulo Birthday (no working day for agency 1)'),    
    ('2020-02-24', 'Carnival'),
    ('2020-02-25', 'Carnival')
]

# -------------------------------------------------------------------
# [APP]: Useful to obtain history of unique number of drivers per day
# -------------------------------------------------------------------
def get_daily_drivers(agency_id, from_='2019-10-01', to_='2020-03-31'):
    
    df = careful_query("""
        select *
        from unique_drivers_daily_oozma
        where date >= '{1}'
          and date < '{2}'
          and distribution_center = '{0}'
        order by date asc 
        """.format(agency_id, from_, to_))
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    return df

# ---------------------------
# PREDICTION UTILS PROCEDURES
# ---------------------------

# prepare data for models
def prepare_daily_drivers_for_predictions(df, column = 'drivers'):
    # -----------------------
    # Prepare day of the week
    # -----------------------
    dow = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    df['DOW'] = df.index.dayofweek
    df = pd.concat([df, pd.get_dummies(df['DOW'], drop_first=True)], axis=1)
    df = df.rename(columns={i : dow[i] for i in range(7)})
    del df['DOW']

    # ---------------
    # Prepare holiday
    # ---------------
    df['holiday'] = 0

    for h in [h[0] for h in holidays]:
        d = pd.to_datetime(h)
        if d in df.index:
            df.loc[d, 'holiday'] = 1

    # -------------------------------------------
    # Prepare previous number of (column) drivers
    # -------------------------------------------
    df['prev_day'] = df[column]
    df.reset_index(inplace=True)

    for i in range(1, len(df)):
        df.loc[i, 'prev_day'] = df.loc[i-1, column]
    df.set_index('date', inplace=True)
    
    return df

# build and train a model
def get_daily_drivers_model(agency_id, today, column='drivers'):

    predictables = ['drivers', 'drivers_alo', 'drivers_alo_10_days']
    if column not in predictables:
        raise "ERROR"
        
    # read all
    df = get_daily_drivers(agency_id)
    
    for col in predictables:
        if col != column:
            del df[col]
    
    # prepare
    df = prepare_daily_drivers_for_predictions(df, column)
    
    train = df[df.index <= pd.to_datetime(today)]
    test = df[df.index > pd.to_datetime(today)]
    
    dates = df.index.tolist()
    dates_train = df[df.index <= pd.to_datetime(today)].index.tolist()
    dates_test = df[df.index > pd.to_datetime(today)].index.tolist()
    
    formula = 'np.sqrt({}) ~ '.format(column) + ' + '.join([col for col in df if col not in ['distribution_center', column]])
    formula = formula.replace('prev_day', 'np.sqrt(prev_day)')
    #print(formula)
    model = smf.ols(formula = formula, data = train).fit()
    #print(model.summary())    

    return model, train, test, dates_train, dates_test

# ---------------------------------------------------------------
# [APP]: Usable to predict number of daily unique drivers per day
# ---------------------------------------------------------------
def predict_daily_unique_drivers(agency_id, today, column='drivers', days=7):
    model, train, test, dates_train, dates_test = get_daily_drivers_model(agency_id, today, column)
    
    test = test.head(days)
    dates_test = dates_test[:days]
    
    t = test.copy()
    del t['distribution_center']
    t = t.reset_index()
    t[column] = 0
    t['prev_day'] = 0
    t.loc[t.index[0], 'prev_day'] = train[train.index == train.index[-1]][column].item()
    
    for i in range(len(t)):
        #print(i, np.square(model.predict(t.iloc[i]).item()))
        #print('.', end='')
        p = np.square(model.predict(t.loc[t.index == t.index[i], :])).item()
        t.loc[t.index == t.index[i], column] = p
        # np.square(model.predict(t.iloc[i]).item())
        if i < len(t)-1:
            t.loc[t.index == t.index[i+1], 'prev_day'] = p
       
    test['prediction'] = np.round(pd.DataFrame({column: t[column].values}, index=dates_test)[column])
    
    return test[[column, 'prediction']]


# START FLASK
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Planify(Resource):
    def get(self):
        return 'Planify API'

class DailyDrivers(Resource):
    def get(self):
        return 'API expects params: agency_id, date and steps'

class DailyDriversFor(Resource):

    def get(self, agency_id, date, steps):
        print(agency_id, date, steps)
        if agency_id not in agencies: return {'error': 'invalid agency_id'}
        df = predict_daily_unique_drivers(agency_id, date, column='drivers', days=min(int(steps), 30))
        return df.to_json()

api.add_resource(Planify, '/')
api.add_resource(HelloWorld, '/hello')
api.add_resource(DailyDrivers, '/daily-drivers')
api.add_resource(DailyDriversFor, '/daily-drivers/<agency_id>/<date>/<steps>/')


if __name__ == '__main__':
    app.run(debug=True)