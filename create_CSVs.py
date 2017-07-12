#Designed to create the .csv files needed for the HDDM package to fit a hierarchical DDM
#This script is designed to be run before using the HDDMfit.py script that fits the individual contrast DDMs

#########################################################################################################################################################################

#import relevant packages and specify where the data is (datapath) and where I'll save the .csv too (savepath)
from pylab import *
from scipy.io import loadmat #used to load .mat files in as dictionaries
import pandas as pd
from glob import glob #for use in searching for/ finding data files

datapath = '/Users/james/Documents/MATLAB/data/et_mt_data/'; #
savepath = '/Users/james/Documents/Python/et_mt/data/'; #

ids=['pilot_3','pilot_6','1','2','3','4','5','6','8','9']; #'jpw',

## Loading data methods 

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
		
		
## Data Structures 

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

#######################################################################################################################################################################


#0. load in all the data for all subjects.
blocks=getAllSubjectBlocks(); #use this local function to import all the MATLAB data, saving them as local Block objects with individual Trial object instances as well
trials = getTrials(blocks);

#1. loop through the list of trials, appending them to a Pandas DataFrame() object if it was a correct (1) or incorrect (0) trial
#do this for three different DataFrames: an aggregate one, then a 1 vs. 2 targets only and a same vs. different HF only
#specify the distinct DataFrames, passing the relevant tuples with column name strings for each
#do it seperately for discrimination and detection tasks, respectively
#ALL csvs must contain 'subj_idx', 'rt', and 'response' columns at minimum
agg_data = pd.DataFrame(columns=('subj_idx','rt','response','nr_targets','same_hf','task_type'));
tt_data = pd.DataFrame(columns=('subj_idx','rt','response','task_type')); #for task type, discrim vs. detect
nr_targ_det_data = pd.DataFrame(columns=('subj_idx','rt','response','nr_targets'));
hf_det_data = pd.DataFrame(columns=('subj_idx','rt','response','same_hf'));
nr_targ_dis_data = pd.DataFrame(columns=('subj_idx','rt','response','nr_targets'));
hf_dis_data = pd.DataFrame(columns=('subj_idx','rt','response','same_hf'));

#this seems gross but it'll work: need to incorporate counter variables for each db
agg_count = 0; det_nr_count = 0; det_hf_count = 0; dis_nr_count = 0; dis_hf_count = 0; tt_count = 0;

#now do the actual loop
for t in flatten(trials):
	#cut out trials where subjects took too long (coded as result = -1)
	if (t.result==1)|(t.result==0):
		agg_data.loc[agg_count] = [t.sub_id, t.response_time/1000.0, t.result, t.nr_targets, t.same_hf, t.block_type]; #specify the response time in seconds for the HDDm fit later
		tt_data.loc[tt_count] = [t.sub_id, t.response_time/1000.0, t.result, t.block_type];
		agg_count+=1; tt_count+=1;
		if (t.block_type=='Detect'):
			nr_targ_det_data.loc[det_nr_count] = [t.sub_id, t.response_time/1000.0, t.result, t.nr_targets];
			det_nr_count+=1;
			if (t.nr_targets==2):
				hf_det_data.loc[det_hf_count] = [t.sub_id, t.response_time/1000.0, t.result, t.same_hf]
				det_hf_count+=1;
		elif (t.block_type=='Discrim'):
			nr_targ_dis_data.loc[dis_nr_count] = [t.sub_id, t.response_time/1000.0, t.result, t.nr_targets];
			dis_nr_count+=1;
			if (t.nr_targets==2):
				hf_dis_data.loc[dis_hf_count] = [t.sub_id, t.response_time/1000.0, t.result, t.same_hf]
				dis_hf_count+=1;

#2. save the DFs as csvs using pandas' built in features
# the index=False argument prevents Pandas from writig the row index to the cvs file
print 'Starting saving of csv files....';

agg_data.to_csv(savepath+'all_data.csv',index=False);
tt_data.to_csv(savepath+'task_type_data.csv',index=False);
nr_targ_det_data.to_csv(savepath+'nr_target_det_data.csv',index=False);
nr_targ_dis_data.to_csv(savepath+'nr_target_dis_data.csv',index=False);
hf_det_data.to_csv(savepath+'hf_det_data.csv',index=False);
hf_dis_data.to_csv(savepath+'hf_dis_data.csv',index=False);

print 'Done saving csvs!';


