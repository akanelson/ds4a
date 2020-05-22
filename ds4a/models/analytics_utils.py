import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.formula.api as smf
from practicum_utils import get_loggi_files, global_connect, run_query, explained_time, careful_query

# ----------------------
# hard coded agencies ID
# ----------------------
agency = {'1': '6e7dacf2149d053183fe901e3cfd8b82', '2': '58cfe3b975dd7cbd1ac84d555640bfd9'}
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


# -----------------------------------------------------------------------
# [APP]: Useful to obtain history of unique number of itineraries per day
# -----------------------------------------------------------------------
def get_daily_itineraries(agency_id, from_='2019-10-01', to_='2020-03-31'):
    
    df = careful_query("""
        select date(created_time) as date, count(distinct(itinerary_id)) as itineraries
        from itinerary
        where created_time >= '{1}'
          and created_time < '{2}'
          and distribution_center = '{0}'
        group by date(created_time)
        order by date asc 
        """.format(agency_id, from_, to_))
    
    date = pd.date_range(start=from_, end=to_) 
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = pd.concat([df, pd.DataFrame(index=date)], axis=1).fillna(0)
    df = df.reset_index().rename(columns={'index':'date'}).set_index('date', drop=True)
    return df


# ------------------------------------------------------------------------------
# [APP]: Useful to obtain the itineraries situation hour by hour for a given day
# ------------------------------------------------------------------------------
def get_hourly_day_itineraries(agency_id, today_time):
    
    today = today_time[:10]
    #today_date = datetime.strptime(today, '%Y-%m-%d')    
    #tomorrow_date = today_date + timedelta(days=1) 
    #tomorrow = str(tomorrow_date)[:10]
    
    df = careful_query("""
        select * from pending_oozma
        where date_time >= '{1}'
          and date_time <  '{2}'
          and distribution_center = '{0}'
        --group by distribution_center, date_time
        order by date_time asc
        """.format(agency_id, today, today_time))
    

    df.set_index('date_time', drop=True, inplace=True)
    
    return df

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

# --------------------------------------------------------------------
# [APP]: Useful to obtain history of unique number of drivers per hour
# --------------------------------------------------------------------
def get_hourly_drivers(agency_id, from_='2019-10-01', to_='2020-03-31'):
    
    df = careful_query("""
        select *
        from unique_drivers_hourly_oozma
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

# prepare data for models
def prepare_hourly_drivers_for_predictions(df, today_time, column = 'drivers'):

    # precalculate number of column drivers in previous hour
    df['prev_hour'] = df[column]
    df.reset_index(inplace=True)
    
    if len(today_time) == 10:
        today_time += ' 00'

    for i in range(1, len(df)):
        df.loc[i, 'prev_hour'] = df.loc[i-1, column]

    df.set_index('date', inplace=True)
    
    # calculate average number of drivers for ra given hour for a given day of the week
    # TODO: we could use just the last four weeks as a maximum
    avg_per_dow_and_hour = []
    for i in range(7):
        condition = (df.index.dayofweek == i)
        if len(today_time) > 0:
            condition = condition & (df.index < today_time[:13])
        
        if len(df[condition]) == 0:
            raise 'There is not enough data to build the hourly prediction model'
        avg_per_dow_and_hour.append(
            df[condition].groupby(df[condition].index.hour)[column].mean().reset_index(drop=True)
        )
    #print(avg_per_dow_and_hour)

    df['hour'] = df.index.hour
    
    df['historical_avg'] = 0
    for day in range(7):
        for hour in range(24):
            df.loc[(df.index.dayofweek == day)
                & (df.index.hour == hour), 'historical_avg'] = avg_per_dow_and_hour[day][hour]
    
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
    
    train = df[df.index < pd.to_datetime(today)]
    test = df[df.index >= pd.to_datetime(today)]
    
    dates = df.index.tolist()
    dates_train = df[df.index < pd.to_datetime(today)].index.tolist()
    dates_test = df[df.index >= pd.to_datetime(today)].index.tolist()
    
    formula = 'np.sqrt({}) ~ '.format(column) + ' + '.join([col for col in df if col not in ['distribution_center', column]])
    formula = formula.replace('prev_day', 'np.sqrt(prev_day)')
    #print(formula)
    model = smf.ols(formula = formula, data = train).fit()
    #print(model.summary())    

    return model, train, test, dates_train, dates_test

# build and train the model
def get_hourly_drivers_model(agency_id, today_time, column='drivers'):

    predictables = ['drivers', 'drivers_alo', 'drivers_alo_10_days']
    if column not in predictables:
        raise "ERROR"
        
    # read all
    # TODO: this is not necessary
    df = get_hourly_drivers(agency_id)
    
    for col in predictables:
        if col != column:
            del df[col]
    
    # prepare
    df = prepare_hourly_drivers_for_predictions(df, today_time, column)
    
    train = df[df.index < pd.to_datetime(today_time)]
    test = df[df.index >= pd.to_datetime(today_time)]
    
    dates = df.index.tolist()
    dates_train = df[df.index < pd.to_datetime(today_time)].index.tolist()
    dates_test = df[df.index >= pd.to_datetime(today_time)].index.tolist()
    
    formula = 'np.power({}, 0.32) ~ '.format(column) + ' + '.join([col for col in df if col not in ['distribution_center', column]])
    formula = formula.replace('prev_hour', 'np.power(prev_hour, 0.32)')
    formula = formula.replace('historical_avg', 'np.power(historical_avg, 0.32)')
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


# ----------------------------------------------------------------
# [APP]: Usable to predict number of hourly unique drivers per day
# ----------------------------------------------------------------
def predict_hourly_unique_drivers(agency_id, today_time, column='drivers', hours=48):
    model, train, test, dates_train, dates_test = get_hourly_drivers_model(agency_id, today_time , column)
    
    test = test.head(hours)
    dates_test = dates_test[:hours]
    

    t = test.copy()
    del t['distribution_center']
    t = t.reset_index()
    t[column] = 0
    t['prev_hour'] = 0
    t.loc[t.index[0], 'prev_hour'] = train[train.index == train.index[-1]][column].item()
    
    for i in range(len(t)):
        #print(i, np.square(model.predict(t.iloc[i]).item()))
        #print('.', end='')
        p = np.power(model.predict(t.loc[t.index == t.index[i], :]), 1/0.32).item()
        t.loc[t.index == t.index[i], column] = p
        if i < len(t)-1:
            t.loc[t.index == t.index[i+1], 'prev_hour'] = p
       
    test['prediction'] = np.round(pd.DataFrame({column: t[column].values}, index=dates_test)[column])
    
    return test[[column, 'prediction']]

    