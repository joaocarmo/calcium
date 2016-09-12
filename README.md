# Calcium data process

Python code to process some lab data on calcium absorption.

## Requirements

To run the code, the following libraries are required:
* Python 2.x
* SciPy
* NumPy
* Matplotlib

Detailed information on obtaining, using and installing these can be found [here](http://www.scipy.org/install.html).

Linux and OS X usually come with python 2.x already installed, but the scientific libraries still need to be installed.

To check whether you have python already installed in your system, open the terminal and type `python -V`. If you see something like `Python x.xx.xx`, then you already have Python. If you get an error, then you need to install it.

## Run the process

The script is contained within a single file `calcium.py` and executing it is as easy as typing `python calcium.py`, within the project folder, on the terminal, after installing the requirements above.

You can simply download the entire repository or, if you're using _git_, just clone it with `git clone <address to this repository>`.

## In a nutshell

The script starts by importing the `scipy`, `csv`, `numpy` and `matplotlib` libraries. Then, some settings can be easily adjusted by just changing some variables:
* Show Plots: True/False
* Data Source: File location (CSV format)
* Start of the relevant data points
* End of the relevant data points

The script proceeds to import the data from the source `.csv` file and filters it to considers only the data points within the range defined in the settings.

It uses the previously considered data to find the best regression fit according to the assumed model. Data integration is performed using two different methods: a numerical integration using the actual data and an analytic integration using the estimated model.

Finally, if the _show plots_ setting is set to true, the script draws some graphs to display the results and outputs the results to the terminal.

## Data source

The script expects the data to be in a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format. This can be done in a [spreadsheet](https://en.wikipedia.org/wiki/List_of_spreadsheet_software) such as _OpenOffice.org Calc_ or _Microsoft Office Excel_ simply by selecting _Save As..._ `Comma-separated values (CSV)`.

#### Original file

![original file](/docs/file1.png)

Columns in red have been removed, the script calculates the _mean_ for better results.

#### Prepared file

![prepared file](/docs/file2.png)

This is an example of how the source file should look like and the line numbers can be used to set the start and end of the data points.

## Model

The assumed model that better describes the observed behavior can be found in the `/docs/equations.pdf` file.

#### Exponential function

After some trial and error, it seemed to me that the best fit for the range of data we're interested in is given by `equation 1`. This can be linearized by applying logarithms as in `equation 2` and thus we can use a simple linear regression on the data to obtain the values for the constants `A` and `B`. We are finally able to compute the expected values given by the model and compare them to the data.

###### Equation 1
![equation 1](/docs/eq1.png)

###### Equation 2
![equation 1](/docs/eq2.png)

## Fitting the data

From the data samples included, we are already able to display some graphs (see the `docs`).

#### The original data with a polynomial fit

Below is the original data plotted as a graph of fluorescence (rfu) against time (t) and a 3rd degree polynomial fit just to show how the data trends.

![plot 1](/docs/figure_1.png)

#### The linearized data

The second graph is a plot of a limited range of the data linearized according to `equation 2`.

![plot 2](/docs/figure_2.png)

#### The model and the data

The final plot shows how the model fits the selected range of data we used to compute the values for model's constants `A` and `B`.

![plot 3](/docs/figure_3.png)

#### The results

The regression returned the output in the box below:
```
A = 6.43869071324
B = -0.458188646779
R2 = 0.941528151585
```

As expected, the value for `B` in negative and inferior to 1. The correlation between the model and the selected range of data is high (close to 1) and given by the coefficient of determination `R2`.
