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

ids = ['jpw','pilot_3']; #use 'agg' for aggregate subject data
block_types = ['Discrim','Detect'];

## Plotting Methods ############################################################################################

def plotNT(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot the number of targets data via a line plot for more asthetic viewing
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Number of Targets',size=25);
	ax1.set_ylim(400,900); ax1.set_xlim([0,3]); ax1.set_xticks([]);  ax1.set_yticks(arange(400,950,50)); xticks([0.4,1.4],['One','Two'],size=20); #ax1.set_yticklabels([200,500,1000],[200,500,1000]); 
	ax2=axes([0.65,0.50,0.25,0.35]); grid(True); ax2.set_xlim([0,3]); ax2.set_xticks([]); ax2.set_ylim(.8,1.0); ax2.set_yticks([0.8,0.85,0.9,0.95,1.0]); xticks([1,2],['One','Two'],size=18);
	ax1.text(1.825,960,'Percent Correct',size=20);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['dodgerblue','red']; #['solid','dashed'];     
	for c,type in zip(colors,block_types):
		ax1.plot([0.4,1.4],[db['%s_%s_st_mean_rt'%(id,type)],db['%s_%s_mt_mean_rt'%(id,type)]],color=c,lw=6.0,ls='solid');
		ax2.plot([1.0,2.0],[db['%s_%s_st_pc'%(id,type)],db['%s_%s_mt_pc'%(id,type)]],color=c,lw=4.0,ls='solid');
		#add errorbars...
		ax1.errorbar(0.4,db['%s_%s_st_mean_rt'%(id,type)],yerr=[[db['%s_%s_st_rt_bs_sems'%(id,type)]],[db['%s_%s_st_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
		ax1.errorbar(1.4,db['%s_%s_mt_mean_rt'%(id,type)],yerr=[[db['%s_%s_mt_rt_bs_sems'%(id,type)]],[db['%s_%s_mt_rt_bs_sems'%(id,type)]]],color='black',lw=3.0);
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
	
def plotDist(block_type,id='agg'):
	#block_type is Discrim or Detect
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot distance effects for multiple target displays
	fig,ax1=subplots(); hold(True); title('Multiple Target Distance \n%s Data for Subject %s'%(block_type,id.upper()),loc='left',size=18);
	ax1.set_ylim(400,900); ax1.set_yticks(arange(400,950,50)); ax1.set_xticks([]); ax1.set_xlim([0,4]); ax1.set_ylabel('Response Time',size=20); ax1.set_xlabel('Distance Between Targets (degrees)',size=20,labelpad=40);
	ax2=axes([0.7,0.6,0.25,0.3]); ax3=axes([0.7,0.1,0.25,0.3]); #create the smaller subplots using Axes call
	ax2.set_xticks([]); ax2.set_xlim([0,4]); ax3.set_xticks([]); ax3.set_xlim([0,4]); ax2.set_ylim(250,800); ax2.set_yticks(arange(250,800,50)); ax3.set_ylim(.8,1.0); ax3.set_yticks([0.8,0.85,0.9,0.95,1.0]);
	ax2.text(3.2,650,'IL',size=16); ax3.text(3.2,0.925,'PC',size=16);
	ex=0.2; w=0.8;
	for name in ['3','5','7']:
		ax1.bar(ex,db['%s_%s_%s_mean_rt'%(id,block_type,name)],color='lightgrey',width=w);
		ax2.bar(ex,db['%s_%s_%s_mean_il'%(id,block_type,name)],color='dodgerblue',width=w);
		ax3.bar(ex,db['%s_%s_%s_pc'%(id,block_type,name)],color='dodgerblue',width=w);
		if id=='agg':
			ax1.errorbar(ex+0.4,db['%s_%s_%s_mean_rt'%(id,block_type,name)],yerr=[[db['%s_%s_%s_rt_bs_sems'%(id,block_type,name)]],[db['%s_%s_%s_rt_bs_sems'%(id,block_type,name)]]],color='black'); #plot bs sem bars
			ax2.errorbar(ex+0.4,db['%s_%s_%s_mean_il'%(id,block_type,name)],yerr=[[db['%s_%s_%s_il_bs_sems'%(id,block_type,name)]],[db['%s_%s_%s_il_bs_sems'%(id,block_type,name)]]],color='black');
			ax3.errorbar(ex+0.4,db['%s_%s_%s_pc'%(id,block_type,name)],yerr=[[db['%s_%s_%s_pc_bs_sems'%(id,block_type,name)]],[db['%s_%s_%s_pc_bs_sems'%(id,block_type,name)]]],color='black');
		else: 
			errors=[db['%s_%s_%s_mean_rt'%(id,block_type,name)]-db['%s_%s_%s_rt_cis'%(id,block_type,name)][0],db['%s_%s_%s_rt_cis'%(id,block_type,name)][1]-db['%s_%s_%s_mean_rt'%(id,block_type,name)]];
			ax1.errorbar(ex+0.4,db['%s_%s_%s_mean_rt'%(id,block_type,name)],yerr=[[errors[0]],[errors[1]]],color='black');
			errors=[db['%s_%s_%s_mean_il'%(id,block_type,name)]-db['%s_%s_%s_il_cis'%(id,block_type,name)][0],db['%s_%s_%s_il_cis'%(id,block_type,name)][1]-db['%s_%s_%s_mean_il'%(id,block_type,name)]];
			ax2.errorbar(ex+0.4,db['%s_%s_%s_mean_il'%(id,block_type,name)],yerr=[[errors[0]],[errors[1]]],color='black');
		ex+=0.8;
	tix=[0.4,1.2,2.0];
	ax1.text(0.4,175,'Three',size=16); ax1.text(1.2,175,'Five',size=16); ax1.text(2.0,175,'Seven',size=16);
	ax2.text(tix[0]+0.1,220,'Three',size=16);ax2.text(tix[1]+0.1,220,'Five',size=16); ax2.text(tix[2]+0.1,220,'Seven',size=16);
	ax3.text(tix[0],0.78,'Three',size=16); ax3.text(tix[1],0.78,'Five',size=16); ax3.text(tix[2],0.78,'Seven',size=16);
		