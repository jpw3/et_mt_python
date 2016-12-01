#Multiple Target (Eyetracking Edition) Data Analysis code
#Author: James Wilmott, Winter 2016

#Designed to import et_mt data and analyze it

from pylab import *
import shelve #for database writing and reading
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
pc = lambda x:sum(x)/float(len(x)); #create a percent correct lambda function

datapath = '/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #'/Users/james/Documents/MATLAB/data/et_mt_data/'; #
shelvepath =  '/Users/jameswilmott/Documents/Python/et_mt_data/'; #'/Users/james/Documents/Python/et_mt_data/'; #

#import the persistent database to save data analysis for future use (plotting)
#subject_data = shelve.open(shelvepath+'mt_data');
#individ_subject_data = shelve.open(shelvepath+'individ_mt_data');

##########################################################################################


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
        print "Imported data for subject %s\n"%sub_id;
    print "Done..\n";
    return blocks;

def getTrials(all_blocks):
    #do some processing of trials...
	processed_blocks = [processTrials(b) for blocks in all_blocks for b in blocks];
    #then segment the trials all together
	trial_matrix = [[t for b in blocks for t in b.trials] for blocks in processed_blocks];
	print "Done..\n"
	return trial_matrix; #trial matrix will be a n by m, n is the number of trials for a subject and m is the number of subjects

def processTrials(b):
	#dimensions of b: list by number of subjects by number of trials
	#go through each trial and add fields as necessary
	for i,t in enumerate(b.trials):
	#code which hemifield the target was in
		#target absent conditions
		if (size(t.target_coors)==1):
			t.target_hf1 = 'none';
			t.target_hf2 = 'none';
			t.hf_locs = [t.target_hf1,t.target_hf2];
			continue;
		#get the first target's side
		if (t.target_coors[1,1]>0):	 #need to check that this works
			t.target_hf1 = 'right'; 
		else:
			t.target_hf1 = 'left';
	#code whether the hemifield of second target matched, if applicable
		if (t.nr_targets==2):
			if (t.target_loc[2,1]>0): #need to check this works
				t.target_hf2 = 'right';
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
		else:
			t.hf_match = -1; #code for single targets is -1
			t.target_hf2='none';
		#get the target hemifields together for easier processing in HF bias function
		t.hf_locs = [t.target_hf1,t.target_hf2];
	return b;


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
		self.dist_col = str(trialData.dist_col); #red or green
		self.target_dist = [trialData.target_distances]; #absolute distances from the origin
		self.distr_dist = [trialData.distractor_distances];
		self.target_coors = trialData.target_coors;
		self.dist_coors = trialData.dist_coors;
		self.trial_times = trialData.trial_times;
		self.initiation_latency = trialData.trial_times.initiation_latency*1000;
		self.response_time = self.trial_times.response_time*1000; #put every time into seconds
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
		self.reponse = str(trialData.response); #letter corresponding to presented
		self.result = trialData.result; #right or wrong, 1 or 0
		self.selected_type = trialData.selected_type; #precense or absence
		self.abort = trialData.abort_trial;
