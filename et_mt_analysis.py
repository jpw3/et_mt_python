#Multiple Target (Eyetracking Edition) Data Analysis code
#Author: James Wilmott, Winter 2016

#Designed to import et_mt data and analyze it

from pylab import *
import shelve #for database writing and reading
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
from collections import namedtuple
import pyvttbl as pt
pc = lambda x:sum(x)/float(len(x)); #create a percent correct lambda function

datapath = '/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #'/Users/james/Documents/MATLAB/data/et_mt_data/'; #
shelvepath =  '/Users/jameswilmott/Documents/Python/et_mt/data/'; #'/Users/james/Documents/Python/et_mt/data/'; #  

#import the persistent database to save data analysis for future use (plotting)
subject_data = shelve.open(shelvepath+'mt_data');
individ_subject_data = shelve.open(shelvepath+'individ_mt_data');

ids=['pilot_3','pilot_6','1','2','3','4','5','6','8','9']; #'jpw',
block_types=['Detect','Discrim'];

## Data Analysis Methods ####################################################################################################

def getStats(id='agg'):
	if id=='agg':
		blocks=getAllSubjectBlocks();
		#getIndividStats();
	else:
		blocks=[loadAllBlocks(id)]; #return as a list for use in get_Trials function
	trials=getTrials(blocks); #should return a a list of lists, with each inner list containg a subject's trials
	computeNT(trials,id);
	computeHF(trials,id);
	computeDist(trials,id);
	computeDistHF(trials,id);
	#computeTTDist(trials,id);
	compute_HFTargetMatch(trials,id);
	computeTTSimple(trials,id);
	#return trials; #for testing here

def getIndividStats():
	for id in ids:
		getStats(id);
	print "Completed individual subject analysis!";
	
