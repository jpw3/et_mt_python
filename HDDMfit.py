#HDDMfit runs the HDDM fit on saved .csvs
#Author: James Wilmott

#Can I use an aggregate (a la, an 'omnibus') .csv file for this?
#Im separating out distinct DDM models for the task type contrast, the nr targets contrast, and the hf relation contrasts


#import relevant packages
from pylab import *
import hddm

savepath = '/Users/james/Documents/Python/et_mt/data/'; #

#This script is designed to fit the specific DDMs for each contrast with each potentially changing variable (i.e., a, v, and t)
#It is designed as an EDA. Anything that looks interesting MUST be explored in more detail with convergence and data fit explanations

### 0. first let's play with the discrimination vs. detection targets comparison

#0.0 load in the relevant csv
tt_data = hddm.load_csv(savepath+'task_type_data.csv');

#0.1.0 flip the errors so that error RTs are 'negative'
tt_data = hddm.utils.flip_errors(tt_data);
# 
# # #0.1.1 plot the distribution of RTs to see what everything looks like..
# # fig = figure();
# # ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Task Type RT Distribution for Correct and Error Trials');
# # #loop to histogram each subjects' RT distributions
# # for i,subj in tt_data.groupby('subj_idx'):
# #      subj.rt.hist(bins=20, histtype = 'step', ax = ax);
# 	 
# 
#0.2 Fit an DDM hierarchically using hddm's functionality

## Example of how to do this... ##

#tt_model = hddm.HDDM(tt_data, informative = True, depends_on = {'v':'task_type'});
#^ this call instantiates an HDDM model. informative = True uses informative priors (i.e. starting points are drawn from likely distributions) when fitting the DDM
#the call to allow v to depend on task_type allows me to test differences in the group fit parameters for that model
#note, I'm not fitting a 'bias' parameter z here because I'm using error coding for responses where 1 is correct and 0 is incorrect, so it doesn't make sense to model it as such
#tt_model.find_starting_values(); #this gets good starting points to help with the convergence of the model fitting
#tt_model.sample(10000, burn = 25); #this samples from the posterior distribution of the model to fit the model to the data. burn argument specifies first N iterations to drop
#note, for my et_mt data, I ran a simulation of 6 models for this set of models and checked out the Gelman-Rubin statistic for convergence.
# It seems like 5000 iterations, burning the first 25, gets a really good convergence stat (a,v, and t group params less than 1.1, individual subjects also all less than 1.1)

# # Fit a model allowing all three parameters to vary, and incorporate the additional sv and st parameters into it
# print 'Starting the fitting for task type HDDM'; print ;
# tt_model = hddm.HDDM(tt_data, informative = True, include=('sv', 'st'), depends_on = {'v':'task_type','a':'task_type','t':'task_type'}); #allow each parameter to vary
# tt_model.find_starting_values(); #find realistic, appropriate starting values
# tt_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# tt_model.plot_posteriors(['a','a_std','v','v_std','t','t_std','sv','st']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# tt_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_dis_node, v_det_node, a_dis_node, a_det_node, t_dis_node, t_det_node] = tt_model.nodes_db.node[['v(Discrim)','v(Detect)','a(Discrim)','a(Detect)','t(Discrim)','t(Detect)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_dis_node, v_det_node]);
# savefig(savepath+'tt_v_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_dis_node, a_det_node]);
# savefig(savepath+'tt_a_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_dis_node, t_det_node]);
# savefig(savepath+'tt_t_includesITV.png', dpi = 200); #save the figure
# #save the model for use later
# hddm.save(savepath+'tt_all_includesITV');
# print 'Completed checking out model with intertrial variability parameters...'; print ;


