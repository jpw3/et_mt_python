#mat2csv takes the data for .mat files and turns it into .csvs for use in fitting the HDDM

#import relevant packages
from pylab import *
import shelve #for database writing and reading
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
import pandas #will use pandas DataFrame.to_csv() function to convert the data to a csv

datapath = '/Users/james/Documents/MATLAB/data/et_mt_data/'; #'/Users/jameswilmott/Documents/MATLAB/data/et_multi_targets/'; #
csvpath =  '/Users/james/Documents/Python/et_mt/data/'; #'/Users/jameswilmott/Documents/Python/et_mt/data/'; #

ids=['pilot_3','pilot_6','1','2','3','4','5','6','8','9']; #'jpw',


def constructNT(trials,id):
	#trials should be an array of all trials
	#create a dataframe and holder lists
	df = pandas.DataFrame();
	ids = []; rts = []; conditions = []; results = []; tasks = [];
	#first loop through the data, appending the relevant values to lists
	for t in trials:
		ids.append(t.sub_id);
		rts.append(t.response_time/1000.0);
		conditions.append(t.nr_targets);
		results.append(t.result);
		tasks.append(t.block_type);	
	#then, append the lists to the Dataframe
	df['id'] = array(ids);
	df['nr_targets'] = array(conditions);
	df['rt'] = array(rts);
	df['result'] = array(results);
	df['task'] = array(tasks);
	df.to_csv(csvpath+'et_mt_%s_NTxTask.csv'%id, index=False);
	print 'Completed constructing and saving .csv for number of targets data'
	return df



##### Importing methods #################################################################################################################

#returns all trials in an array of trials for use in fitting segregating into DataFrames
def getTrialArray(id):
	if id=='agg':
		blocks=getAllSubjectBlocks();
		#getIndividStats();
	else:
		blocks=[loadAllBlocks(id)]; #return as a list for use in get_Trials function
	trial_matrix=getTrials(blocks);
	return [t for trials in trial_matrix for t in trials]; #get all the trials together into an array

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
	return trial_matrix;

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
