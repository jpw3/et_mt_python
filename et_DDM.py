# Script to confirm the validity of ANOVA calculation in MATLAB for DDM params

from pylab import *
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
import random #general purpose
from collections import namedtuple
import pyvttbl as pt

## Data Object to get all the data where it needs to be
class Real_data(object):
	def __init__(self,object):
		#subject data
		self.nt_data_detect_res  = object['nt_data'].detect.res; #nt
		self.nt_data_detect_rts  = object['nt_data'].detect.rts;
		self.st_data_detect_res  = object['st_data'].detect.res; #st
		self.st_data_detect_rts  = object['st_data'].detect.rts;
		self.st_data_discrim_res  = object['st_data'].discrim.res;
		self.st_data_discrim_rts  = object['st_data'].discrim.rts;
		self.mt_data_detect_res  = object['mt_data'].detect.res; #mt
		self.mt_data_detect_rts  = object['mt_data'].detect.rts;
		self.mt_data_detect_same_hf_res  = object['mt_data'].detect.same_hf.res;
		self.mt_data_detect_same_hf_rts  = object['mt_data'].detect.same_hf.rts;
		self.mt_data_detect_diff_hf_res  = object['mt_data'].detect.diff_hf.res;
		self.mt_data_detect_diff_hf_rts  = object['mt_data'].detect.diff_hf.rts;
		self.mt_data_discrim_res  = object['mt_data'].discrim.res;
		self.mt_data_discrim_rts  = object['mt_data'].discrim.rts;			
		self.mt_data_discrim_same_hf_res  = object['mt_data'].discrim.same_hf.res;
		self.mt_data_discrim_same_hf_rts  = object['mt_data'].discrim.same_hf.rts;
		self.mt_data_discrim_diff_hf_res  = object['mt_data'].discrim.diff_hf.res;
		self.mt_data_discrim_diff_hf_rts  = object['mt_data'].discrim.diff_hf.rts;
		#parameters
		self.nt_params_detect_as = object['nt_params'].detect.ays; #nt
		self.nt_params_detect_vs = object['nt_params'].detect.vs;
		self.nt_params_detect_ters = object['nt_params'].detect.ters;
		self.st_params_detect_as = object['st_params'].detect.ays; #st
		self.st_params_detect_vs = object['st_params'].detect.vs;
		self.st_params_detect_ters = object['st_params'].detect.ters;		
		self.st_params_discrim_as = object['st_params'].discrim.ays; 
		self.st_params_discrim_vs = object['st_params'].discrim.vs;
		self.st_params_discrim_ters = object['st_params'].discrim.ters;			
		self.mt_params_detect_as = object['mt_params'].detect.ays; #mt
		self.mt_params_detect_vs = object['mt_params'].detect.vs;
		self.mt_params_detect_ters = object['mt_params'].detect.ters;		
		self.mt_params_discrim_as = object['mt_params'].discrim.ays; 
		self.mt_params_discrim_vs = object['mt_params'].discrim.vs;
		self.mt_params_discrim_ters = object['mt_params'].discrim.ters;			

## Import the data that needs to be confirmed with a repeated measures anova
filename = '/Users/james/Documents/MATLAB/et_DDM_data.mat';
mat_data = loadmat(filename,struct_as_record=False,squeeze_me=True);
data = Real_data(mat_data);

#create the named tuple for installing, then put all the data together and run the test ANOVA
score = namedtuple('score',['id','a_param','nr_targets']);
df = pt.DataFrame();

for nt,scores in zip([0,1,2],[data.nt_params_detect_as,data.st_params_detect_as,data.mt_params_detect_as]):
	for i,a in enumerate(scores):
		df.insert(score(i,a,nt)._asdict()); #append the params to the dataframe

#print the results
print(df.anova('a_param',sub='id',wfactors=['nr_targets']));
		
		