# # Fit a model allowing all three parameters to vary but without the intertrial variability params
# print 'Starting the fitting for task type HDDM without the inter trial varaiability params'; print ;
# tt_model = hddm.HDDM(tt_data, informative = True, depends_on = {'v':'task_type','a':'task_type','t':'task_type'}); #allow each parameter to vary
# tt_model.find_starting_values(); #find realistic, appropriate starting values
# tt_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# tt_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# tt_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model for parameter'; print ;
# [v_dis_node, v_det_node, a_dis_node, a_det_node, t_dis_node, t_det_node] = tt_model.nodes_db.node[['v(Discrim)','v(Detect)','a(Discrim)','a(Detect)','t(Discrim)','t(Detect)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_dis_node, v_det_node]);
# savefig(savepath+'tt_v.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_dis_node, a_det_node]);
# savefig(savepath+'tt_a.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_dis_node, t_det_node]);
# savefig(savepath+'tt_t.png', dpi = 200); #save the figure
# #save the model for use later
# #hddm.save(savepath+'tt_all');
# print 'Completed checking out model withOUT intertrial variability parameters...'; print ;


# #this is wrong, and is liable to find differences in parameters that don't have any because I'm forcing that param to describe the differences in the RT distributions
# #here, loop through and allow each of the potential parameters to vary along the task_type call. This way I can see what 'comes out' from the differences in task 
# models = [];
# for param in ['v','a','t']:
# 	print 'Starting the fitting for parameter %s...'%param; print ;
# 	tt_model = hddm.HDDM(tt_data, informative = True, include=('sv', 'st'), depends_on = {'%s'%param:'task_type'}); #allow each parameter type to vary
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
	
#note, while I'm checking out the models and saving the models I will need to check for convergence AND FIT for any models I want to explore in more depth


