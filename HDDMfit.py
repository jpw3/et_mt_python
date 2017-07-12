#HDDMfit runs the HDDM fit on saved .csvs
#Author: James Wilmott

#Can I use an aggregate (a la, an 'omnibus') .csv file for this?
#Im separating out distinct DDM models for the task type contrast, the nr targets contrast, and the hf relation contrasts


#import relevant packages
from pylab import *
import hddm

savepath = '/Users/james/Documents/Python/et_mt/data/'; #

# ### 0. first let's play with the discrimination vs. detection targets comparison
# 
# #0.0 load in the relevant csv
# tt_data = hddm.load_csv(savepath+'task_type_data.csv');
# 
# #0.1.0 flip the errors so that error RTs are 'negative'
# tt_data = hddm.utils.flip_errors(tt_data);
# 
# # #0.1.1 plot the distribution of RTs to see what everything looks like..
# # fig = figure();
# # ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Task Type RT Distribution for Correct and Error Trials');
# # #loop to histogram each subjects' RT distributions
# # for i,subj in tt_data.groupby('subj_idx'):
# #      subj.rt.hist(bins=20, histtype = 'step', ax = ax);
# 	 
# 
# #0.2 Fit an DDM hierarchically using hddm's functionality
# 
# ## Example of how to do this... ##
# 
# #tt_model = hddm.HDDM(tt_data, informative = True, depends_on = {'v':'task_type'});
# #^ this call instantiates an HDDM model. informative = True uses informative priors (i.e. starting points are drawn from likely distributions) when fitting the DDM
# #the call to allow v to depend on task_type allows me to test differences in the group fit parameters for that model
# #note, I'm not fitting a 'bias' parameter z here because I'm using error coding for responses where 1 is correct and 0 is incorrect, so it doesn't make sense to model it as such
# #tt_model.find_starting_values(); #this gets good starting points to help with the convergence of the model fitting
# #tt_model.sample(10000, burn = 25); #this samples from the posterior distribution of the model to fit the model to the data. burn argument specifies first N iterations to drop
# #note, for my et_mt data, I ran a simulation of 6 models for this set of models and checked out the Gelman-Rubin statistic for convergence.
# # It seems like 5000 iterations, burning the first 25, gets a really good convergence stat (a,v, and t group params less than 1.1, individual subjects also all less than 1.1)
# 
# ##
# 
# #here, loop through and allow each of the potential parameters to vary along the task_type call. This way I can see what 'comes out' from the differences in task 
# models = [];
# for param in ['v','a','t']:
# 	print 'Starting the fitting for parameter %s...'%param; print ;
# 	tt_model = hddm.HDDM(tt_data, informative = True, depends_on = {'%s'%param:'task_type'}); #allow each parameter type to vary
# 	tt_model.find_starting_values(); #find realistic, appropriate starting values
# 	tt_model.sample(10000, burn = 50); #sample from the posterior distribution of the model
# 	print ;  print 'Plotting the posteriors for this model run...'; print ;
# 	tt_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
# 	print ; print '### Parameter fit summary for this model ###'; print; print;
# 	tt_model.print_stats(); #prints a, v, and t
# 	print ; print 'Plotting the posteriors for the fit model for parameter %s...'%param; print ;
# 	nodes = tt_model.nodes_db.node[['%s(Discrim)'%param,'%s(Detect)'%param]]; #get the relevant 'nodes' (posteriors?)
# 	hddm.analyze.plot_posterior_nodes(nodes); #this should plot the two together
# 	#save the model for use later
# 	hddm.save(savepath+'tt_depends_on_%s'%param);
# 	models.append(tt_model); #append the model to the list
# 	print 'Completed checking out models for parameter %s!'%param; print ;
# 	
# #note, while I'm checking out the models and saving the models I will need to check for convergence AND FIT for any models I want to explore in more depth


### 1. Now do the nr of target stuff independantly for discrimination and detection tasks

print ; print 'Starting # of target contrasts'; 
print 'Detection task first...'; print ;

#1.0 Detection task first...
#1.0.1 load in the data
det_nr_data = hddm.load_csv(savepath+'nr_target_det_data.csv');
#1.0.2 flip the errors so that error RTs are 'negative'
det_nr_data = hddm.utils.flip_errors(det_nr_data);
# #1.0.3 plot the distribution of RTs to see what everything looks like..
# fig = figure();
# ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# #loop to histogram each subjects' RT distributions
# for i,subj in tt_data.groupby('subj_idx'):
#      subj.rt.hist(bins=20, histtype = 'step', ax = ax);

# 1.0.4 Fit each model independently, allowing each a,t, and v to vary accordingly

models = [];
for param in ['v','a','t']:
	print 'Starting the fitting for parameter %s...'%param; print ;
	model = hddm.HDDM(det_nr_data, informative = True, depends_on = {'%s'%param:'nr_targets'}); #allow each parameter type to vary
	model.find_starting_values(); #find realistic, appropriate starting values
	model.sample(10000, burn = 50); #sample from the posterior distribution of the model
	print ;  print 'Plotting the posteriors for this model run...'; print ;
	model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
	#print ; print '### Parameter fit summary for this model ###'; print; print;
	#tt_model.print_stats(); #prints a, v, and t
	print ; print 'Plotting the posteriors for the fit model for parameter %s...'%param; print ;
	nodes = model.nodes_db.node[['%s(0.0)'%param,'%s(1.0)'%param,'%s(2.0)'%param]]; #get the relevant 'nodes' (posteriors?)
	hddm.analyze.plot_posterior_nodes(nodes); #this should plot the two together
	#save the model for use later
	model.save(savepath+'det_nr_depends_on_%s'%param);
	models.append(model); #append the model to the list
	print 'Completed checking out models for parameter %s!'%param; print ;
	
print ; print 'Now Discrimination task...'; print ;

#1.0 Detection task first...
#1.0.1 load in the data
dis_nr_data = hddm.load_csv(savepath+'nr_target_dis_data.csv');
#1.0.2 flip the errors so that error RTs are 'negative'
dis_nr_data = hddm.utils.flip_errors(dis_nr_data);
# #1.0.3 plot the distribution of RTs to see what everything looks like..
# fig = figure();
# ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# #loop to histogram each subjects' RT distributions
# for i,subj in tt_data.groupby('subj_idx'):
#      subj.rt.hist(bins=20, histtype = 'step', ax = ax);

# 1.0.4 Fit each model independently, allowing each a,t, and v to vary accordingly

models = [];
for param in ['v','a','t']:
	print 'Starting the fitting for parameter %s...'%param; print ;
	model = hddm.HDDM(dis_nr_data, informative = True, depends_on = {'%s'%param:'nr_targets'}); #allow each parameter type to vary
	model.find_starting_values(); #find realistic, appropriate starting values
	model.sample(10000, burn = 50); #sample from the posterior distribution of the model
	print ;  print 'Plotting the posteriors for this model run...'; print ;
	model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
	#print ; print '### Parameter fit summary for this model ###'; print; print;
	#tt_model.print_stats(); #prints a, v, and t
	print ; print 'Plotting the posteriors for the fit model for parameter %s...'%param; print ;
	nodes = model.nodes_db.node[['%s(0.0)'%param,'%s(1.0)'%param,'%s(2.0)'%param]]; #get the relevant 'nodes' (posteriors?)
	hddm.analyze.plot_posterior_nodes(nodes); #this should plot the two together
	#save the model for use later
	model.save(savepath+'dis_nr_depends_on_%s'%param);
	models.append(model); #append the model to the list
	print 'Completed checking out models for parameter %s!'%param; print ;


