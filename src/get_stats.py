# script to analyze the activity

import pandas as pd
import re
import pdb
import numpy as np
from datetime import datetime
from categories import patterns

'''
Check if a given pattern matches an element
'''
def match(pattern, element):
    for key in pattern.keys():
        try:
            for s in pattern[key]:
                pt = re.compile(s)
                if not pd.isnull(element[key]) and pt.search( element[key] ) != None:
                    return True
        except:
            print("Failed matching the key '{}' in the element {}".format(key, element))        
            #pdb.set_trace()
    return False

'''
Create a list with the patterns that match an element {title, program}
'''
def classify_element(patterns, element):
    matches = []
    for category in patterns.keys():
        if match(patterns[category], element):
            matches.append(category)
    if len(matches) == 0:
        matches = ['other']
    return matches    

'''
For each entry find the patterns that match
'''    
def classify_df(patterns, df):
    n = len(df)
    labels = ['' for i in range(n)]
    for i in range(n):
        element = {'title': df.iloc[i]['title'], 'program': df.iloc[i]['program']}
        labels[i] = classify_element(patterns, element)
    return labels
    
'''
Get the number of matches for each pattern cathegory
'''    
def get_freq(df, patterns):
    freq_categories = {key: 0 for key in patterns.keys()}

    for i in range(len(df)):
        labels = df.iloc[i]['class']
        for l in labels:
            freq_categories[l] += 1
    return freq_categories

'''
Get samples from last x days
'''
def select_recent_samples(df, d):
    # find the range of samples
    n = len(df)
    min_time = dt_sec - d*24*60*60
    
    for i in range(n):
        if min_time > df.loc[n-i-1, 'time']:  
            #print(i)
            break
    return df.loc[n-i-1:]

'''
Get the total time recorded for a given cathegory
'''
def get_time(freq, total):
    time = freq*sampling_period
    #weeks = time // (7*24*60*60)
    days = time // (24*60*60)
    time %= 24*3600
    hours = time // (3600)
    time %= 3600
    minutes = time // 60
    #seconds = time % 60
    if hours > 24:
        return '{} days and {:02d}:{:02d} ({:.2f}%)'.format(days, hours, minutes, freq/total*100)
    else: 
        return '{:02d}:{:02d} ({:.2f}%)'.format(hours, minutes, freq/total*100)


sampling_period = 60

dir_log = '~/.timetracker-sway/'
record_file = dir_log + 'record.csv'

df = pd.read_csv(record_file, sep=';', header=None, names=['time', 'window_name', 'program', 'title'])

df['class'] = classify_df(patterns, df)

# get current time
dt = datetime.today()
dt_sec = int(dt.timestamp())

# get the samples from the last day
df_range = select_recent_samples(df, 1)
m = len(df_range)
# get the frequency of each cathegory
freq_cat = get_freq(df_range, patterns)

#cat_exclude = set(['other'])
cat_exclude = set([''])


#print('Time Usage in the last 24h')
for x in sorted(freq_cat.items(), key=lambda item: item[1], reverse=True):
    if not x[0] in cat_exclude and x[1]>0:
        cathegory = x[0]
        usage = get_time(x[1], m)
        space = ''.join([' ' for j in range(40-len(cathegory)-len(usage))])
        print('{}:{}{}'.format( cathegory, space, usage) )