# ### 1. Now do the nr of target stuff independantly for discrimination and detection tasks
# 
# print ; print 'Starting # of target contrasts';  print; 
# print 'Detection task first...'; print ;
# 
# #1.0 Detection task first...
# #1.0.1 load in the data
# det_nr_data = hddm.load_csv(savepath+'nr_target_det_data.csv');
# #1.0.2 flip the errors so that error RTs are 'negative'
# det_nr_data = hddm.utils.flip_errors(det_nr_data);
# # #1.0.3 plot the distribution of RTs to see what everything looks like..
# # fig = figure();
# # ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# # #loop to histogram each subjects' RT distributions
# # for i,subj in tt_data.groupby('subj_idx'):
# #      subj.rt.hist(bins=20, histtype = 'step', ax = ax);
# 
# # 1.0.4 Fit each model independently, allowing each a,t, and v to vary accordingly
# 
# # Fit a model allowing all three parameters to vary, and incorporate the additional sv and st parameters into it
# print 'Starting the fitting for detection task, number of target HDDM'; print ;
# det_nr_model = hddm.HDDM(det_nr_data, informative = True, include=('sv', 'st'), depends_on = {'v':'nr_targets','a':'nr_targets','t':'nr_targets'}); #allow each parameter to vary
# det_nr_model.find_starting_values(); #find realistic, appropriate starting values
# det_nr_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# det_nr_model.plot_posteriors(['a','a_std','v','v_std','t','t_std','sv','st']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# det_nr_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_none_node, v_one_node, v_two_node, a_none_node, a_one_node, a_two_node, t_none_node, t_one_node, t_two_node] = det_nr_model.nodes_db.node[['v(0.0)','v(1.0)','v(2.0)','a(0.0)','a(1.0)','a(2.0)','t(0.0)','t(1.0)','t(2.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_none_node, v_one_node, v_two_node]);
# savefig(savepath+'det_nr_v_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_none_node, a_one_node, a_two_node]);
# savefig(savepath+'det_nr_a_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_none_node, t_one_node, t_two_node]);
# savefig(savepath+'det_nr_t_includesITV.png', dpi = 200); #save the figure
# #save the model for use later
# hddm.save(savepath+'det_nr_all_includesITV');
# print 'Completed checking out model with intertrial variability parameters...'; print ;
# 
# 
# # Fit a model allowing all three parameters to vary but without the intertrial variability params
# print 'Starting the fitting for detection task, number of target HDDM'; print ;
# det_nr_model = hddm.HDDM(det_nr_data, informative = True, depends_on = {'v':'nr_targets','a':'nr_targets','t':'nr_targets'}); #allow each parameter to vary
# det_nr_model.find_starting_values(); #find realistic, appropriate starting values
# det_nr_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# det_nr_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# det_nr_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_none_node, v_one_node, v_two_node, a_none_node, a_one_node, a_two_node, t_none_node, t_one_node, t_two_node] = det_nr_model.nodes_db.node[['v(0.0)','v(1.0)','v(2.0)','a(0.0)','a(1.0)','a(2.0)','t(0.0)','t(1.0)','t(2.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_none_node, v_one_node, v_two_node]);
# savefig(savepath+'det_nr_v.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_none_node, a_one_node, a_two_node]);
# savefig(savepath+'det_nr_a.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_none_node, t_one_node, t_two_node]);
# savefig(savepath+'det_nr_t.png', dpi = 200); #save the figure
# #save the model for use later
# hddm.save(savepath+'det_nr_all');
# models.append(tt_model); #append the model to the list
# print 'Completed checking out model withOUT intertrial variability parameters...'; print ;
# 
# 
# print ; print 'Now Discrimination task...'; print ;
# 
# #1.1 Discrimination task...
# #1.1.1 load in the data
# dis_nr_data = hddm.load_csv(savepath+'nr_target_dis_data.csv');
# #1.1.2 flip the errors so that error RTs are 'negative'
# dis_nr_data = hddm.utils.flip_errors(dis_nr_data);
# # #1.1.3 plot the distribution of RTs to see what everything looks like..
# # fig = figure();
# # ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# # #loop to histogram each subjects' RT distributions
# # for i,subj in tt_data.groupby('subj_idx'):
# #      subj.rt.hist(bins=20, histtype = 'step', ax = ax);
# 
# # 1.1.4 Fit each model independently, allowing each a,t, and v to vary accordingly
# 
# # Fit a model allowing all three parameters to vary, and incorporate the additional sv and st parameters into it
# print 'Starting the fitting for discrimination task, number of target HDDM'; print ;
# dis_nr_model = hddm.HDDM(dis_nr_data, informative = True, include=('sv', 'st'), depends_on = {'v':'nr_targets','a':'nr_targets','t':'nr_targets'}); #allow each parameter to vary
# dis_nr_model.find_starting_values(); #find realistic, appropriate starting values
# dis_nr_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# dis_nr_model.plot_posteriors(['a','a_std','v','v_std','t','t_std','sv','st']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# dis_nr_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_one_node, v_two_node, a_one_node, a_two_node, t_one_node, t_two_node] = dis_nr_model.nodes_db.node[['v(1.0)','v(2.0)','a(1.0)','a(2.0)','t(1.0)','t(2.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_one_node, v_two_node]);
# savefig(savepath+'dis_nr_v_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_one_node, a_two_node]);
# savefig(savepath+'dis_nr_a_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_one_node, t_two_node]);
# savefig(savepath+'dis_nr_t_includesITV.png', dpi = 200); #save the figure
# #save the model for use later
# hddm.save(savepath+'dis_nr_all_includesITV');
# print 'Completed checking out model with intertrial variability parameters...'; print ;
# 
# 
# # Fit a model allowing all three parameters to vary but without the intertrial variability params
# print 'Starting the fitting for discrimination task, number of target HDDM'; print ;
# dis_nr_model = hddm.HDDM(dis_nr_data, informative = True, depends_on = {'v':'nr_targets','a':'nr_targets','t':'nr_targets'}); #allow each parameter to vary
# dis_nr_model.find_starting_values(); #find realistic, appropriate starting values
# dis_nr_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# dis_nr_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# dis_nr_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_one_node, v_two_node, a_one_node, a_two_node, t_one_node, t_two_node] = dis_nr_model.nodes_db.node[['v(1.0)','v(2.0)','a(1.0)','a(2.0)','t(1.0)','t(2.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_one_node, v_two_node]);
# savefig(savepath+'dis_nr_v.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_one_node, a_two_node]);
# savefig(savepath+'dis_nr_a.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_one_node, t_two_node]);
# savefig(savepath+'dis_nr_t.png', dpi = 200); #save the figure
# #save the model for use later
# hddm.save(savepath+'dis_nr_all');
# print 'Completed checking out model withOUT intertrial variability parameters...'; print ;
	
	
# # # 2.0 EDA fitting for the SAME vs. DIFFERENT HF contrast
# 
print ; print 'Starting hemifield relation contrasts'; 
print 'Detection task first...'; print ;

