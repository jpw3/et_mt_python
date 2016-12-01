#Multiple Target (Eyetracking Condition) Plotting code
#Author: James Wilmott, Winter 2016

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import shelve #for database writing and reading

datapath = '/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #'/Users/james/Documents/MATLAB/data/et_mt_data/'; #
shelvepath =  '/Users/jameswilmott/Documents/Python/et_mt/data/'; #'/Users/james/Documents/Python/et_mt/data/'; #

subject_data = shelve.open(shelvepath+'mt_data.db');
individ_subject_data = shelve.open(shelvepath+'individ_mt_data.db');

ids = ['jpw']; #use 'agg' for aggregate subject data
block_types = ['Discrim','Detect'];