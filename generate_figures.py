#This code is designed to generate plots that can be used for presentation and manuscript creation for Experiment 2

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib.lines as mlines
import shelve #for database writing and reading

#screen dimensions for the office ocmputer = (19.2,10.44)

shelvepath =  '/Users/james/Documents/Python/et_mt/data/'; #'/Users/jameswilmott/Documents/Python/et_mt/data/'; #	
savepath = '/Users/james/Documents/Python/et_mt/figures/' #'/Users/jameswilmott/Documents/Python/et_mt/figures/'; #

subject_data = shelve.open(shelvepath+'mt_data.db');
db = subject_data; id = 'agg';

## Create the plots and save them ####
#Note, all plots are means of aggregate data
#set parameters for plots
matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=30;
matplotlib.rcParams['xtick.major.width']=2.0; matplotlib.rcParams['ytick.major.width']=2.0;
matplotlib.rcParams['xtick.major.size']=10.0; matplotlib.rcParams['ytick.major.size']=10.0; #increase the length of the ticks
matplotlib.rcParams['hatch.linewidth'] = 9.0; #set the hatch width to larger than the default case
matplotlib.rcParams['hatch.color'] = 'black';
matplotlib.pyplot.rc('font',weight='bold');

# # 0.0 number of targets data
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
# ax1.set_xticklabels(['Discrimination','Detection']);
# colors=['limegreen','mediumpurple']; ex=1;
# for c,type in zip(colors,['st','mt']):
#     #note, already converted this to milliseconds in analysis:
#     ax1.bar(ex,db['%s_Discrim_%s_mean_rt'%(id,type)],color=c,width=0.4);  #,edgecolor='black'
#     ax1.errorbar(ex,db['%s_Discrim_%s_mean_rt'%(id,type)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ax1.bar(ex+1,db['%s_Detect_%s_mean_rt'%(id,type)],color=c,width=0.4); #,edgecolor='black'
#     ax1.errorbar(ex+1,db['%s_Detect_%s_mean_rt'%(id,type)],yerr=[[db['%s_Detect_%s_rt_bs_sems'%(id,type)]],[db['%s_Detect_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ex+=0.4
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_nt_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_nt';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
#