#2.0 Detection task first...
#2.0.1 load in the data
det_hf_data = hddm.load_csv(savepath+'hf_det_data.csv');
#2.0.2 flip the errors so that error RTs are 'negative'
det_hf_data = hddm.utils.flip_errors(det_hf_data);
# #2.0.3 plot the distribution of RTs to see what everything looks like..
# fig = figure();
# ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# #loop to histogram each subjects' RT distributions
# for i,subj in tt_data.groupby('subj_idx'):
#      subj.rt.hist(bins=20, histtype = 'step', ax = ax);

# 2.0.4 Fit each model independently, allowing each a,t, and v to vary accordingly

det_hf_model = hddm.HDDM(det_hf_data, informative = True, include=('sv', 'st'), depends_on = {'v':'same_hf','a':'same_hf','t':'same_hf'}); #allow each parameter to vary
det_hf_model.find_starting_values(); #find realistic, appropriate starting values
det_hf_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
print ;  print 'Plotting the posteriors for this model run...'; print ;
det_hf_model.plot_posteriors(['a','a_std','v','v_std','t','t_std','sv','st']);
print ; print '### Parameter fit summary for this model ###'; print; print;
det_hf_model.print_stats(); #prints a, v, and t
print ; print 'Plotting the posteriors for the fit model'; print ;
[v_diff_node, v_same_node, a_diff_node, a_same_node, t_diff_node, t_same_node] = det_hf_model.nodes_db.node[['v(0.0)','v(1.0)','a(0.0)','a(1.0)','t(0.0)','t(1.0)']]; #get the relevant 'nodes' (posteriors?)
#run through each parameter and plot seperately, saving each
hddm.analyze.plot_posterior_nodes([v_diff_node, v_same_node]);
savefig(savepath+'det_hf_v_includesITV.png', dpi = 200); #save the figure
hddm.analyze.plot_posterior_nodes([a_diff_node, a_same_node]);
savefig(savepath+'det_hf_a_includesITV.png', dpi = 200); #save the figure
hddm.analyze.plot_posterior_nodes([t_diff_node, t_same_node]);
savefig(savepath+'det_hf_t_includesITV.png', dpi = 200); #save the figure
#save the model for use later
#hddm.save(savepath+'dis_nr_all');
print 'Without ITV params next...'; print ;

