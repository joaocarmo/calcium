#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# Library imports
from __future__ import division
from scipy import stats
from scipy.integrate import quad
from scipy.integrate import simps
import csv
import numpy as np
import matplotlib.pyplot as plt

# --- SETTINGS START --- #

# Show data plots
showPlots = True
# Data sorce
data = 'data_calcium_handling.csv'
# Ignore the first X data points from the source
start = 7
# Where to cutoff the data points for the analysis
cutoff = 25

# ---- SETTINGS END ---- #

# Arrays to hold the raw data
x1 = []
x2 = []
x3 = []
x4 = []
sec = []

# Read the source and pass it to the arrays
with open(data, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        x1.append(row[0])
        x2.append(row[1])
        x3.append(row[2])
        x4.append(row[3])
        sec.append(row[4])

x1_s = x1[start:]
x2_s = x2[start:]
x3_s = x3[start:]
x4_s = x4[start:]
sec_s = sec[start:]

# New arrays for the treated data
avg_x = []
time = []

# Populate the arrays with the Mean of x1, x2, x3 and x4
for i in range(len(x1_s)):
    avg_x.append( np.mean( [ float(x1_s[i]), float(x2_s[i]), float(x3_s[i]), float(x4_s[i]) ] ) )
    time.append( float(sec_s[i]) )

# Interpolate as a 3rd degree polinomial
z = np.polyfit(time, avg_x, 3)
p = np.poly1d(z)
avg_fit = p(time)

# Interpolate the first X data points as log f = A + B log t
log_avg_x = np.log(avg_x[:cutoff])
log_time = np.log(time[:cutoff])
slope, intercept, r_value, p_value, std_err = stats.linregress(log_time, log_avg_x)
p2 = np.poly1d([slope, intercept])
avg_log_fit = p2(log_time)
r2_value = r_value ** 2

# Get the value of A from ln A and of B from the slope
A = np.exp(intercept)
B = slope

def f(t):
    return A * t ** B

# Integrate the interpolated function
I = quad(f, time[0], time[cutoff])

# Integrate using the data
I_data = simps(avg_x[:cutoff], time[:cutoff])

# Calculate the total area of the rectangle
height = avg_x[0]
width = time[cutoff] - time[0]
total_area = height * width

# Get the differences
diff_I = total_area - I[0]
diff_I_data = total_area - I_data

# Print out the results to the console
print '\nfirst point (' + str(avg_x[0]) + ', ' + str(time[0]) + ')' + '\nlast point (' + str(avg_x[cutoff]) + ', ' + str(time[cutoff]) + ')\n\n'
print '\nlog f(t) = ln A + B x log t\n' + '\nA = ' + str(A) + '\nB = ' + str(slope) + '\nR2 = ' + str(r2_value) + '\n\n'
print '\nthe integral of f(t) = ' + str(A) + ' x t ^ ' + str(B) + '\nfrom ' + str(time[0]) + 's to ' + str(time[cutoff]) + 's is\n\nI-func = ' + str(I[0]) + '\n\n'
print '\nthe numerical integral of the data from the first point to the last is\n\nI-data = ' + str(I_data) + '\n\n'
print '\nthe total area of the rectangle which includes the\nfirst and last points as vertices is\n\nArea = ' + str(total_area) + '\n\n'
print '\nthe difference in area - integral is, respectively\n\nArea - I-func = ' + str(diff_I) + '\nArea - I-data = ' + str(diff_I_data) + '\n\n'

# Plot the graph figures
if showPlots:
    fig1 = plt.figure(1)
    plt.plot(time, avg_x, 'bx', time, avg_fit, 'r--')
    plt.xlabel('time (s)')
    plt.ylabel('fluorescence (rfu)')
    plt.title('Data with a 3rd degree polynomial fit')

    fig2 = plt.figure(2)
    plt.plot(log_time, log_avg_x, 'bx', log_time, avg_log_fit, 'r--')
    plt.xlabel('log time (s)')
    plt.ylabel('log fluorescence (rfu)')
    plt.title('Data on a logarithmic scale with a linear fit')

    fig3 = plt.figure(3)
    plt.plot(time, avg_x, 'bx', time[:cutoff], f(time[:cutoff]), 'r--')
    plt.xlabel('time (s)')
    plt.ylabel('fluorescence (rfu)')
    plt.title('Data with the linear fit')
    plt.show()