#detection task first
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]);
#ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Number of Targets',size=18,labelpad=40);
ax1.set_xticklabels(['Zero','One','Two']);
colors=['darkgrey','steelblue','mediumpurple']; 
#detection task first
ax1.bar(1,db['%s_Detect_abs_mean_rt'%(id)],color=colors[0],width=0.4);
ax1.errorbar(1,db['%s_Detect_abs_mean_rt'%(id)],yerr=[[db['%s_Detect_abs_rt_bs_sems'%(id)]],[db['%s_Detect_abs_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(1.6,db['%s_Detect_st_mean_rt'%(id)],color=colors[1],width=0.4);
ax1.errorbar(1.6,db['%s_Detect_st_mean_rt'%(id)],yerr=[[db['%s_Detect_st_rt_bs_sems'%(id)]],[db['%s_Detect_st_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.2,db['%s_Detect_mt_mean_rt'%(id)],color=colors[2],width=0.4);
ax1.errorbar(2.2,db['%s_Detect_mt_mean_rt'%(id)],yerr=[[db['%s_Detect_mt_rt_bs_sems'%(id)]],[db['%s_Detect_mt_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#save the labeled figure as a .png	
filename = 'exp2_detection_nt_labeled';
savefig(savepath+filename+'.png',dpi=400);
#then get rid of labels and save as a .eps
labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);
filename = 'exp2_detection_nt';
savefig(savepath+filename+'.eps',dpi=400);
show();

# #discrimination plot
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100));  ax1.set_xlim([0.7,3.1]); ax1.set_xticks([1,1.6,2.2,2.8]);
#ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Number of Targets',size=18,labelpad=40);
ax1.set_xticklabels(['One','Two','Target Shapes Match', 'Target Shapes Mismatch']);
colors=['steelblue','mediumpurple','indigo','orchid']; 
#do one target, two targets, and then target shapes match vs. not match
ax1.bar(1,db['%s_Discrim_st_mean_rt'%(id)],color=colors[0],width=0.4);
ax1.errorbar(1,db['%s_Discrim_st_mean_rt'%(id)],yerr=[[db['%s_Discrim_st_rt_bs_sems'%(id)]],[db['%s_Discrim_st_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(1.6,db['%s_Discrim_mt_mean_rt'%(id)],color=colors[1],width=0.4);
ax1.errorbar(1.6,db['%s_Discrim_mt_mean_rt'%(id)],yerr=[[db['%s_Discrim_mt_rt_bs_sems'%(id)]],[db['%s_Discrim_mt_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.2,db['%s_Discrim_match_mean_rt'%(id)],color=colors[2],width=0.4);
ax1.errorbar(2.2,db['%s_Discrim_match_mean_rt'%(id)],yerr=[[db['%s_Discrim_match_rt_bs_sems'%(id)]],[db['%s_Discrim_match_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.8,db['%s_Discrim_no_match_mean_rt'%(id)],color=colors[3],width=0.4);
ax1.errorbar(2.8,db['%s_Discrim_no_match_mean_rt'%(id)],yerr=[[db['%s_Discrim_no_match_rt_bs_sems'%(id)]],[db['%s_Discrim_no_match_rt_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#save the labeled figure as a .png	
filename = 'exp2_discrimination_nt_labeled';
savefig(savepath+filename+'.png',dpi=400);
#then get rid of labels and save as a .eps
labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);
filename = 'exp2_discrimination_nt';
savefig(savepath+filename+'.eps',dpi=400);
show();


######### Accuracy for number of targets data

#detection task
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(0.75,1.00); ax1.set_yticks(arange(0.8,1.01,0.05)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]);
#ax1.set_ylabel('Proportion Correct',size=18); ax1.set_xlabel('Number of Targets',size=18,labelpad=40);
ax1.set_xticklabels(['Zero','One','Two']);
colors=['darkgrey','steelblue','mediumpurple']; 
ax1.bar(1,db['%s_Detect_abs_pc'%(id)],color=colors[0],width=0.4);
ax1.errorbar(1,db['%s_Detect_abs_pc'%(id)],yerr=[[db['%s_Detect_abs_pc_bs_sems'%(id)]],[db['%s_Detect_abs_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(1.6,db['%s_Detect_st_pc'%(id)],color=colors[1],width=0.4);
ax1.errorbar(1.6,db['%s_Detect_st_pc'%(id)],yerr=[[db['%s_Detect_st_pc_bs_sems'%(id)]],[db['%s_Detect_st_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.2,db['%s_Detect_mt_pc'%(id)],color=colors[2],width=0.4);
ax1.errorbar(2.2,db['%s_Detect_mt_pc'%(id)],yerr=[[db['%s_Detect_mt_pc_bs_sems'%(id)]],[db['%s_Detect_mt_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#save the labeled figure as a .png	
filename = 'exp2_detection_nt_PC_labeled';
savefig(savepath+filename+'.png',dpi=400);
#then get rid of labels and save as a .eps
labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);
filename = 'exp2_detection_nt_PC';
savefig(savepath+filename+'.eps',dpi=400);
show();


#discrimination task
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(0.75,1.00); ax1.set_yticks(arange(0.8,1.01,0.05)); ax1.set_xlim([0.7,3.1]); ax1.set_xticks([1,1.6,2.2,2.8]);
#ax1.set_ylabel('Proportion Correct',size=18); ax1.set_xlabel('Number of Targets',size=18,labelpad=40);
ax1.set_xticklabels(['One','Two','Target Shapes Match', 'Target Shapes Mismatch']);
colors=['steelblue','mediumpurple','indigo','orchid']; 
#do one target, two targets, and then target shapes match vs. not match
ax1.bar(1,db['%s_Discrim_st_pc'%(id)],color=colors[0],width=0.4);
ax1.errorbar(1,db['%s_Discrim_st_pc'%(id)],yerr=[[db['%s_Discrim_st_pc_bs_sems'%(id)]],[db['%s_Discrim_st_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(1.6,db['%s_Discrim_mt_pc'%(id)],color=colors[1],width=0.4);
ax1.errorbar(1.6,db['%s_Discrim_mt_pc'%(id)],yerr=[[db['%s_Discrim_mt_pc_bs_sems'%(id)]],[db['%s_Discrim_mt_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.2,db['%s_Discrim_match_pc'%(id)],color=colors[2],width=0.4);
ax1.errorbar(2.2,db['%s_Discrim_match_pc'%(id)],yerr=[[db['%s_Discrim_match_pc_bs_sems'%(id)]],[db['%s_Discrim_match_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.bar(2.8,db['%s_Discrim_no_match_pc'%(id)],color=colors[3],width=0.4);
ax1.errorbar(2.8,db['%s_Discrim_no_match_pc'%(id)],yerr=[[db['%s_Discrim_no_match_pc_bs_sems'%(id)]],[db['%s_Discrim_no_match_pc_bs_sems'%(id)]]],color='black',lw=6.0);
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#save the labeled figure as a .png	
filename = 'exp2_discrimination_nt_PC_labeled';
savefig(savepath+filename+'.png',dpi=400);
#then get rid of labels and save as a .eps
labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);
filename = 'exp2_discrimination_nt_PC';
savefig(savepath+filename+'.eps',dpi=400);
show();

# ##############################################################################################################################
# 
# # 1.0 Hemifield Relation stuff
# #start with same vs. different HF plot
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
# ax1.set_xticklabels(['Discrimination','Detection']);
# colors=['dodgerblue','darkorange']; 
# ex=1;
# for hat,type,c in zip(['',''],['same','diff'],colors):
#     ax1.bar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],color=c,hatch=hat,width=0.4); #,edgecolor='black'
#     ax1.errorbar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ax1.bar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],color=c,hatch=hat,width=0.4); #,edgecolor='black'
#     ax1.errorbar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Detect_%s_rt_bs_sems'%(id,type)]],[db['%s_Detect_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ex+=0.4
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_hf_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_hf';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# #proportion correct for HF
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.75,1.000); ax1.set_yticks(arange(0.75,1.01,0.05)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
# ax1.set_xticklabels(['Discrimination','Detection']);
# colors=['dodgerblue','darkorange'];  ex=1;
# for hat,type,c in zip(['',''],['same','diff'],colors):
#     #note, already converted this to milliseconds in analysis:
#     ax1.bar(ex,db['%s_Discrim_%s_hf_pc'%(id,type)],color=c,width=0.4); #,edgecolor='black'
#     ax1.errorbar(ex,db['%s_Discrim_%s_hf_pc'%(id,type)],yerr=[[db['%s_Discrim_%s_hf_pc_bs_sems'%(id,type)]],[db['%s_Discrim_%s_hf_pc_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ax1.bar(ex+1,db['%s_Detect_%s_hf_pc'%(id,type)],color=c,width=0.4); #,edgecolor='black'
#     ax1.errorbar(ex+1,db['%s_Detect_%s_hf_pc'%(id,type)],yerr=[[db['%s_Detect_%s_hf_pc_bs_sems'%(id,type)]],[db['%s_Detect_%s_hf_pc_bs_sems'%(id,type)]]],color='black',lw=6.0);
#     ex+=0.4
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_hf_pc_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_hf_pc';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# ##############################################################################################################################
# 
# #simple effect of distance- for discrimination and detection tasks
# #reaction time first!
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,3.8]);  ax1.set_xticks([1.2,2.2,3.2]);
# ax1.set_xticklabels(['3','5','7']);
# for type,style,mark in zip(['Discrim','Detect'],['solid','dotted'],['o','o']):
# 	ax1.plot(array([1.2,2.2,3.2]),array([db['%s_%s_dist_3_mean_rt'%(id,type)],db['%s_%s_dist_5_mean_rt'%(id,type)],db['%s_%s_dist_7_mean_rt'%(id,type)]]), marker = mark, color = 'black',ls = style, lw = 8, markersize = 14);
# 	#plotting the errorbars separately to prevent the line being drawn that overshaows the line drawn in the above plotting commands
# 	ax1.errorbar(1.2,db['%s_%s_dist_3_mean_rt'%(id,type)], yerr = [[db['%s_%s_dist_3_rt_bs_sems'%(id,type)]],[db['%s_%s_dist_3_rt_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);
# 	ax1.errorbar(2.2,db['%s_%s_dist_5_mean_rt'%(id,type)], yerr = [[db['%s_%s_dist_5_rt_bs_sems'%(id,type)]],[db['%s_%s_dist_5_rt_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);				 
# 	ax1.errorbar(3.2,db['%s_%s_dist_7_mean_rt'%(id,type)], yerr = [[db['%s_%s_dist_7_rt_bs_sems'%(id,type)]],[db['%s_%s_dist_7_rt_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_distance_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_distance';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# #then the percent correct
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.75,1.02); ax1.set_yticks(arange(0.75,1.01,0.05)); ax1.set_xlim([0.5,3.8]);  ax1.set_xticks([1.2,2.2,3.2]);
# ax1.set_xticklabels(['3','5','7']);
# for type,style,mark in zip(['Discrim','Detect'],['solid','dotted'],['o','o']):
# 	ax1.plot(array([1.2,2.2,3.2]),array([db['%s_%s_dist_3_pc'%(id,type)],db['%s_%s_dist_5_pc'%(id,type)],db['%s_%s_dist_7_pc'%(id,type)]]), marker = mark, color = 'black',ls = style, lw = 8, markersize = 14);
# 	#plotting the errorbars separately to prevent the line being drawn that overshaows the line drawn in the above plotting commands
# 	ax1.errorbar(1.2,db['%s_%s_dist_3_pc'%(id,type)], yerr = [[db['%s_%s_dist_3_pc_bs_sems'%(id,type)]],[db['%s_%s_dist_3_pc_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);
# 	ax1.errorbar(2.2,db['%s_%s_dist_5_pc'%(id,type)], yerr = [[db['%s_%s_dist_5_pc_bs_sems'%(id,type)]],[db['%s_%s_dist_5_pc_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);				 
# 	ax1.errorbar(3.2,db['%s_%s_dist_7_pc'%(id,type)], yerr = [[db['%s_%s_dist_7_pc_bs_sems'%(id,type)]],[db['%s_%s_dist_7_pc_bs_sems'%(id,type)]]], color = 'black',lw = 6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_distance_pc_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_distance_pc';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 
# ##############################################################################################################################

# #DIstance by hemifield relation for discrimination then detection task. Want to separate them into two separate bar graphs
# #reaction time first!
# #loop through for each type and then create a bar plot
# for type in ['Discrim','Detect']:
#     colors=['dodgerblue','darkorange'];
#     fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
#     ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,3.8]);  ax1.set_xticks([1.2,2.2,3.2]);
#     ax1.set_xticklabels(['3','5','7']);
#     for dist,ex in zip([3,5,7],[1.0,2.0,3.0]):
#         add = 0;
#         for hf, c in zip(['same','diff'], colors):
#             ax1.bar(ex+add, db['%s_%s_%s_hf_dist_%s_mean_rt'%(id,type,hf,dist)], color = c, width = 0.4);
#             #plotting the errorbars separately to prevent the line being drawn that overshaows the line drawn in the above plotting commands
#             ax1.errorbar(ex+add,db['%s_%s_%s_hf_dist_%s_mean_rt'%(id,type,hf,dist)], yerr = [[db['%s_%s_%s_hf_dist_%s_rt_bs_sems'%(id,type,hf,dist)]],[db['%s_%s_%s_hf_dist_%s_rt_bs_sems'%(id,type,hf,dist)]]], color = 'black',lw = 6.0);
#             add+=0.4;
#     ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
#     ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
#     ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#     #save the labeled figure as a .png	
#     filename = 'exp2_%s_distance_hf_labeled'%type; show();
#     savefig(savepath+filename+'.png',dpi=400);
#     #then get rid of labels and save as a .eps
#     labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
#     ax1.set_xticklabels(labels);
#     ax1.set_yticklabels(['','','','','','','','','','','','','','']);
#     filename = 'exp2_%s_distance_hf'%type;
#     savefig(savepath+filename+'.eps',dpi=400);
#     show();
# 
# #then the percent correct
# for type in ['Discrim','Detect']:
#     colors=['dodgerblue','darkorange'];
#     fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
#     ax1.set_ylim(0.75,1.0); ax1.set_yticks(arange(0.75,1.03,0.05));
#     ax1.set_xlim([0.5,3.8]);  ax1.set_xticks([1.2,2.2,3.2]);
#     ax1.set_xticklabels(['3','5','7']);
#     for dist,ex in zip([3,5,7],[1.0,2.0,3.0]):
#         add = 0;
#         for hf, c in zip(['same','diff'], colors):
#             ax1.bar(ex+add, db['%s_%s_%s_hf_dist_%s_pc'%(id,type,hf,dist)], color = c, width = 0.4);
#             #plotting the errorbars separately to prevent the line being drawn that overshaows the line drawn in the above plotting commands
#             ax1.errorbar(ex+add,db['%s_%s_%s_hf_dist_%s_pc'%(id,type,hf,dist)], yerr = [[db['%s_%s_%s_hf_dist_%s_pc_bs_sems'%(id,type,hf,dist)]],[db['%s_%s_%s_hf_dist_%s_pc_bs_sems'%(id,type,hf,dist)]]], color = 'black',lw = 6.0);
#             add+=0.4;
#     ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
#     ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
#     ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#     #save the labeled figure as a .png	
#     filename = 'exp2_%s_distance_hf_pc_labeled'%type; show();
#     savefig(savepath+filename+'.png',dpi=400);
#     #then get rid of labels and save as a .eps
#     labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
#     ax1.set_xticklabels(labels);
#     ax1.set_yticklabels(['','','','','','','','','','','','','','']);
#     filename = 'exp2_%s_distance_hf_pc'%type;
#     savefig(savepath+filename+'.eps',dpi=400);
#     show();


# ##############################################################################################################################
# 
# # target shapes match vs. don't match for discrimination trials
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,2.6]);  ax1.set_xticks([1.0,2.0]);
# #ax1.set_xticklabels(['Different Shape','Same Shape']);
# width=0.4; ex = 1.0;
# for targ_match,c in zip(['no_match','match'],['lightsteelblue','dimgrey']):
#         ax1.bar(ex,db['%s_Discrim_%s_mean_rt'%(id,targ_match)],color=c,width=width); 
#         ax1.errorbar(ex,db['%s_Discrim_%s_mean_rt'%(id,targ_match)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,targ_match)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,targ_match)]]],color='black',lw=6.0);
#         ex+=1.0;
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# #save the labeled figure as a .png	
# filename = 'exp2_tt_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_tt';
# savefig(savepath+filename+'.eps',dpi=400);
# show();    
# 
# ##############################################################################################################################
# 
# 
# # same vs. different by target shape match for discrimination trials
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(350,800); ax1.set_yticks(arange(400,850,100)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]);
# #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
# ax1.set_xticklabels(['Different Shape','Same Shape']);
# width=0.4; add=0;
# for h,targ_match in zip(['',''],['no_match','match']):
#     ex=1;
#     for c,hf_match in zip(['dodgerblue','darkorange'],['same','diff']):	
#         ax1.bar(ex+add,db['%s_Discrim_%s_hf_%s_mean_rt'%(id,hf_match,targ_match)],color=c,hatch=h,width=width); #,edgecolor='black'
#         ax1.errorbar(ex+add,db['%s_Discrim_%s_hf_%s_mean_rt'%(id,hf_match,targ_match)],yerr=[[db['%s_Discrim_%s_%s_rt_bs_sems'%(id,hf_match,targ_match)]],[db['%s_Discrim_%s_%s_rt_bs_sems'%(id,hf_match,targ_match)]]],color='black',lw=6.0);
#         ex+=0.4;
#         if hf_match=='diff':
#             add=1;
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_tt_hf_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_tt_hf';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# #proportion correct for HF by target types..
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.75,1.000); ax1.set_yticks(arange(0.75,1.01,0.05)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
# ax1.set_xticklabels(['Different Shape','Same Shape']);  
# width=0.4; add=0;
# for h,targ_match in zip(['',''],['no_match','match']):  #['/','x']
#     ex=1;
#     for c,hf_match in zip(['dodgerblue','darkorange'],['same','diff']):	
#         ax1.bar(ex+add,db['%s_Discrim_%s_hf_%s_pc'%(id,hf_match,targ_match)],color=c,hatch=h,width=width); #,edgecolor='black'
#         ax1.errorbar(ex+add,db['%s_Discrim_%s_hf_%s_pc'%(id,hf_match,targ_match)],yerr=[[db['%s_Discrim_%s_hf_%s_pc_bs_sems'%(id,hf_match,targ_match)]],[db['%s_Discrim_%s_hf_%s_pc_bs_sems'%(id,hf_match,targ_match)]]],color='black',lw=6.0);
#         ex+=0.4;
#         if hf_match=='diff':
#             add=1;
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = 'exp2_tt_hf_pc_labeled'; show();
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# filename = 'exp2_tt_hf_pc';
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 
# # #figure HF legend for reference
# # fig = figure(figsize = (12.8,7.64)); ax1=gca();
# # oneline=mlines.Line2D([],[],color='dodgerblue',lw=6,label='Same HF'); twoline=mlines.Line2D([],[],color='darkorange',lw=6,label='Diff HF');
# # ax1.legend(handles=[oneline,twoline],loc = 10,ncol=2,fontsize = 22);
# # #save the labeled figure as a .png	
# # filename = 'exp2_hf_legend';
# # savefig(savepath+filename+'.png',dpi=400);