det_hf_model = hddm.HDDM(det_hf_data, informative = True, depends_on = {'v':'same_hf','a':'same_hf','t':'same_hf'}); #allow each parameter to vary
det_hf_model.find_starting_values(); #find realistic, appropriate starting values
det_hf_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
print ;  print 'Plotting the posteriors for this model run...'; print ;
det_hf_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
print ; print '### Parameter fit summary for this model ###'; print; print;
det_hf_model.print_stats(); #prints a, v, and t
print ; print 'Plotting the posteriors for the fit model'; print ;
[v_diff_node, v_same_node, a_diff_node, a_same_node, t_diff_node, t_same_node] = det_hf_model.nodes_db.node[['v(0.0)','v(1.0)','a(0.0)','a(1.0)','t(0.0)','t(1.0)']]; #get the relevant 'nodes' (posteriors?)
#run through each parameter and plot seperately, saving each
hddm.analyze.plot_posterior_nodes([v_diff_node, v_same_node]);
savefig(savepath+'det_hf_v.png', dpi = 200); #save the figure
hddm.analyze.plot_posterior_nodes([a_diff_node, a_same_node]);
savefig(savepath+'det_hf_a.png', dpi = 200); #save the figure
hddm.analyze.plot_posterior_nodes([t_diff_node, t_same_node]);
savefig(savepath+'det_hf_t.png', dpi = 200); #save the figure
#save the model for use later
#hddm.save(savepath+'dis_nr_all');
# print 'Now for Discrimination task...'; print ;
# 
# 	
# #2.1 Discrimination task
# #2.1.1 load in the data
# dis_hf_data = hddm.load_csv(savepath+'hf_dis_data.csv');
# #2.1.2 flip the errors so that error RTs are 'negative'
# dis_hf_data = hddm.utils.flip_errors(dis_hf_data);
# # #2.1.3 plot the distribution of RTs to see what everything looks like..
# # fig = figure();
# # ax = fig.add_subplot(111, xlabel = 'RT', ylabel = 'Frequency', title = 'Detection Nr Targets RT Distribution for Correct and Error Trials');
# # #loop to histogram each subjects' RT distributions
# # for i,subj in dis_hf_data.groupby('subj_idx'):
# #      subj.rt.hist(bins=20, histtype = 'step', ax = ax);
# 
# #2.1.4 Fit each model independently, allowing each a,t, and v to vary accordingly
# 
# dis_hf_model = hddm.HDDM(dis_hf_data, informative = True, include=('sv', 'st'), depends_on = {'v':'same_hf','a':'same_hf','t':'same_hf'}); #allow each parameter to vary
# dis_hf_model.find_starting_values(); #find realistic, appropriate starting values
# dis_hf_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# dis_hf_model.plot_posteriors(['a','a_std','v','v_std','t','t_std','sv','st']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# dis_hf_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_diff_node, v_same_node, a_diff_node, a_same_node, t_diff_node, t_same_node] = dis_hf_model.nodes_db.node[['v(0.0)','v(1.0)','a(0.0)','a(1.0)','t(0.0)','t(1.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_diff_node, v_same_node]);
# savefig(savepath+'dis_hf_v_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_diff_node, a_same_node]);
# savefig(savepath+'dis_hf_a_includesITV.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_diff_node, t_same_node]);
# savefig(savepath+'dis_hf_t_includesITV.png', dpi = 200); #save the figure
# #save the model for use later
# #hddm.save(savepath+'dis_nr_all');
# print 'Now without ITV parameters...'; print ;
# 
# dis_hf_model = hddm.HDDM(dis_hf_data, informative = True, depends_on = {'v':'same_hf','a':'same_hf','t':'same_hf'}); #allow each parameter to vary
# dis_hf_model.find_starting_values(); #find realistic, appropriate starting values
# dis_hf_model.sample(5000, burn = 25); #sample from the posterior distribution of the model
# print ;  print 'Plotting the posteriors for this model run...'; print ;
# dis_hf_model.plot_posteriors(['a','a_std','v','v_std','t','t_std']);
# print ; print '### Parameter fit summary for this model ###'; print; print;
# dis_hf_model.print_stats(); #prints a, v, and t
# print ; print 'Plotting the posteriors for the fit model'; print ;
# [v_diff_node, v_same_node, a_diff_node, a_same_node, t_diff_node, t_same_node] = dis_hf_model.nodes_db.node[['v(0.0)','v(1.0)','a(0.0)','a(1.0)','t(0.0)','t(1.0)']]; #get the relevant 'nodes' (posteriors?)
# #run through each parameter and plot seperately, saving each
# hddm.analyze.plot_posterior_nodes([v_diff_node, v_same_node]);
# savefig(savepath+'dis_hf_v.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([a_diff_node, a_same_node]);
# savefig(savepath+'dis_hf_a.png', dpi = 200); #save the figure
# hddm.analyze.plot_posterior_nodes([t_diff_node, t_same_node]);
# savefig(savepath+'dis_hf_t.png', dpi = 200); #save the figure
# #save the model for use later
# #hddm.save(savepath+'dis_nr_all');
print 'Done...'; print ;