def computeHF(trial_matrix,id):
	#trial_matrix should be a list of trials for each subjects
	#get appropriate database to store data
	if id=='agg':
		db=subject_data;
		score = namedtuple('score',['id','rt','task','hemifield']); #create a named tuple object for use in dataframe   'il','pc',
		hf_df = pt.DataFrame();
		disc_df = pt.DataFrame(); det_df = pt.DataFrame(); #create data frames for use in simple effects ANOVAs
		simp_score = namedtuple('simp_score',['id','rt','hemifield']); #and create a named tuple for this..
		pc_score = namedtuple('score',['id','pc','task','hemifield']); pc_simp_score = namedtuple('score',['id','pc','hemifield']);
		pc_df = pt.DataFrame(); dis_pc_df = pt.DataFrame(); det_pc_df = pt.DataFrame();
	else:
		db=individ_subject_data;
	#loop through each hemifield name and find the mean, median, and such
	trials = [tee for person in trial_matrix for tee in person];
	for type in ['Discrim','Detect']:
		t = [tee for tee in trials if (tee.block_type==type)]; #segment the relevant trials
		t_matrix = [[tee for tee in trs if (tee.block_type==type)] for trs in trial_matrix];
		for hf,name in zip([0,1],['diff','same']):
			#all_rts=[tee.response_time for tee in t if (tee.result==1)&(tee.same_hf==hf)]; all_ils=[tee.initiation_latency for tee in t if (tee.result==1)&(tee.same_hf==hf)];
			res=[tee.result for tee in t if (tee.same_hf==hf)]; #gets the rts, ils, and results for the relevant data
			#agg_rt_sd = std(all_rts); agg_il_sd = std(all_ils);
			#rts=[r for r in all_rts if (r>=(mean(all_rts)-(3*agg_rt_sd)))&(r<=(mean(all_rts)+(3*agg_rt_sd)))];#shave the rts, cutting out outliers above 3 s.d.s...
			#ils=[i for i in all_ils if (i>=(mean(all_ils)-(3*agg_il_sd)))&(i<=(mean(all_ils)+(3*agg_il_sd)))];#shave the ils, cutting out outliers above 3 s.d.s...
			all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.same_hf==hf)] for ts in t_matrix];
			all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.same_hf==hf)] for ts in t_matrix];
			res_matrix = [[tee.result for tee in ts if(tee.same_hf==hf)] for ts in t_matrix];
			ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
			rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
			il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
			rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l];
			if len(rts)==0:
				continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
			#compute and save the data
			db['%s_%s_%s_rt_bs_sems'%(id,type,name)] = compute_BS_SEM(rt_matrix,'time'); db['%s_%s_%s_il_bs_sems'%(id,type,name)] = compute_BS_SEM(il_matrix,'time');
			db['%s_%s_%s_hf_mean_rt'%(id,type,name)]=mean(rts); db['%s_%s_%s_hf_var_rt'%(id,type,name)]=var(rts); db['%s_%s_%s_hf_median_rt'%(id,type,name)]=median(rts); #db['%s_%s_%s_hf_rt_cis'%(id,type,name)]=compute_CIs(rts);
			db['%s_%s_%s_hf_mean_il'%(id,type,name)]=mean(ils); db['%s_%s_%s_hf_var_il'%(id,type,name)]=var(ils); db['%s_%s_%s_hf_median_il'%(id,type,name)]=median(ils); #db['%s_%s_%s_hf_il_cis'%(id,type,name)]=compute_CIs(ils);
			db['%s_%s_%s_hf_pc'%(id,type,name)]=pc(res); db['%s_%s_%s_hf_pc_bs_sems'%(id,type,name)] = compute_BS_SEM(res_matrix,'result');
			if id=='agg':
				#append all the datae for each subject together in the dataframe for use in ANOVA
				for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
					pc_df.insert(pc_score(i,pc(res_scores),type,name)._asdict());
					hf_df.insert(score(i,mean(r_scores),type,name)._asdict()); #,mean(i_scores),pc(res_scores)
					if type=='Discrim': #append the sppropriate scores to the simple effects ANOVAs as well
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						disc_df.insert(simp_score(i,mean(r_scores),name)._asdict());
						dis_pc_df.insert(pc_simp_score(i,p,name)._asdict());
					elif type=='Detect':
						det_df.insert(simp_score(i,mean(r_scores),name)._asdict());
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						det_pc_df.insert(pc_simp_score(i,p,name)._asdict());
	if id=='agg':
		print; print('##################### PRINTING OMNIBUS HEMIFIELD RELATION RT ANOVA RESULTS  #####################');
		print(hf_df.anova('rt',sub='id',wfactors=['task','hemifield']));
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING DISCRIMINATION-TASK SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(disc_df.anova('rt',sub='id',wfactors=['hemifield']));		
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING DETECTION-TASK SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(det_df.anova('rt',sub='id',wfactors=['hemifield']));		
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING OMNIBUS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(pc_df.anova('pc',sub='id',wfactors=['task','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(dis_pc_df.anova('pc',sub='id',wfactors=['hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(det_pc_df.anova('pc',sub='id',wfactors=['hemifield']));
	print "Finished computing hemifield data....";
	
def compute_HFTargetMatch(trial_matrix,id):
	print 'Running hemifield analysis by target shape analysis:'; print;
	if id=='agg':
		db=subject_data;
		score = namedtuple('score',['id','rt','target_match','HF']); #create a named tuple object for use in dataframe   'il','pc',
		hf_df = pt.DataFrame();
		match_df = pt.DataFrame(); no_match_df = pt.DataFrame(); #create data frames for use in simple effects ANOVAs
		simp_score = namedtuple('simp_score',['id','rt','HF']); #and create a named tuple for this..
		pc_score = namedtuple('score',['id','pc','target_match','HF']); pc_simp_score = namedtuple('score',['id','pc','HF']);
		pc_df = pt.DataFrame(); no_match_pc_df = pt.DataFrame(); match_pc_df = pt.DataFrame();
	else:
		db=individ_subject_data;
	#loop through each hemifield name and find the mean, median, and such
	trials = [tee for person in trial_matrix for tee in person];
	for type in ['Discrim']:
		t = [tee for tee in trials if (tee.block_type==type)]; #segment the relevant trials
		t_matrix = [[tee for tee in trs if (tee.block_type==type)] for trs in trial_matrix];
		for hf,name in zip([0,1],['diff','same']):
			for took,mat in zip([0,1],['no_match','match']): #loop through same vs. different 
				res=[tee.result for tee in t if (tee.same_hf==hf)&((tee.target_types[0]==tee.target_types[1])==took)]; #gets the rts, ils, and results for the relevant data 
				all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.same_hf==hf)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
				all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.same_hf==hf)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
				res_matrix = [[tee.result for tee in ts if(tee.same_hf==hf)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
				ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
				rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
				il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
				rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; print 'Number of %s %s trials: %s'%(type,name,len(rts));
				if len(rts)==0:
					continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
				#if it wasn't an empty array, compute and save relevant data
				db['%s_%s_%s_%s_rt_bs_sems'%(id,type,name,mat)] = compute_BS_SEM(rt_matrix,'time'); db['%s_%s_%s_%s_il_bs_sems'%(id,type,name,mat)] = compute_BS_SEM(il_matrix,'time');
				db['%s_%s_%s_hf_%s_mean_rt'%(id,type,name,mat)]=mean(rts); db['%s_%s_%s_hf_%s_var_rt'%(id,type,name,mat)]=var(rts); db['%s_%s_%s_hf_%s_median_rt'%(id,type,name,mat)]=median(rts); db['%s_%s_%s_hf_%s_rt_cis'%(id,type,name,mat)]=compute_CIs(rts);
				db['%s_%s_%s_hf_%s_mean_il'%(id,type,name,mat)]=mean(ils); db['%s_%s_%s_hf_%s_var_il'%(id,type,name,mat)]=var(ils); db['%s_%s_%s_hf_%s_median_il'%(id,type,name,mat)]=median(ils); db['%s_%s_%s_hf_%s_il_cis'%(id,type,name,mat)]=compute_CIs(ils);
				db['%s_%s_%s_hf_%s_pc'%(id,type,name,mat)]=pc(res); db['%s_%s_%s_hf_%s_pc_bs_sems'%(id,type,name,mat)] = compute_BS_SEM(res_matrix,'result');
				if id=='agg':
					#append all the datae for each subject together in the dataframe for use in ANOVA
					for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
						hf_df.insert(score(i,mean(r_scores),mat,name)._asdict()); #,mean(i_scores),pc(res_scores)
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						pc_df.insert(pc_score(i,p,mat,name)._asdict());
						if mat=='match': #append the sppropriate scores to the simple effects ANOVAs as well
							p = pc(res_scores);
							if p==1.0:
								p = p-0.000000000001; #failsafe against the incorrect calculation
							match_pc_df.insert(pc_simp_score(i,p,name)._asdict());
							match_df.insert(simp_score(i,mean(r_scores),name)._asdict());
						elif mat=='no_match':
							p = pc(res_scores);
							if p==1.0:
								p = p-0.000000000001; #failsafe against the incorrect calculation
							no_match_pc_df.insert(pc_simp_score(i,p,name)._asdict());
							no_match_df.insert(simp_score(i,mean(r_scores),name)._asdict());
	if id=='agg':
		print; print('##################### PRINTING TARGETS MATCH OR NOT HEMIFIELD RELATION OMNIBUS RT ANOVA RESULTS  #####################');		
		print(hf_df.anova('rt',sub='id',wfactors=['target_match','HF']));
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING TARGET MATCH HEMIFIELD RELATION SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(match_df.anova('rt',sub='id',wfactors=['HF']));		
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING TARGET DOESN"T MATCH HEMIFIELD RELATION SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(no_match_df.anova('rt',sub='id',wfactors=['HF']));		
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING OMNIBUS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(pc_df.anova('pc',sub='id',wfactors=['target_match','HF']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING TARGET MATCH SIMPLE EFFECTS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(match_pc_df.anova('pc',sub='id',wfactors=['HF']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING TARGET DOESN"T MATCH SIMPLE EFFECTS HEMIFIELD RELATION PC ANOVA REESULTS ##############################'; print ;
		print(no_match_pc_df.anova('pc',sub='id',wfactors=['HF']));
	print "Finished computing target's match by hemifield relation data...";


def computeTTSimple(trial_matrix, id='agg'):
	print 'Running hemifield analysis by target shape analysis for the simple effect of yes match vs. no match:'; print;
	if id=='agg':
		db=subject_data;
		score = namedtuple('score',['id','rt','target_match']); #create a named tuple object for use in dataframe   'il','pc',
		df = pt.DataFrame();
		pc_df = pt.DataFrame();
		pc_score = namedtuple('score',['id','pc','target_match']);
	else:
		db=individ_subject_data;
	#loop through each hemifield name and find the mean, median, and such
	trials = [tee for person in trial_matrix for tee in person];
	for type in ['Discrim']:
		t = [tee for tee in trials if (tee.block_type==type)]; #segment the relevant trials
		t_matrix = [[tee for tee in trs if (tee.block_type==type)] for trs in trial_matrix];
		for took,mat in zip([0,1],['no_match','match']): #loop through same vs. different 		
			res=[tee.result for tee in t if (tee.nr_targets==2)&((tee.target_types[0]==tee.target_types[1])==took)]; #gets the rts, ils, and results for the relevant data 
			all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.nr_targets==2)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
			all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.nr_targets==2)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
			res_matrix = [[tee.result for tee in ts if(tee.nr_targets==2)&((tee.target_types[0]==tee.target_types[1])==took)] for ts in t_matrix];
			ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
			rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
			il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
			rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; print 'Number of %s trials: %s'%(mat,len(rts));
			if len(rts)==0:
				continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
			#if it wasn't an empty array, compute and save relevant data
			db['%s_%s_%s_rt_bs_sems'%(id,type,mat)] = compute_BS_SEM(rt_matrix,'time'); db['%s_%s_%s_il_bs_sems'%(id,type,mat)] = compute_BS_SEM(il_matrix,'time');
			db['%s_%s_%s_mean_rt'%(id,type,mat)]=mean(rts); db['%s_%s_%s_var_rt'%(id,type,mat)]=var(rts); db['%s_%s_%s_median_rt'%(id,type,mat)]=median(rts); db['%s_%s_%s_rt_cis'%(id,type,mat)]=compute_CIs(rts);
			db['%s_%s_%s_mean_il'%(id,type,mat)]=mean(ils); db['%s_%s_%s_var_il'%(id,type,mat)]=var(ils); db['%s_%s_%s_median_il'%(id,type,mat)]=median(ils); db['%s_%s_%s_il_cis'%(id,type,mat)]=compute_CIs(ils);
			db['%s_%s_%s_pc'%(id,type,mat)]=pc(res); db['%s_%s_%s_pc_bs_sems'%(id,type,mat)] = compute_BS_SEM(res_matrix,'result');
			if id=='agg':
				#append all the datae for each subject together in the dataframe for use in ANOVA
				for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
					df.insert(score(i,mean(r_scores),mat)._asdict()); #,mean(i_scores),pc(res_scores)
					p = pc(res_scores);
					if p==1.0:
						p = p-0.000000000001; #failsafe against the incorrect calculation
					pc_df.insert(pc_score(i,p,mat)._asdict());
	if id=='agg':
		print; print('##################### PRINTING TARGETS MATCH ONLY RT ANOVA RESULTS  #####################');		
		print(df.anova('rt',sub='id',wfactors=['target_match']));
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING TARGETS MATCH ONLY PC ANOVA RESULTS  #####################');		
		print(pc_df.anova('pc',sub='id',wfactors=['target_match']));
		raw_input("Press ENTER to continue...");	
	print "Finished computing targets match simple data...";
	

def computeNT(trial_matrix, id):
	#trial_matrix should be a list of trials for each subjects
	#get appropriate database to store data
	if id=='agg':
		db=subject_data;
		score = namedtuple('score',['id','rt','task','nr_targets']); #create a named tuple object for use in dataframe   'il','pc',
		nt_df = pt.DataFrame();
		disc_df = pt.DataFrame(); det_df = pt.DataFrame(); #create data frames for use in simple effects ANOVAs
		simp_score = namedtuple('simp_score',['id','rt','nr_targets']); #and create a named tuple for this..
		pc_score = namedtuple('score',['id','pc','task','nr_targets']); pc_simp_score = namedtuple('score',['id','pc','nr_targets']);
		pc_df = pt.DataFrame(); dis_pc_df = pt.DataFrame(); det_pc_df = pt.DataFrame();
	else:
		db=individ_subject_data;
	trials = [tee for person in trial_matrix for tee in person]; #get all the trials across all subjects together to perform data analysis on
	for type in ['Discrim','Detect']:
		t = [tee for tee in trials if (tee.block_type==type)]; #segment the relevant trials
		t_matrix = [[tee for tee in trs if (tee.block_type==type)] for trs in trial_matrix]; #list of subject trials; for use in SEM calculation
		#loop through the possible number of targets, calculating RT and pc stats as I go
		for n,name in zip([1,2,0],['st','mt','abs']):
			if ((type=='Discrim')&(n==0)): #impossible condition
				continue;
			#gets the rts, ils, and results for the relevant data
			all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.nr_targets==n)] for ts in t_matrix];
			all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.nr_targets==n)] for ts in t_matrix];
			res_matrix = [[tee.result for tee in ts if(tee.nr_targets==n)] for ts in t_matrix];
			ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
			#trim matrixed rts of outliers greater than 3 s.d.s from the mean
			rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; 
			il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
			rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; res=[io for lo in res_matrix for io in lo]; 
			#compute and save the relevant data
			db['%s_%s_%s_rt_bs_sems'%(id,type,name)] = compute_BS_SEM(rt_matrix,'time'); db['%s_%s_%s_il_bs_sems'%(id,type,name)] = compute_BS_SEM(il_matrix,'time');
			db['%s_%s_%s_mean_rt'%(id,type,name)]=mean(rts); db['%s_%s_%s_var_rt'%(id,type,name)]=var(rts); db['%s_%s_%s_median_rt'%(id,type,name)]=median(rts); #db['%s_%s_%s_rt_cis'%(id,type,name)]=compute_CIs(rts); 
			db['%s_%s_%s_mean_il'%(id,type,name)]=mean(ils); db['%s_%s_%s_var_il'%(id,type,name)]=var(ils); db['%s_%s_%s_median_il'%(id,type,name)]=median(ils); #db['%s_%s_%s_il_cis'%(id,type,name)]=compute_CIs(ils); 
			db['%s_%s_%s_pc'%(id,type,name)]=pc(res); db['%s_%s_%s_pc_bs_sems'%(id,type,name)] = compute_BS_SEM(res_matrix,'result');
			if id=='agg':
				#append all the datae for each subject together in the dataframe for use in ANOVA
				for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
					if type=='Discrim': #append the sppropriate scores to the simple effects ANOVAs as well
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						disc_df.insert(simp_score(i,mean(r_scores),n)._asdict());
						dis_pc_df.insert(pc_simp_score(i,p,n)._asdict());
					elif type=='Detect':
						det_df.insert(simp_score(i,mean(r_scores),n)._asdict());
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						det_pc_df.insert(pc_simp_score(i,p,n)._asdict());
					if n==0: #cut out 0 scores because there is no target absent in discrimination
						continue;
					nt_df.insert(score(i,mean(r_scores),type,n)._asdict()); #,mean(i_scores),pc(res_scores)
					pc_df.insert(pc_score(i,pc(res_scores),type,n)._asdict());

	if id=='agg':
		print; print('##################### PRINTING OMNIBUS NR TARGETS ANOVA RESULTS  #####################');
		print(nt_df.anova('rt',sub='id',wfactors=['task','nr_targets']));		
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING DISCRIMINATION-TASK NR TARGETS SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(disc_df.anova('rt',sub='id',wfactors=['nr_targets']));		
		raw_input("Press ENTER to continue...");
		print; print('##################### PRINTING DETECTION-TASK NR TARGETS SIMPLE EFFECTS ANOVA RESULTS  #####################');
		print(det_df.anova('rt',sub='id',wfactors=['nr_targets']));		
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING OMNIBUS NR TARGETS PC ANOVA REESULTS ##############################'; print ;
		print(pc_df.anova('pc',sub='id',wfactors=['task','nr_targets']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS NR TARGETS PC ANOVA REESULTS ##############################'; print ;
		print(dis_pc_df.anova('pc',sub='id',wfactors=['nr_targets']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS NR TARGETS PC ANOVA REESULTS ##############################'; print ;
		print(det_pc_df.anova('pc',sub='id',wfactors=['nr_targets']));
	print 'Finished computing number of target data...'

def computeDist(trial_matrix, id):
	if id=='agg':
		score = namedtuple('score',['id','rt','task','distance']); #create a named tuple object for use in dataframe
		simp_score = namedtuple('score',['id','rt','distance']);
		df = pt.DataFrame(); dis_df = pt.DataFrame(); det_df = pt.DataFrame();
		pc_score = namedtuple('score',['id','pc','task','distance']); simp_pc_score = namedtuple('score',['id','pc','distance']);
		pc_df = pt.DataFrame(); dis_pc_df = pt.DataFrame(); det_pc_df = pt.DataFrame(); 
	#get appropriate database to store data
	if id=='agg':
		db=subject_data;
	else:
		db=individ_subject_data;
	trials = [tee for person in trial_matrix for tee in person];
	#cycle through each type of task
	for type in ['Discrim','Detect']:
		t = [tee for tee in trials if ((tee.block_type==type)&(tee.nr_targets==2))]; #segment the relevant trials
		t_matrix = [[tee for tee in trs if ((tee.block_type==type)&(tee.nr_targets==2))] for trs in trial_matrix];
		#cycle throught the different distances
		for nombre,dist in zip(['3','5','7'],[3,5,7]):
			all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.t_dist==dist)] for ts in t_matrix]; #collect the rts
			all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.t_dist==dist)] for ts in t_matrix];
			res_matrix = [[tee.result for tee in ts if(tee.t_dist==dist)] for ts in t_matrix];
			ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
			rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
			il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
			rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; res = [re for ye in res_matrix for re in ye];
			if len(rts)==0:
				print "%s %s %s skipping because rts is len %s"%(type,dist,name,len(rts))
				continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
			#find the means, variances, etc. for each dependant measure and then append it to the appropriate dataframe object
			db['%s_%s_dist_%s_rt_bs_sems'%(id,type,nombre)]=compute_BS_SEM(rt_matrix,'time'); db['%s_%s_dist_%s_il_bs_sems'%(id,type,nombre)]=compute_BS_SEM(il_matrix,'time');
			db['%s_%s_dist_%s_mean_rt'%(id,type,nombre)]=mean(rts); db['%s_%s_dist_%s_var_rt'%(id,type,nombre)]=var(rts); db['%s_%s_dist_%s_median_rt'%(id,type,nombre)]=median(rts); 
			db['%s_%s_dist_%s_mean_il'%(id,type,nombre)]=mean(ils); db['%s_%s_dist_%s_var_il'%(id,type,nombre)]=var(ils); db['%s_%s_dist_%s_median_il'%(id,type,nombre)]=median(ils); 
			db['%s_%s_dist_%s_pc'%(id,type,nombre)]=pc(res); db['%s_%s_dist_%s_pc_bs_sems'%(id,type,nombre)] = compute_BS_SEM(res_matrix,'result');
			if id=='agg':	
				#append all the datae for each subject together in the dataframe for use in ANOVA
				for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
					df.insert(score(i,mean(r_scores),type,dist)._asdict());
					pc_df.insert(pc_score(i,pc(res_scores),type,dist)._asdict());
					#append data to the simple-effects DataFrames
					if type=='Discrim':
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						dis_df.insert(simp_score(i,mean(r_scores),dist)._asdict());
						dis_pc_df.insert(simp_pc_score(i,p,dist)._asdict());
					elif type=='Detect':
						p = pc(res_scores);
						if p==1.0:
							p = p-0.000000000001; #failsafe against the incorrect calculation
						det_df.insert(simp_score(i,mean(r_scores),dist)._asdict());
						det_pc_df.insert(simp_pc_score(i,p,dist)._asdict());
	
	#print the ANOVA tables
	if id=='agg':
		print ; print '##################### PRINTING OMNIBUS DISTANCE RT ANOVA REESULTS ##############################'; print ;
		print(df.anova('rt',sub='id',wfactors=['task','distance']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS DISTANCE RT ANOVA REESULTS ##############################'; print ;
		print(dis_df.anova('rt',sub='id',wfactors=['distance']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS DISTANCE RT ANOVA REESULTS ##############################'; print ;
		print(det_df.anova('rt',sub='id',wfactors=['distance']));
		print ; print '##################### PRINTING OMNIBUS DISTANCE PC ANOVA REESULTS ##############################'; print ;
		print(pc_df.anova('pc',sub='id',wfactors=['task','distance']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS DISTANCE PC ANOVA REESULTS ##############################'; print ;
		print(dis_pc_df.anova('pc',sub='id',wfactors=['distance']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS DISTANCE PC ANOVA REESULTS ##############################'; print ;
		print(det_pc_df.anova('pc',sub='id',wfactors=['distance']));
	print "Finished computing distance data...";

		
def computeDistHF(trial_matrix, id):
	if id=='agg':
		score = namedtuple('score',['id','rt','task','distance','hemifield']); #create a named tuple object for use in dataframe   'il','pc',
		simp_score = namedtuple('score',['id','rt','distance','hemifield']);
		hf_df = pt.DataFrame();
		dis_df = pt.DataFrame(); det_df = pt.DataFrame();
		pc_score = namedtuple('score',['id','pc','task','distance','hemifield']); simp_pc_score = namedtuple('score',['id','pc','distance','hemifield']);
		pc_df = pt.DataFrame(); dis_pc_df = pt.DataFrame(); det_pc_df = pt.DataFrame(); 
	#get appropriate database to store data
	if id=='agg':
		db=subject_data;
	else:
		db=individ_subject_data;
	trials = [tee for person in trial_matrix for tee in person];
	#cycle through each type of task
	for type in ['Discrim','Detect']:
		#cycle throught the different distances
		for nombre,dist in zip(['3','5','7'],[3,5,7]):
			t = [tee for tee in trials if ((tee.block_type==type)&(tee.nr_targets==2))]; #segment the relevant trials
			t_matrix = [[tee for tee in trs if ((tee.block_type==type)&(tee.nr_targets==2))] for trs in trial_matrix];
			#loop through the same and different HFs to get those individual measurements of the distnce effects
			for hf,name in zip([0,1],['diff','same']):
				 #gets the rts, ils, and results for the relevant data
				all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&(tee.same_hf==hf)&(tee.t_dist==dist)] for ts in t_matrix];
				all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&(tee.same_hf==hf)&(tee.t_dist==dist)] for ts in t_matrix];
				res_matrix = [[tee.result for tee in ts if(tee.same_hf==hf)&(tee.t_dist==dist)] for ts in t_matrix];
				ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
				rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
				il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
				rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; res=[ir for lr in res_matrix for ir in lr];
				if len(rts)==0:
					print "%s %s %s skipping because rts is len %s"%(type,dist,name,len(rts))
					continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
				db['%s_%s_%s_hf_dist_%s_rt_bs_sems'%(id,type,name,nombre)]=compute_BS_SEM(rt_matrix,'time'); db['%s_%s_%s_hf_dist_%s_il_bs_sems'%(id,type,name,nombre)]=compute_BS_SEM(il_matrix,'time');
				db['%s_%s_%s_hf_dist_%s_mean_rt'%(id,type,name,nombre)]=mean(rts); db['%s_%s_%s_hf_dist_%s_var_rt'%(id,type,name,nombre)]=var(rts); db['%s_%s_%s_hf_dist_%s_median_rt'%(id,type,name,nombre)]=median(rts); 
				db['%s_%s_%s_hf_dist_%s_mean_il'%(id,type,name,nombre)]=mean(ils); db['%s_%s_%s_hf_dist_%s_var_il'%(id,type,name,nombre)]=var(ils); db['%s_%s_%s_hf_dist_%s_median_il'%(id,type,name,nombre)]=median(ils); 
				db['%s_%s_%s_hf_dist_%s_pc'%(id,type,name,nombre)]=pc(res); db['%s_%s_%s_hf_dist_%s_pc_bs_sems'%(id,type,name,nombre)] = compute_BS_SEM(res_matrix,'result');
				if id=='agg':	
					#append all the datae for each subject together in the dataframe for use in ANOVA
					for i,r_scores,i_scores,res_scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix,il_matrix,res_matrix):
						hf_df.insert(score(i,mean(r_scores),type,dist,name)._asdict()); #,mean(i_scores),pc(res_scores)
						pc_df.insert(pc_score(i,pc(res_scores),type,dist,name)._asdict());
						if type=='Discrim':
							p = pc(res_scores);
							if p==1.0:
								p = p-0.000000000001; #failsafe against the incorrect calculation
							dis_df.insert(simp_score(i,mean(r_scores),dist,name)._asdict());
							dis_pc_df.insert(simp_pc_score(i,p,dist,name)._asdict());
						elif type=='Detect':
							p = pc(res_scores);
							if p==1.0:
								p = p-0.000000000001; #failsafe against the incorrect calculation
							det_df.insert(simp_score(i,mean(r_scores),dist,name)._asdict());
							det_pc_df.insert(simp_pc_score(i,p,dist,name)._asdict());
	if id=='agg':
		print ; print '##################### PRINTING OMNIBUS DISTANCE BY HEMIFIELD RT ANOVA REESULTS ##############################'; print ;
		print(hf_df.anova('rt',sub='id',wfactors=['task','distance','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS DISTANCE BY HEMIFIELD RT ANOVA REESULTS ##############################'; print ;
		print(dis_df.anova('rt',sub='id',wfactors=['distance','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS DISTANCE BY HEMIFIELD RT ANOVA REESULTS ##############################'; print ;
		print(det_df.anova('rt',sub='id',wfactors=['distance','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING OMNIBUS DISTANCE BY HEMIFIELD PC ANOVA REESULTS ##############################'; print ;
		print(pc_df.anova('pc',sub='id',wfactors=['task','distance','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DISCRIMINATION SIMPLE EFFECTS DISTANCE BY HEMIFIELD PC ANOVA REESULTS ##############################'; print ;
		print(dis_pc_df.anova('pc',sub='id',wfactors=['distance','hemifield']));
		raw_input("Press ENTER to continue...");
		print ; print '##################### PRINTING DETECTION SIMPLE EFFECTS DISTANCE BY HEMIFIELD PC ANOVA REESULTS ##############################'; print ;
		print(det_pc_df.anova('pc',sub='id',wfactors=['distance','hemifield']));		
	print "Finished computing distance by hemifield relation data...";
		
# def computeTTDist(trial_matrix,id):
# 	print "Started the function...";
# 	#function to compute the RT difference between same and different target types wth diatnce factored in for discrimination tasks
# 	if id=='agg':
# 		db=subject_data;
# 		score = namedtuple('score',['id','rt','targets_match','hemifield_match','distance']); #create a named tuple object for use in dataframe   'il','pc',
# 		df = pt.DataFrame();
# 	else:
# 		db=individ_subject_data;
# 	#loop through for each discrimination task condition with two targets checking if the target types are the same
# 	trials = [tee for person in trial_matrix for tee in person];	
# 	t = [tee for tee in trials if (tee.block_type=='Discrim')&(tee.nr_targets==2)]; #segment the relevant trials
# 	t_matrix = [[tee for tee in trs if (tee.block_type=='Discrim')&(tee.nr_targets==2)] for trs in trial_matrix];
# 	for match,m in zip(['yes_match','no_match'],[1,0]): #cycle through whether the targets match or not
# 		struct = [[[[] for i in range(3)] for p in range(3)] for j in range(2)];
# 		individ_struct = [[[[[] for k in range(len(ids))] for i in range(3)] for p in range(3)] for j in range(2)];
# 		for hf_match,hf in zip(['diff','same'],[0,1]): #go through same or different hf
# 			en=0;
# 			for dist,n in zip(['3','5','7'],[3,5,7]): #go through the distances  ,'d3' ,3
# 				#partition the respective statistics
# 				all_rt_matrix = [[tee.response_time for tee in ts if(tee.result==1)&((tee.target_types[0]==tee.target_types[1])==m)&(tee.same_hf==hf)&(tee.t_dist==n)] for ts in t_matrix];
# 				all_il_matrix = [[tee.initiation_latency for tee in ts if(tee.result==1)&((tee.target_types[0]==tee.target_types[1])==m)&(tee.same_hf==hf)&(tee.t_dist==n)] for ts in t_matrix];
# 				res_matrix = [[tee.result for tee in ts if((tee.target_types[0]==tee.target_types[1])==m)&(tee.same_hf==hf)&(tee.t_dist==n)] for ts in t_matrix];				
# 				ind_rt_sds=[std(are) for are in all_rt_matrix]; ind_il_sds=[std(eye) for eye in all_il_matrix]; #get individual rt sds and il sds to 'shave' the rts of extreme outliers
# 				rt_matrix=[[r for r in individ_rts if (r>=(mean(individ_rts)-(3*ind_rt_sd)))&(r<=(mean(individ_rts)+(3*ind_rt_sd)))] for individ_rts,ind_rt_sd in zip(all_rt_matrix,ind_rt_sds)]; #trim matrixed rts of outliers greater than 3 s.d.s from the mean
# 				il_matrix=[[i for i in individ_ils if (i>=(mean(individ_ils)-(3*ind_il_sd)))&(i<=(mean(individ_ils)+(3*ind_il_sd)))] for individ_ils,ind_il_sd in zip(all_il_matrix,ind_il_sds)];
# 				rts = [r for y in rt_matrix for r in y]; ils = [i for l in il_matrix for i in l]; res=[s for v in res_matrix for s in v]; #collect the aggregate rt, ils, and pc
# 				if len(rts)==0:
# 					1/0
# 					continue; #skip computing and saving data if there was no data that matched the criteria (so the array is empty)
# 				#save the data into th structure as needed. use hf and n variables to do so, respectively
# 				[struct[hf][en-1][0].append(o) for o in rts]; [struct[hf][en-1][1].append(z) for z in ils]; [struct[hf][en-1][2].append(em) for em in res];
# 				[individ_struct[hf][en-1][0][y].append(e) for y,u in enumerate(rt_matrix) for e in u]; [individ_struct[hf][en-1][1][y].append(e) for y,u in enumerate(il_matrix) for e in u]; [individ_struct[hf][en-1][2][y].append(e) for y,u in enumerate(res_matrix) for e in u];
# 				db['%s_Discrim_%s_%s_hf_%s_rt_bs_sems'%(id,match,hf_match,dist)]=compute_BS_SEM(rt_matrix,'time'); db['%s_Discrim_%s_%s_hf_%s_il_bs_sems'%(id,match,hf_match,dist)]=compute_BS_SEM(il_matrix,'time');
# 				db['%s_Discrim_%s_%s_hf_%s_mean_rt'%(id,match,hf_match,dist)]=mean(rts); db['%s_Discrim_%s_%s_hf_%s_var_rt'%(id,match,hf_match,dist)]=var(rts); db['%s_Discrim_%s_%s_hf_%s_median_rt'%(id,match,hf_match,dist)]=median(rts); db['%s_Discrim_%s_%s_hf_%s_rt_cis'%(id,match,hf_match,dist)]=compute_CIs(rts);
# 				db['%s_Discrim_%s_%s_hf_%s_mean_il'%(id,match,hf_match,dist)]=mean(ils); db['%s_Discrim_%s_%s_hf_%s_var_il'%(id,match,hf_match,dist)]=var(ils); db['%s_Discrim_%s_%s_hf_%s_median_il'%(id,match,hf_match,dist)]=median(ils); db['%s_Discrim_%s_%s_hf_%s_il_cis'%(id,match,hf_match,dist)]=compute_CIs(ils);
# 				db['%s_Discrim_%s_%s_hf_%s_pc'%(id,match,hf_match,dist)]=pc(res); db['%s_Discrim_%s_%s_hf_%s_pc_bs_sems'%(id,match,hf_match,dist)]=compute_BS_SEM(res_matrix,'result');
# 				print "Saved %s %s %s %s data to database..."%(id,match,hf_match,dist);
# 				#append rts to the dataframe
# 				if id=='agg':
# 					for i,scores in zip(linspace(1,len(rt_matrix),len(rt_matrix)),rt_matrix):
# 						df.insert(score(i,mean(scores),match,hf_match,n)._asdict());
# 				en+=1;
# 	if id=='agg':		
# 		print(df.anova('rt',sub='id',wfactors=['targets_match','hemifield_match','distance']));
# 		raw_input("Press ENTER to continue...");
# 	print "Finished ctarget type data...";


def compute_BS_SEM(data_matrix, type):
    #calculate the between-subjects standard error of the mean. data_matrix should be matrix of trials including each subject
    #should only pass data matrix into this function after segmenting into relevant conditions
	agg_data = [datum for person in data_matrix for datum in person]; #get all the data together
	n = len(data_matrix);
	if type=='time':
		grand_mean = mean(agg_data);
		matrix = [[dee for dee in datas] for datas in data_matrix]
		err = [mean(d) for d in matrix if (len(d)>0)]-grand_mean;
		squared_err = err**2;
		MSE = sum(squared_err)/(n-1);
	elif type=='result':
		grand_pc = pc(agg_data);
		matrix = [[dee for dee in datas] for datas in data_matrix]
		err = [pc(d) for d in matrix if (len(d)>0)]-grand_pc;
		squared_err = err**2;
		MSE = sum(squared_err)/(n-1);
	denom = sqrt(n);
	standard_error_estimate=sqrt(MSE)/float(denom);
	return standard_error_estimate;

def compute_CIs(data, func=mean, interval=95):
    #data should be a list or array, func can be a lambda function (e.g. percent correct)
    percentiles = [(0+(100-interval)/2.0),(100-(100-interval)/2.0)]; #get the percentiles for use in getting CIs
    n = len(data);
    epochs = 1000; #run through the bootstrapping procedure this many times
    sample_stats = zeros(epochs);# to hold samples
    for i in range(epochs):
        sample = choice(data,size=n,replace=True); #randomly sample from distribution
        sample_stats[i] = func(sample);
    cis = array([percentile(sample_stats,percentiles[0]),percentile(sample_stats,percentiles[1])]);
    #print "Finished computing CIs..."
    return cis;

## Importing Methods #############################################################################################################

#define a function to import individual .mat data files
def loadBlock(subid,block_type,block_nr):
	#returns a single Block object corresponding to the block number and subject id
	#block type should be a string corresponding to the task type(e.g. 'Discrim')
	filename = glob(datapath+'%s'%subid+'/'+'*_%s_%s_%d.mat'%(block_type,subid,block_nr)); #Not sure if this regex will work here, must check
	matdata = loadmat(filename[0],struct_as_record=False,squeeze_me=True)['block']; #use scipy loadmat() to load in the files
	block=Block(matdata); #here, create Block object with dictionary of trial data in matdata
	return block;

#define a function to import all .mat data files for a given subject
def loadAllBlocks(subid):
    filenames = glob(datapath+'%s'%subid+'/'+'*_%s_[1-9].mat'%subid); #got to check that this regex works here
    blocks = []; #empty list to hold loaded blocks
    for filename in filenames:
        matdata=loadmat(filename,struct_as_record=False,squeeze_me=True)['block'];
        block=Block(matdata);
        blocks.append(block);
    return blocks #return the loaded blocks as a list for later purposes..

#define functions to get subject specific blocks and aggregate blocks together for analysis, respectively
def getAllSubjectBlocks():
    blocks = [[] for i in range(len(ids))]; #create a list of empty lists to append the individual blocks to
    for i,sub_id in enumerate(ids):
        blocks[i] = loadAllBlocks(sub_id);
        #print "Imported data for subject %s\n"%sub_id;
    #print "Done getting all subject blocks..\n";
    return blocks;

def getTrials(all_blocks):
    #do some processing of trials...
	foo = [processTrials(b) for blocks in all_blocks for b in blocks]; #foo is a dummy variable; I'm performing all the operations on all_blocks list
    #then segment the trials all together
	trial_matrix = [[t for b in blocks for t in b.trials] for blocks in all_blocks];
	print "Done getting trials together..\n"
	return trial_matrix; #trial matrix will be a n by m, n is the number of trials for a subject and m is the number of subjects

def processTrials(b):
	#dimensions of b: list by number of subjects by number of trials
	#go through each trial and add fields as necessary
	for i,t in enumerate(b.trials):
	#code which hemifield the target was in
		#target absent 
		if (t.nr_targets==0):
			t.target_hf1='none';
			t.target_hf2='none';
			t.hf_match=-1;
		#one target
		elif (t.nr_targets==1):
			if (t.target_coors[0]>0):	 
				t.target_hf1='right'; 
			else:
				t.target_hf1='left';
			t.hf_match = -1; #code for single targets is -1
			t.target_hf2='none';
		#multiple targets
		elif (t.nr_targets==2):
			if (t.target_coors[0,0]>0):	 
				t.target_hf1='right'; 
			else:
				t.target_hf1='left';
			#code whether the hemifield of second target matched
			if (t.target_coors[1,0]>0): 
				t.target_hf2='right';
				if t.target_hf1=='right':
					t.hf_match=1;
				else:
					t.hf_match=0;
			else:
				t.target_hf2='left';
				if t.target_hf1=='left':
					t.hf_match=1;
				else:
					t.hf_match=0;
		#get the target hemifields together for easier processing in HF bias function
		t.hf_locs = [t.target_hf1,t.target_hf2];


## Data Structures ###############################################################################################################

#define a Block object that will hold the Trials for each block along with relevant data (e.g. date)
class Block(object):
	#object being passed into this class should be a scipy mat_structure of data from the block
	def __init__(self, matStructure=None):
		self.block_nr= matStructure.block_nr;
		self.date = str(matStructure.date);
		self.sub_id = str(matStructure.sub_id);
		self.block_type = str(matStructure.type);
		self.nr_invalids = matStructure.nr_invalids;
		self.sp = matStructure.sp;
		self.dp = matStructure.dp;
		if self.block_type=='Discrim':
			self.trials = [discrimTrial(trialData,self.block_type,self.sub_id) for trialData in  matStructure.trial_data];
		elif self.block_type=='Detect':
			self.trials = [detectTrial(trialData,self.block_type,self.sub_id) for trialData in  matStructure.trial_data];

#define a Trial object that will hold the individual trial data for discrimination tasks
class discrimTrial(object):
	#object being passed into this Trial instance should be a dictionary corresponding to the trial data for this given trial
	def __init__(self, trialData, block_type, sub_id):
		self.sub_id = sub_id;
		self.block_type = block_type;
		self.trial_type = trialData.trial_type; #determines the colors, distances, nr of targets
		self.nr_targets = trialData.nr_targets;
		self.t_dist = trialData.t_dist;
		self.same_hf = trialData.same_HF;
		self.nr_distractors = trialData.nr_distractors;
		self.target_col = str(trialData.target_col); #red or green
		self.dist_col = str(trialData.dist_col); #red or green
		self.target_types = trialData.t_types;
		self.target_dist = [trialData.target_distances]; #absolute distances from the origin
		self.distr_dist = [trialData.distractor_distances];
		self.target_coors = trialData.target_coors;
		self.dist_coors = trialData.dist_coors;
		self.trial_times = trialData.trial_times;
		self.initiation_latency = trialData.trial_times.initiation_latency*1000;
		self.response_time = self.trial_times.response_time*1000; #put every time into seconds
		self.movement_time = self.response_time-self.initiation_latency;
		self.reponse = str(trialData.response); #letter corresponding to presented
		self.result = trialData.result; #right or wrong, 1 or 0
		self.selected_type = trialData.selected_type; #precense or absence
		self.abort = trialData.abort_trial;
 
 #define a Trial object to hold information for a Detection trial       
class detectTrial(object):
	#object being passed into this Trial instance should be a dictionary corresponding to the trial data for this given trial
	def __init__(self, trialData, block_type, sub_id):
		self.sub_id = sub_id;
		self.block_type = block_type;
		self.trial_type = trialData.trial_type; #determines the colors, distances, nr of targets
		self.nr_targets = trialData.nr_targets;
		self.t_dist = trialData.t_dist;
		self.target_present = trialData.target_present;
		self.same_hf = trialData.same_HF;
		self.nr_targets = trialData.nr_targets;
		self.nr_distractors = trialData.nr_distractors;
		self.target_col = str(trialData.target_col); #red or green
		self.dist_col = str(trialData.dist_col); #red or green
		self.target_dist = [trialData.target_distances]; #absolute distances from the origin
		self.distr_dist = [trialData.distractor_distances];
		self.target_coors = trialData.target_coors;
		self.dist_coors = trialData.dist_coors;
		self.trial_times = trialData.trial_times;
		self.initiation_latency = trialData.trial_times.initiation_latency*1000;
		self.response_time = self.trial_times.response_time*1000; #time into seconds
		self.movement_time = self.response_time-self.initiation_latency;
		self.reponse = str(trialData.response); #letter corresponding to presented
		self.result = trialData.result; #right or wrong, 1 or 0
		self.selected_type = trialData.selected_type; #precense or absence
		self.abort = trialData.abort_trial;
