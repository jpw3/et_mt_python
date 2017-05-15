#Multiple Target (Eyetracking Condition) Plotting code
#Author: James Wilmott, Winter 2016

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib.lines as mlines
import shelve #for database writing and reading

matplotlib.rcParams.update(matplotlib.rcParamsDefault); #restore the default matplotlib styles

datapath = '/Users/james/Documents/MATLAB/data/et_mt_data/'; #'/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #
shelvepath =  '/Users/james/Documents/Python/et_mt/data/'; #'/Users/jameswilmott/Documents/Python/et_mt/data/'; #	

subject_data = shelve.open(shelvepath+'mt_data.db');
individ_subject_data = shelve.open(shelvepath+'individ_mt_data.db');

ids = ['pilot_3','pilot_6','1','2','3','4','5','6','8','9']; #'jpw', use 'agg' for aggregate subject data
block_types = ['Discrim','Detect'];

## Plotting Methods ############################################################################################

def plotAll(id='agg'):
	plotNT(id); print "Plotted number of targets data...";
	plotHF(id); print 'Plotted hemifield data...';
	plotDist(id); print 'Plotted distance data...';
	plotDistXHF(id); print 'Plotted distance by HF data';

def plotIndividHF():
	db = individ_subject_data;
	matplotlib.rcParams['ytick.labelsize']=20; 	matplotlib.rcParams['xtick.labelsize']=20;
	matplotlib.pyplot.rc('font',weight='bold');
	fig,ax1=subplots(); hold(True); grid(True); #title('Experiment 2: Hemifield Difference Plot',size=25);
	ax1.set_ylim(-200,200); ax1.set_xlim(-200,200); ax1.set_yticks(arange(-200,250,50)); ax1.set_xticks(arange(-200,250,50));
	#ax1.set_ylabel('Detection Hemifield RT Difference (RT Different - RT Same)',size=20,labelpad=40); ax1.set_xlabel('Discrimination Hemifield RT Difference (RT Different - RT Same)',size=20,labelpad=40);
	for id in ids:
		detect_diff = db['%s_Detect_diff_hf_mean_rt'%(id)]-db['%s_Detect_same_hf_mean_rt'%(id)];
		discrim_diff = db['%s_Discrim_diff_hf_mean_rt'%(id)]-db['%s_Discrim_same_hf_mean_rt'%(id)];
		ax1.plot(discrim_diff,detect_diff,marker='s',markersize=20);
	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	show();

