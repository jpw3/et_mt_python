#HDDMfit runs the HDDM fit on saved .csvs
#Author: James Wilmott

#Can I use an aggregate (a la, an 'omnibus') .csv file for this?
#Im separating out distinct DDM models for the task type contrast, the nr targets contrast, and the hf relation contrasts


#import relevant packages
from pylab import *
import hddm

savepath = '/Users/james/Documents/Python/et_mt/data/'; #

### first let's play with the discrimination vs. detection targets comparison

#0. load in the relevant csv
data = hddm.load_csv(savepath+'task_type_data.csv');

#0.1.0 flip the errors so that error RTs are 'negative'
data = hddm.utils.flip_errors(data);

#0.1.1 plot the distribution of RTs to see what everything looks like..
fig = figure();
ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'RT Distribution for Correct and Error Trials');
#loop to histogram each subjects' RT distributions
for i,subj in data.groupby('subj_id'):
     subj.rt.hist(bins=20, histtype = 'step', ax = ax);
	 

#0.2 Fit an DDM hierarchically using hddm's functionality


