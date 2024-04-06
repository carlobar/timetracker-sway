# timetracker-sway
Time tracker for Sway

## Install
To install the time tracker run

`make install` 

This command does the follwoing: 
1. Copies the scripts in the folder ~/.timetracker-sway
2. Creates an alias named `time-stats` to get the statistics of the time usage

## Execution
Execute the following to start recording the activity

`./.timetracker-sway/record_activity.sh`

This script records the information from the active window wvery 60 seconds.

On Sway this can be executed at the startup adding the following to .config/sawy/config 

`exec ~/.timetracker-sway/record_activity.sh`

The statistics of time usage are generated executing 'time-stats'
`$ time-stats
other:                     01:21 (75.70%)
coding:                    00:23 (21.50%)
games:                      00:03 (2.80%)
`

## Configuration
The time tracker gets information from the current window of the form 
> 'LIVE FACEBOOK - YouTube — Mozilla Firefox'

The script `pre-process.py` attempts to get the title and program name, assuming that the information has the following format:
`title - program`

This information is recorded in the file 'record.csv'

The time statistics obtained with `time-stats` are generated with the script 'get_stats.py'. This script checks whether an entry match the patterns defined in the file '~/.timetracker-sway/categories.py'.

A pattern is defined as a dictionary of the form
`re_coding = {
    'program': ['IPython'],
    'title': ['\.py', '\.sh', 'python']
}`

The script tries to match each pattern to the program or title entries recorded.

## To DO

1. It would be interesting to create a plot with the time usage during a day
2. Check whether we record the activity when the computer is inactive