def plotNT(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot the number of targets data via a line plot for more asthetic viewing
	matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=36;
	matplotlib.pyplot.rc('font',weight='bold');
	fig = figure(figsize = (4,4)); ax1=gca(); #grid(True);
	ax1.set_ylim(350,1000); ax1.set_yticks(arange(350,1050,50)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
	labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
	ax1.set_xticklabels(labels);
	ax1.set_yticklabels(['','','','','','','','','','','','','','']);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['dodgerblue','red']; #['solid','dashed'];
	ex=1;
	for c,type in zip(colors,['st','mt']):
		#note, already converted this to milliseconds in analysis:
		ax1.bar(ex,db['%s_Discrim_%s_mean_rt'%(id,type)],color=c,width=0.4,edgecolor='black');
		ax1.errorbar(ex,db['%s_Discrim_%s_mean_rt'%(id,type)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ax1.bar(ex+1,db['%s_Detect_%s_mean_rt'%(id,type)],color=c,width=0.4,edgecolor='black');
		ax1.errorbar(ex+1,db['%s_Detect_%s_mean_rt'%(id,type)],yerr=[[db['%s_Detect_%s_rt_bs_sems'%(id,type)]],[db['%s_Detect_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ex+=0.4
	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	show();
	
def plotHF(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot the number of targets data via a line plot for more asthetic viewing
	#matplotlib.rcParams['ytick.labelsize']=20;
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Multiple Target Hemifield Relationship Data',size=20);
	ax1.set_ylim(400,900); ax1.set_xlim([0,3]); ax1.set_xticks([]);  ax1.set_yticks(arange(400,950,50)); xticks([0.4,1.4],['Same HF','Diff HF'],size=15); ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemifield Relationship',size=18); 
	ax2=axes([0.65,0.50,0.25,0.35]); grid(True); ax2.set_xlim([0,3]); ax2.set_xticks([]); ax2.set_ylim(.8,1.0); ax2.set_yticks([0.8,0.85,0.9,0.95,1.0]); xticks([1,2],['Same','Diff'],size=18);
	ax1.text(2.2,605,'Percent Correct',size=15);
	#iterate over each block type and plot the same and different multiple target data
	colors=['dodgerblue','red'];
	for c,type in zip(colors,block_types):
		ax1.plot([0.4,1.4],[db['%s_%s_same_hf_mean_rt'%(id,type)],db['%s_%s_diff_hf_mean_rt'%(id,type)]],color=c,lw=6.0,ls='solid');
		ax2.plot([1.0,2.0],[db['%s_%s_same_hf_pc'%(id,type)],db['%s_%s_diff_hf_pc'%(id,type)]],color=c,lw=4.0,ls='solid');
		#add errorbars...
		ax1.errorbar(0.4,db['%s_%s_same_hf_mean_rt'%(id,type)],yerr=[[db['%s_%s_same_rt_bs_sems'%(id,type)]],[db['%s_%s_same_rt_bs_sems'%(id,type)]]],color=c,lw=3.0);
		ax1.errorbar(1.4,db['%s_%s_diff_hf_mean_rt'%(id,type)],yerr=[[db['%s_%s_diff_rt_bs_sems'%(id,type)]],[db['%s_%s_diff_rt_bs_sems'%(id,type)]]],color=c,lw=3.0);
		ax2.errorbar(1.0,db['%s_%s_same_hf_pc'%(id,type)],yerr=[[db['%s_%s_same_hf_pc_bs_sems'%(id,type)]],[db['%s_%s_same_hf_pc_bs_sems'%(id,type)]]],color=c,lw=3.0);
		ax2.errorbar(2.0,db['%s_%s_diff_hf_pc'%(id,type)],yerr=[[db['%s_%s_diff_hf_pc_bs_sems'%(id,type)]],[db['%s_%s_diff_hf_pc_bs_sems'%(id,type)]]],color=c,lw=3.0);
	discrim_line=mlines.Line2D([],[],color='dodgerblue',lw=6,label='Discrimination'); detect_line=mlines.Line2D([],[],color='red',lw=6,label='Detection');
	ax1.legend(handles=[discrim_line,detect_line],bbox_to_anchor=[1.0,0.3],ncol=2); #bbox_to_anchor=[0.97,0.0]
	show();
	
def plotHFBar(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=20;
	matplotlib.rcParams['hatch.linewidth']=4.0;
	matplotlib.pyplot.rc('font',weight='bold');
	fig = figure(figsize = (4,4)); ax1=gca(); #grid(True);
	ax1.set_ylim(350,1000); ax1.set_yticks(arange(350,1050,50)); ax1.set_xlim([0.5,2.8]);  ax1.set_xticks([1.2,2.2]); #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
	labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
	ax1.set_xticklabels(labels);
	ax1.set_yticklabels(['','','','','','','','','','','','','','']);
	colors=['lightsteelblue','dimgray']; styles=['solid','dashed'];
	ex=1;
	for hat,type,c in zip(['',''],['same','diff'],colors):
		ax1.bar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],color=c,hatch=hat,width=0.4,edgecolor='black');
		ax1.errorbar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ax1.bar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],color=c,hatch=hat,width=0.4,edgecolor='black');
		ax1.errorbar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Detect_%s_rt_bs_sems'%(id,type)]],[db['%s_Detect_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ex+=0.4
	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	show();
	
def plotAltHFBar(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=36;
	matplotlib.pyplot.rc('font',weight='bold');
	fig = figure(figsize = (4,4)); ax1=gca(); #grid(True);	
	ax1.set_ylim(300,900); ax1.set_yticks(arange(300,950,50)); ax1.set_xlim([0.5,2.8]); ax1.set_xticks([1.2,2.2]) #ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemispheric Location of Targets',size=18,labelpad=40);		
	labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]='Discrimination'; labels[1]='Detection'; #have to do this to center the x ticks on correct spot without incurring ticks at every spot
	ax1.set_xticklabels(labels);	
	colors=['forestgreen','mediumpurple']; #styles=['solid','dashed'];
	ex=1;
	for c,type in zip(colors,['same','diff']):
		ax1.bar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],color=c,width=0.4);
		ax1.errorbar(ex,db['%s_Discrim_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]],[db['%s_Discrim_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ax1.bar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],color=c,width=0.4);
		ax1.errorbar(ex+1,db['%s_Detect_%s_hf_mean_rt'%(id,type)],yerr=[[db['%s_Detect_%s_rt_bs_sems'%(id,type)]],[db['%s_Detect_%s_rt_bs_sems'%(id,type)]]],color='black',lw=6.0);
		ex+=0.4
	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	show();
	
def plotDist(id='agg'):
	#block_type is Discrim or Detect
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot distance effects for multiple target displays
	matplotlib.rcParams['ytick.labelsize']=20;
	fig,ax1=subplots(); hold(True); grid(True); title('Multiple Target Distance \n Data for Subject %s'%(id.upper()),loc='left',size=22);
	ax1.set_ylim(400,900); ax1.set_yticks(arange(400,950,50)); ax1.set_xticks([]); ax1.set_xlim([0,5]); ax1.set_ylabel('Response Time',size=20); ax1.set_xlabel('Distance Between Targets (degrees)',size=20,labelpad=40);
	ax2=axes([0.7,0.6,0.25,0.3]); grid(True); ax3=axes([0.7,0.1,0.25,0.3]); grid(True); #create the smaller subplots using Axes call
	ax2.set_xticks([]); ax2.set_xlim([0,5]); ax3.set_xticks([]); ax3.set_xlim([0,5]); ax2.set_ylim(200,600); ax2.set_yticks(arange(20,800,50)); ax3.set_ylim(.8,1.0); ax3.set_yticks([0.8,0.85,0.9,0.95,1.0]);
	ax2.text(3.2,650,'IL',size=16); ax3.text(3.2,0.925,'PC',size=16);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['dodgerblue','red'];
	for c,block_type in zip(colors,block_types):
		ax1.plot([0.4,1.4,2.4],[db['%s_%s_3_mean_rt'%(id,block_type)],db['%s_%s_5_mean_rt'%(id,block_type)],db['%s_%s_7_mean_rt'%(id,block_type)]],color=c,lw=6,ls='solid');
		ax2.plot([0.4,1.4,2.4],[db['%s_%s_3_mean_il'%(id,block_type)],db['%s_%s_5_mean_il'%(id,block_type)],db['%s_%s_7_mean_il'%(id,block_type)]],color=c,lw=6,ls='solid');
		ax3.plot([0.4,1.4,2.4],[db['%s_%s_3_pc'%(id,block_type)],db['%s_%s_5_pc'%(id,block_type)],db['%s_%s_7_pc'%(id,block_type)]],color=c,lw=6,ls='solid');
		if id=='agg':
			ax1.errorbar(0.4,db['%s_%s_3_mean_rt'%(id,block_type)],yerr=[[db['%s_%s_3_rt_bs_sems'%(id,block_type)]],[db['%s_%s_3_rt_bs_sems'%(id,block_type)]]],color=c); #plot bs sem bars
			ax1.errorbar(1.4,db['%s_%s_5_mean_rt'%(id,block_type)],yerr=[[db['%s_%s_5_rt_bs_sems'%(id,block_type)]],[db['%s_%s_5_rt_bs_sems'%(id,block_type)]]],color=c); 
			ax1.errorbar(2.4,db['%s_%s_7_mean_rt'%(id,block_type)],yerr=[[db['%s_%s_7_rt_bs_sems'%(id,block_type)]],[db['%s_%s_7_rt_bs_sems'%(id,block_type)]]],color=c); 
			ax2.errorbar(0.4,db['%s_%s_3_mean_il'%(id,block_type)],yerr=[[db['%s_%s_3_il_bs_sems'%(id,block_type)]],[db['%s_%s_3_rt_bs_sems'%(id,block_type)]]],color=c); #plot bs sem bars
			ax2.errorbar(1.4,db['%s_%s_5_mean_il'%(id,block_type)],yerr=[[db['%s_%s_5_il_bs_sems'%(id,block_type)]],[db['%s_%s_5_il_bs_sems'%(id,block_type)]]],color=c); 
			ax2.errorbar(2.4,db['%s_%s_7_mean_il'%(id,block_type)],yerr=[[db['%s_%s_7_il_bs_sems'%(id,block_type)]],[db['%s_%s_7_il_bs_sems'%(id,block_type)]]],color=c);
			ax3.errorbar(0.4,db['%s_%s_3_pc'%(id,block_type)],yerr=[[db['%s_%s_3_pc_bs_sems'%(id,block_type)]],[db['%s_%s_3_pc_bs_sems'%(id,block_type)]]],color=c); #plot bs sem bars
			ax3.errorbar(1.4,db['%s_%s_5_pc'%(id,block_type)],yerr=[[db['%s_%s_5_pc_bs_sems'%(id,block_type)]],[db['%s_%s_5_pc_bs_sems'%(id,block_type)]]],color=c); 
			ax3.errorbar(2.4,db['%s_%s_7_pc'%(id,block_type)],yerr=[[db['%s_%s_7_pc_bs_sems'%(id,block_type)]],[db['%s_%s_7_pc_bs_sems'%(id,block_type)]]],color=c);
	tix=[0.4,1.4,2.4];
	ax1.text(0.4,375,'Three',size=16); ax1.text(1.4,375,'Five',size=16); ax1.text(2.4,375,'Seven',size=16);
	ax2.text(tix[0]+0.1,-20,'Three',size=16);ax2.text(tix[1]+0.1,-20,'Five',size=16); ax2.text(tix[2]+0.1,-20,'Seven',size=16);
	ax3.text(tix[0],0.78,'Three',size=16); ax3.text(tix[1],0.78,'Five',size=16); ax3.text(tix[2],0.78,'Seven',size=16);
	discrim_line=mlines.Line2D([],[],color='dodgerblue',lw=6,label='Discrimination'); detect_line=mlines.Line2D([],[],color='red',lw=6,label='Detection');
	ax1.legend(handles=[discrim_line,detect_line],bbox_to_anchor=[1.05,0.52],ncol=2);
	show();
		
def plotDistXHF(id='agg'):
	#block_type is Discrim or Detect
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	matplotlib.rcParams['ytick.labelsize']=20;
	#plot distance effects for multiple target displays
	fig,ax1=subplots(); hold(True); grid(True); title('Hemifield X Multiple Target Distance \n Data for Subject %s'%(id.upper()),loc='left',size=22);
	ax1.set_ylim(400,900); ax1.set_yticks(arange(400,950,50)); ax1.set_xticks([]); ax1.set_xlim([0,5]); ax1.set_ylabel('Response Time',size=20); ax1.set_xlabel('Distance Between Targets (degrees)',size=20,labelpad=40);
	ax2=axes([0.7,0.6,0.25,0.3]); grid(True); ax3=axes([0.7,0.1,0.25,0.3]); grid(True); #create the smaller subplots using Axes call
	ax2.set_xticks([]); ax2.set_xlim([0,5]); ax3.set_xticks([]); ax3.set_xlim([0,5]); ax2.set_ylim(200,600); ax2.set_yticks(arange(20,800,50)); ax3.set_ylim(.8,1.0); ax3.set_yticks([0.8,0.85,0.9,0.95,1.0]);
	ax2.text(3.2,650,'IL',size=16); ax3.text(3.2,0.925,'PC',size=16);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['dodgerblue','red']; styles=['solid','dashed'];
	for c,block_type in zip(colors,block_types):
		for s,loc in zip(styles,['same','diff']):
			ax1.plot([0.4,1.4,2.4],[db['%s_%s_%s_hf_3_mean_rt'%(id,block_type,loc)],db['%s_%s_%s_hf_5_mean_rt'%(id,block_type,loc)],db['%s_%s_%s_hf_7_mean_rt'%(id,block_type,loc)]],color=c,lw=6,ls=s);
			ax2.plot([0.4,1.4,2.4],[db['%s_%s_%s_hf_3_mean_il'%(id,block_type,loc)],db['%s_%s_%s_hf_5_mean_il'%(id,block_type,loc)],db['%s_%s_%s_hf_7_mean_il'%(id,block_type,loc)]],color=c,lw=6,ls=s);
			ax3.plot([0.4,1.4,2.4],[db['%s_%s_%s_hf_3_pc'%(id,block_type,loc)],db['%s_%s_%s_hf_5_pc'%(id,block_type,loc)],db['%s_%s_%s_hf_7_pc'%(id,block_type,loc)]],color=c,lw=6,ls=s);
			if id=='agg':
				ax1.errorbar(0.4,db['%s_%s_%s_hf_3_mean_rt'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_3_rt_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_3_rt_bs_sems'%(id,block_type,loc)]]],color=c); #plot bs sem bars
				ax1.errorbar(1.4,db['%s_%s_%s_hf_5_mean_rt'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_5_rt_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_5_rt_bs_sems'%(id,block_type,loc)]]],color=c); 
				ax1.errorbar(2.4,db['%s_%s_%s_hf_7_mean_rt'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_7_rt_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_7_rt_bs_sems'%(id,block_type,loc)]]],color=c); 
				ax2.errorbar(0.4,db['%s_%s_%s_hf_3_mean_il'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_3_il_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_3_rt_bs_sems'%(id,block_type,loc)]]],color=c); #plot bs sem bars
				ax2.errorbar(1.4,db['%s_%s_%s_hf_5_mean_il'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_5_il_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_5_il_bs_sems'%(id,block_type,loc)]]],color=c); 
				ax2.errorbar(2.4,db['%s_%s_%s_hf_7_mean_il'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_7_il_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_7_il_bs_sems'%(id,block_type,loc)]]],color=c);
				ax3.errorbar(0.4,db['%s_%s_%s_hf_3_pc'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_3_pc_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_3_pc_bs_sems'%(id,block_type,loc)]]],color=c); #plot bs sem bars
				ax3.errorbar(1.4,db['%s_%s_%s_hf_5_pc'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_5_pc_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_5_pc_bs_sems'%(id,block_type,loc)]]],color=c); 
				ax3.errorbar(2.4,db['%s_%s_%s_hf_7_pc'%(id,block_type,loc)],yerr=[[db['%s_%s_%s_hf_7_pc_bs_sems'%(id,block_type,loc)]],[db['%s_%s_%s_hf_7_pc_bs_sems'%(id,block_type,loc)]]],color=c);
	tix=[0.4,1.4,2.4];
	ax1.text(0.4,375,'Three',size=16); ax1.text(1.4,375,'Five',size=16); ax1.text(2.4,375,'Seven',size=16);
	ax2.text(tix[0]+0.1,-20,'Three',size=16);ax2.text(tix[1]+0.1,-20,'Five',size=16); ax2.text(tix[2]+0.1,-20,'Seven',size=16);
	ax3.text(tix[0],0.78,'Three',size=16); ax3.text(tix[1],0.78,'Five',size=16); ax3.text(tix[2],0.78,'Seven',size=16);
	dis_same_line=mlines.Line2D([],[],color='dodgerblue',lw=6,ls='solid',label='Discrimination, Same HF'); dis_diff_line=mlines.Line2D([],[],color='dodgerblue',lw=6,ls='dashed',label='Discrimination, Diff HF');
	det_same_line=mlines.Line2D([],[],color='red',ls='solid',lw=6,label='Detection, Same HF'); det_diff_line=mlines.Line2D([],[],color='red',lw=6,ls='dashed',label='Detection, Diff HF');
	ax1.legend(handles=[dis_same_line,dis_diff_line,det_same_line,det_diff_line],bbox_to_anchor=[1.1,0.56],ncol=2);
	show();
	
def plotTT(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	#plot distance effects for multiple target displays
	matplotlib.rcParams['ytick.labelsize']=20;
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Target Match by HF\n by Distance for Subject %s'%(id.upper()),loc='left',size=22);
	ax1.set_ylim(400,900); ax1.set_yticks(arange(400,950,50)); ax1.set_xticks([]); ax1.set_xlim([0,5]); ax1.set_ylabel('Response Time',size=20); ax1.set_xlabel('Distance Between Targets (degrees)',size=20,labelpad=40);
	ax2=axes([0.7,0.6,0.25,0.3]); grid(True); ax3=axes([0.7,0.1,0.25,0.3]); grid(True); #create the smaller subplots using Axes call
	ax2.set_xticks([]); ax2.set_xlim([0,5]); ax3.set_xticks([]); ax3.set_xlim([0,5]); ax2.set_ylim(200,600); ax2.set_yticks(arange(20,800,50)); ax3.set_ylim(.8,1.0); ax3.set_yticks([0.8,0.85,0.9,0.95,1.0]);
	ax2.text(3.2,650,'IL',size=16); ax3.text(3.2,0.925,'PC',size=16);
	#iterate over each block type and plot the same and different multiple target data
	colors=['dodgerblue','red']; target_types = ['no_match','yes_match']; styles=['solid','dashed'];
	for c,match in zip(colors,target_types):
		for s,hf_match in zip(styles,['same','diff']):
			ax1.plot([0.4,1.4,2.4],[db['%s_Discrim_%s_%s_hf_3_mean_rt'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_5_mean_rt'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_7_mean_rt'%(id,match,hf_match)]],color=c,lw=6,ls=s); #no third distance db['%s_%s_%s_hf_3_mean_rt'%(id,block_type,loc)]],
			ax2.plot([0.4,1.4,2.4],[db['%s_Discrim_%s_%s_hf_3_mean_il'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_5_mean_il'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_7_mean_il'%(id,match,hf_match)]],color=c,lw=6,ls=s); #no third distance db['%s_%s_%s_hf_3_mean_rt'%(id,block_type,loc)]],
			ax3.plot([0.4,1.4,2.4],[db['%s_Discrim_%s_%s_hf_3_pc'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_5_pc'%(id,match,hf_match)],db['%s_Discrim_%s_%s_hf_7_pc'%(id,match,hf_match)]],color=c,lw=6,ls=s); #no third distance db['%s_%s_%s_hf_3_mean_rt'%(id,block_type,loc)]],
			if id=='agg':
				ax1.errorbar([0.4],db['%s_Discrim_%s_%s_hf_3_mean_rt'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_3_rt_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_3_rt_bs_sems'%(id,match,hf_match)]]],color=c); 
				ax1.errorbar([1.4],db['%s_Discrim_%s_%s_hf_5_mean_rt'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_5_rt_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_5_rt_bs_sems'%(id,match,hf_match)]]],color=c);
				ax1.errorbar([2.4],db['%s_Discrim_%s_%s_hf_7_mean_rt'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_7_rt_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_7_rt_bs_sems'%(id,match,hf_match)]]],color=c);
				ax2.errorbar([0.4],db['%s_Discrim_%s_%s_hf_3_mean_il'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_3_il_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_3_il_bs_sems'%(id,match,hf_match)]]],color=c); 
				ax2.errorbar([1.4],db['%s_Discrim_%s_%s_hf_5_mean_il'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_5_il_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_5_il_bs_sems'%(id,match,hf_match)]]],color=c);
				ax2.errorbar([2.4],db['%s_Discrim_%s_%s_hf_7_mean_il'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_7_il_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_7_il_bs_sems'%(id,match,hf_match)]]],color=c);
				ax3.errorbar([0.4],db['%s_Discrim_%s_%s_hf_3_pc'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_3_pc_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_3_pc_bs_sems'%(id,match,hf_match)]]],color=c); 
				ax3.errorbar([1.4],db['%s_Discrim_%s_%s_hf_5_pc'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_5_pc_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_5_pc_bs_sems'%(id,match,hf_match)]]],color=c);
				ax3.errorbar([2.4],db['%s_Discrim_%s_%s_hf_7_pc'%(id,match,hf_match)],yerr=[[db['%s_Discrim_%s_%s_hf_7_pc_bs_sems'%(id,match,hf_match)]],[db['%s_Discrim_%s_%s_hf_7_pc_bs_sems'%(id,match,hf_match)]]],color=c);
	tix=[0.4,1.4,2.4];
	ax1.text(0.4,375,'Three',size=20); ax1.text(1.4,375,'Five',size=20); ax1.text(2.4,375,'Seven',size=20);
	ax2.text(tix[0]+0.1,-20,'Three',size=16);ax2.text(tix[1]+0.1,-20,'Five',size=16); ax2.text(tix[2]+0.1,-20,'Seven',size=16);
	ax3.text(tix[0],0.78,'Three',size=16); ax3.text(tix[1],0.78,'Five',size=16); ax3.text(tix[2],0.78,'Seven',size=16);
	dis_same_line=mlines.Line2D([],[],color='dodgerblue',lw=6,ls='solid',label='Target Shape Doesn"t Match, Same HF'); dis_diff_line=mlines.Line2D([],[],color='dodgerblue',lw=6,ls='dashed',label='Target Shape Doesn"t Match, Diff HF');
	det_same_line=mlines.Line2D([],[],color='red',ls='solid',lw=6,label='Target Shape Matches, Same HF'); det_diff_line=mlines.Line2D([],[],color='red',lw=6,ls='dashed',label='Target Shape Matches, Diff HF');
	ax1.legend(handles=[dis_same_line,dis_diff_line,det_same_line,det_diff_line],bbox_to_anchor=[1.1,0.56],ncol=2);
	show();
	
def plot_HF_match(id='agg'):
	if id=='agg':
		db=subject_data
	else:
		db=individ_subject_data;
	fig,ax1=subplots(); hold(True); grid(True); title('Experiment 2: Multiple Target Hemifield Relationship Data',size=20);
	ax1.set_ylim(400,900); ax1.set_xlim([0,3]); ax1.set_xticks([]);  ax1.set_yticks(arange(400,950,50)); xticks([0.4,1.4],['Same HF','Diff HF'],size=15); ax1.set_ylabel('Response Time',size=18); ax1.set_xlabel('Hemifield Relationship',size=18); 
	ax2=axes([0.65,0.50,0.25,0.35]); grid(True); ax2.set_xlim([0,3]); ax2.set_xticks([]); ax2.set_ylim(.8,1.0); ax2.set_yticks([0.8,0.85,0.9,0.95,1.0]); xticks([1,2],['Same','Diff'],size=18);
	ax1.text(2.1,650,'Percent Correct',size=15);
	#iterate over each block type and plot the sngle and multiple target data
	colors=['black']; styles=['solid','dashed'];
	for c,type in zip(colors,['Discrim']):
		for s,mat in zip(styles,['match','no_match']):
			ax1.plot([0.4,1.4],[db['%s_%s_same_hf_%s_mean_rt'%(id,type,mat)],db['%s_%s_diff_hf_%s_mean_rt'%(id,type,mat)]],color=c,lw=6.0,ls=s);
			ax2.plot([1.0,2.0],[db['%s_%s_same_hf_%s_pc'%(id,type,mat)],db['%s_%s_diff_hf_%s_pc'%(id,type,mat)]],color=c,lw=4.0,ls=s);
			#add errorbars...
			ax1.errorbar(0.4,db['%s_%s_same_hf_%s_mean_rt'%(id,type,mat)],yerr=[[db['%s_%s_same_%s_rt_bs_sems'%(id,type,mat)]],[db['%s_%s_same_%s_rt_bs_sems'%(id,type,mat)]]],color=c,lw=3.0);
			ax1.errorbar(1.4,db['%s_%s_diff_hf_%s_mean_rt'%(id,type,mat)],yerr=[[db['%s_%s_diff_%s_rt_bs_sems'%(id,type,mat)]],[db['%s_%s_diff_%s_rt_bs_sems'%(id,type,mat)]]],color=c,lw=3.0);
			ax2.errorbar(1.0,db['%s_%s_same_hf_%s_pc'%(id,type,mat)],yerr=[[db['%s_%s_same_hf_%s_pc_bs_sems'%(id,type,mat)]],[db['%s_%s_same_hf_%s_pc_bs_sems'%(id,type,mat)]]],color=c,lw=3.0);
			ax2.errorbar(2.0,db['%s_%s_diff_hf_%s_pc'%(id,type,mat)],yerr=[[db['%s_%s_diff_hf_%s_pc_bs_sems'%(id,type,mat)]],[db['%s_%s_diff_hf_%s_pc_bs_sems'%(id,type,mat)]]],color=c,lw=3.0);
	match_line=mlines.Line2D([],[],color='black',ls='solid',lw=6,label='Shapes Match'); no_match_line=mlines.Line2D([],[],color='black',ls='dashed',lw=6,label="Shapes Don't Match");
	ax1.legend(handles=[match_line,no_match_line],bbox_to_anchor=[1.0,0.3],ncol=1); #[0.97,0.0]
	show();	