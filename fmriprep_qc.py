#! env python

'''
code to extract out relevant qc data from fmriprep output.

sample file: desc-confounds_regressors.tsv


'''
import pandas as pd
#import matplotlib.pyplot as plt
import os
import fnmatch
import sys

class SummarizeQC:
    def __init__(self,fpath):
        self.fpath=fpath  # path to fmriprep output
        
        # get list of all tsv files
        self.allfiles = self.find_confoundstsv(fpath)
        
        self.dfsummary = self.process_files(self.allfiles[:])
        
        # write out to csv
        self.dfsummary.to_csv('summary.csv', index=False)
        
        # write out to hdf5
        # To read hdf5
        # d = pd.read_hdf('summary.h5','summary')
        self.dfsummary.to_hdf('summary.h5', key='summary',mode='w')
 
        
 
    def process_files(self, allfiles):
        # process all the files
        
        # list of columns to generate
        # this supports metageneration of the output to simplify code
        col_list =[
            ['sub'],
            ['ses'],
            ['task'],
            ['acq'],
            ['run'],
            ['fd-per', 'framewise_displacement', 'percent'],
            ['fd-mean', 'framewise_displacement', 'mean'],
            ['fd-std', 'framewise_displacement', 'std'],
            ['fd-max', 'framewise_displacement', 'max'],
            ['fd-min', 'framewise_displacement', 'min'],
            ['dvars-per', 'dvars', 'percent'],
            ['dvars-mean', 'dvars', 'mean'],
            ['dvars-std', 'dvars', 'std'],
            ['dvars-max', 'dvars', 'max'],
            ['dvars-min', 'dvars', 'min'],
            ['std_dvars-per', 'std_dvars', 'percent'],
            ['std_dvars-mean', 'std_dvars', 'mean'],
            ['std_dvars-std', 'std_dvars', 'std'],
            ['std_dvars-max', 'std_dvars', 'max'],
            ['std_dvars-min', 'std_dvars', 'min'],
            ]
        
        # create the dictionary of lists that hold the columns
        dict = {}
        for item in col_list:
            dict[item[0]] = []
            
        
        for file in allfiles:
            res = self.process_file(file['fullpath'])
            
            # load data into the dictonary of lists
            self.retrieve_load_value(col_list, dict, res)

        
        # create the dataframe
        df = pd.DataFrame(dict)
    
        return df
    
    def retrieve_load_value(self,col_list, dict, res):
        """
        retrieves and loads results into output dictionary

        Parameters
        ----------
        col_list : TYPE
            DESCRIPTION.
        dict : TYPE
            DESCRIPTION.
        res : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
    
        for data_item in col_list:
            # check how many items in list
            if len(data_item) == 1:
                # res has single key
                dict[data_item[0]].append(res[data_item[0]])
            else: 
                # res has multiple keys
                dict[data_item[0]].append(res[data_item[1]][data_item[2]])
          
        
    def process_file(self, fullpath):
        # parse filename
        fileinfo = self.parse_tsv_filename(fullpath)
        
        # read the tsv
        self.readtsv(fullpath)
        
        items = {"framewise_displacement": 0.5,
                 "dvars": 1.5, 
                 "std_dvars": 1.5, 
                 }
        
        # calculate the desired stats for selected items
        res = self.calcstats(items) 
        fileinfo.update(res)
        print(fileinfo['sub'])
        #print(res)
        return fileinfo
    
    def readtsv(self, fullpath):
        # read a tsv file into a dataframe
        self.df =  pd.read_csv(fullpath, sep="\t")
        return self.df

    def calcstats(self, items):
        # return counts that exceed thresholds of provided items
        # items is a dictionary with the column name and value

        res = {}  # dictionary returning results

        for key in items:
            res2 = {}
            # get the series for this item
            ser = self.df[key]
            size = len(ser) 
            res2["mean"] = ser.mean()
            res2["std"] = ser.std()
            res2["min"] = ser.min()
            res2["max"] = ser.max()
            
            # get the number of items that exceed the threshold
            num = self.df[self.df[key] > items[key] ].shape[0]
            res2["percent"] = 100.0 * num/size
            
            #print(key, num)
            res[key] = res2
        return res
    
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
    
    def sampletest(self):
        df = qc.readtsv()
        print(df.info())
        print(df.loc[0])
  
        # get the dvars column
        #df = qc.df[["dvars","framewise_displacement"]]
        #df = qc.df[["framewise_displacement"]]
    
        items = {"dvars": 20, "framewise_displacement": 0.2 }
    
        res = qc.calcstats(items)
        print(res)
        print(df.shape)
        abovethresh = df [df["framewise_displacement"]> 0.2]
        print(abovethresh.shape[0])
        #df.plot()
        #plt.legend()
        #plt.savefig("mygraph.png")
        #plt.show()

if __name__ == '__main__':

    fmriprepdir = '/home/share/eyegaze_BIDS/Derivs/fmriprep'
    
    # expect two arguments
    if len(sys.argv) == 2:
        qc = SummarizeQC(sys.argv[1])
    else:
        print("Usage: ", sys.argv[0], " fmriprep_output_directory")


    
