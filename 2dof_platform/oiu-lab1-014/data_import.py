"""
Simple script for importing CSV-formatted data.
"""

import csv
import numpy
import argparse
import os

def read(file_name, column_names):
    """
    Import CSV formatted data from file_name.
    
    Returns a dict with column_names as keys.
    """
    
    data = dict()
    for c in column_names:
        data[c] = []
        
    with open(file_name, 'rb') as logfile:
        reader = csv.reader(logfile)
        for row in reader:
            row = row[0].split(';')
            for c, x in zip(column_names,row):
                data[c].append(float(x))
    
    for c in column_names:
        data[c] = numpy.array(data[c])
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data loading script.')
    parser.add_argument('--file_name',help='File containing experimental data.',default='')
    parser.add_argument('--newest',action='store_true',help='Load the newest file.')
    args = parser.parse_args()

    logfile = ''
    if args.newest:
        files = [f for f in os.listdir('.') if f.endswith('.csv')]
        files.sort()
        if files:
            logfile = files[-1]
    elif args.file_name:
        logfile = args.file_name
    else:
        raise Exception('Please either specify a file with the --file name flag, or just the newest file with --newest')

    print('Loading data from file {0}'.format(logfile))
    data = read(logfile, ['t','x','y','x_ref','y_ref','phi_1','phi_2'])
    t = data['t'] - data['t'][0]
    x = data['x']
    y = data['y']
    x_ref = data['x_ref']
    y_ref = data['y_ref']
    phi_1 = data['phi_1']
    phi_2 = data['phi_2']
    
