#! env python

'''
code to extract out relevant qc data from fmriprep output.

sample file: desc-confounds_regressors.tsv


'''
import pandas as pd
import os
import fnmatch
import sys

class ExtractRegressors:
    def __init__(self,fpath):
        self.fpath=fpath  # path to fmriprep output
        
        # get list of all tsv files
        self.allfiles = self.find_confoundstsv(fpath)
        
        self.process_files(self.allfiles[:])
        
 
    def process_files(self, allfiles):
        # process all the files
            
        
        for file in allfiles:
            self.process_file(file['fullpath'])
      
        
    def process_file(self, fullpath):
        # parse filename
        fileinfo = self.parse_tsv_filename(fullpath)
        
        # read the tsv into the self.df
        self.readtsv(fullpath)
        
        # extract out the desired columns from data frame
        col_list = ['csf','white_matter','global_signal',
            'trans_x', 'trans_y', 'trans_z',
            'rot_x', 'rot_y', 'rot_z']

        newdf = self.df[col_list]

        # create the fullpath outputfile
        fullpathout  = os.path.join( os.path.dirname(fullpath),
            'sub-'+fileinfo['sub'] + '_ses-'+fileinfo['ses'] +'_task-' + fileinfo['task'] +
            '_run-' + fileinfo['run'] + '_regressors.1D')

        # write out tsv omitting the header and index column
        newdf.to_csv(fullpathout, sep = '\t', header=False, index=False)
        print(fullpathout)

    def readtsv(self, fullpath):
        # read a tsv file into a dataframe
        self.df =  pd.read_csv(fullpath, sep="\t")
        return self.df

    
    def parse_tsv_filename(self, filepath):
        """
        Parse the tsv filename
        
        extract out the sub, ses task and run

        "sub-902_ses-1602_task-eyegazeall_run-1_desc-confounds_regressors.tsv"
       
        "sub-1954711_ses-01_task-rest_acq-AP_run-1_desc-confounds_timeseries.tsv"
        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        fileinfo = {}
        
        # first parse based on _
        p1 = os.path.basename(filepath).split("_")
        
        # initialize vars
        sub = ""
        ses = ""
        task = ""
        acq = ""
        run = ""
        
        for p in p1:
            # check for each parameter
            
            if p.startswith('sub-'):
                sub = p.split('sub-')[1]
 
            if p.startswith('ses-'):
                ses = p.split('ses-')[1]
                
            if p.startswith('task-'):
                task = p.split('task-')[1]
  
            if p.startswith('acq-'):
                acq = p.split('acq-')[1]
                
            if p.startswith('run-'):
                run = p.split('run-')[1]
        
        fileinfo["sub"] = sub
        fileinfo["ses"] = ses
        fileinfo["task"] = task
        fileinfo["acq"] = acq
        fileinfo["run"] = run
       
        return fileinfo
        

    def find_confoundstsv(self, dir, stub="*desc-confounds_*.tsv"):
        '''
        Find the confounds tsv files starting at the provided
        directory. 

        First level starts with the sub-xxxx


        '''
        
        tsvfiles = []
        
        for root, dirs, files in os.walk(dir):
        
            for file in files: 
                tsvinfo = {}

                # change the extension from '.mp3' to 
                # the one of your choice.
                if fnmatch.fnmatch(file, stub):
                    #print (root+'/'+str(file))
                    #print(root + " : " +  str(file))
                    tsvinfo['root'] = root
                    tsvinfo['file'] = str(file)
                    tsvinfo['fullpath'] = root+'/'+str(file)
                    tsvfiles.append(tsvinfo)
                
        return tsvfiles
    


if __name__ == '__main__':

    fmriprepdir = '/home/share/eyegaze_BIDS/Derivs/fmriprep'
    
    # expect two arguments
    if len(sys.argv) == 2:
        qc = ExtractRegressors(sys.argv[1])
    else:
        print("Usage: ", sys.argv[0], " fmriprep_output_directory")


    
