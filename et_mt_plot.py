#Multiple Target (Eyetracking Condition) Plotting code
#Author: James Wilmott, Winter 2016

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import shelve #for database writing and reading

matplotlib.rcParams.update(matplotlib.rcParamsDefault); #restore the default matplotlib styles

datapath = '/Users/james/Documents/MATLAB/data/et_mt_data/'; #'/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #
shelvepath =  '/Users/james/Documents/Python/et_mt/data/'; #'/Users/jameswilmott/Documents/Python/et_mt/data/'; #

subject_data = shelve.open(shelvepath+'mt_data.db');
individ_subject_data = shelve.open(shelvepath+'individ_mt_data.db');

ids = ['jpw']; #use 'agg' for aggregate subject data
block_types = ['Discrim','Detect'];

## Plotting Methods ############################################################################################

def plotNT(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot the number of targets data via a line plot for more asthetic viewing
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Number of Targets',size=25);
	ax1.set_ylim(400,900); ax1.set_xlim([0.04,0.11]); ax1.set_xticks([]);  ax1.set_yticks(arange(400,950,50)); xticks([0.05,0.1],['One','Two'],size=20); #ax1.set_yticklabels([200,500,1000],[200,500,1000]); 
	ax2=axes([0.65,0.50,0.25,0.35]); grid(True); ax2.set_xlim([0,3]); ax2.set_xticks([]); ax2.set_ylim(.8,1.0); ax2.set_yticks([0.8,0.85,0.9,0.95,1.0]); xticks([1,2],['One','Two'],size=18);
	ax1.text(1.825,960,'Percent Correct',size=20);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['dodgerblue','red']; #['solid','dashed'];     
	for c,type in zip(colors,block_types):
		ax1.plot([0.05,0.1],[db['%s_%s_st_mean_rt'%(id,type)],db['%s_%s_mt_mean_rt'%(id,type)]],color=c,lw=6.0,ls='solid');
		ax2.plot([1.0,2.0],[db['%s_%s_st_pc'%(id,type)],db['%s_%s_mt_pc'%(id,type)]],color=c,lw=4.0,ls='solid');
		#add errorbars...
		ax1.errorbar(0.05,db['%s_%s_st_mean_rt'%(id,type)],yerr=[[db['%s_%s_st_rt_bs_sems'%(id,type)]],[db['%s_%s_st_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax1.errorbar(0.1,db['%s_%s_mt_mean_rt'%(id,type)],yerr=[[db['%s_%s_mt_rt_bs_sems'%(id,type)]],[db['%s_%s_mt_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax2.errorbar(1.0,db['%s_%s_st_pc'%(id,type)],yerr=[[db['%s_%s_st_pc_bs_sems'%(id,type)]],[db['%s_%s_st_pc_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax2.errorbar(2.0,db['%s_%s_mt_pc'%(id,type)],yerr=[[db['%s_%s_mt_pc_bs_sems'%(id,type)]],[db['%s_%s_mt_pc_bs_sems'%(id,type)]]],color='black',lw=3.0);
		blue_p=patches.Patch(color='dodgerblue',label='Discrimination'); red_p=patches.Patch(color='red',label='Detection');
		ax1.legend(bbox_to_anchor=[0.97,0.0],ncol=2);
	show();
	
def plotHF(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot the number of targets data via a line plot for more asthetic viewing
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Multiple Target Hemifield Relationship Data',size=22);
	ax1.set_ylim(400,900); ax1.set_xlim([0,3]); ax1.set_xticks([]);  ax1.set_yticks(arange(400,950,50)); xticks([0.4,1.4],['Same HF','Different HF'],size=20); 
	ax2=axes([0.65,0.50,0.25,0.35]); grid(True); ax2.set_xlim([0,3]); ax2.set_xticks([]); ax2.set_ylim(.8,1.0); ax2.set_yticks([0.8,0.85,0.9,0.95,1.0]); xticks([1,2],['Same HF','Different HF'],size=18);
	ax1.text(1.825,960,'Percent Correct',size=20);
	#iterate over each block type and plot the sngle and multiple target data
	styles=['solid','dashed'];     #['dodgerblue','red'];
	for s,type in zip(styles,block_types):
		ax1.plot([0.4,1.4],[db['%s_%s_same_hf_mean_rt'%(id,type)],db['%s_%s_diff_hf_mean_rt'%(id,type)]],color='black',lw=6.0,ls=s);
		ax2.plot([1.0,2.0],[db['%s_%s_same_hf_pc'%(id,type)],db['%s_%s_diff_hf_pc'%(id,type)]],color='black',lw=4.0,ls=s);
		#add errorbars...
		ax1.errorbar(0.4,db['%s_%s_same_hf_mean_rt'%(id,type)],yerr=[[db['%s_%s_same_rt_bs_sems'%(id,type)]],[db['%s_%s_same_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax1.errorbar(1.4,db['%s_%s_diff_hf_mean_rt'%(id,type)],yerr=[[db['%s_%s_diff_rt_bs_sems'%(id,type)]],[db['%s_%s_diff_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax2.errorbar(1.0,db['%s_%s_same_hf_pc'%(id,type)],yerr=[[db['%s_%s_same_hf_pc_bs_sems'%(id,type)]],[db['%s_%s_same_hf_pc_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax2.errorbar(2.0,db['%s_%s_diff_hf_pc'%(id,type)],yerr=[[db['%s_%s_diff_hf_pc_bs_sems'%(id,type)]],[db['%s_%s_diff_hf_pc_bs_sems'%(id,type)]]],color='black',lw=3.0);
	#blue_p=patches.Patch(color='dodgerblue',label='Discrimination'); red_p=patches.Patch(color='red',label='Detection');
	ax1.legend(bbox_to_anchor=[0.97,0.0],ncol=2);
	show();
	
		
		