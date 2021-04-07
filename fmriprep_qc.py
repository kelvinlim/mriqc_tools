#!/bin/env python3

'''
code to extract out relevant qc data from fmriprep output.

sample file: desc-confounds_regressors.tsv


'''
import pandas as pd
import matplotlib.pyplot as plt

class SummarizeQC:
    def __init__(self,fpath):
        self.fpath=fpath

    def readtsv(self):
        self.df =  pd.read_csv(self.fpath, sep="\t")
        return self.df

    def calcstats(self, items):
        # return counts that exceed thresholds of provided items
        # items is a dictionary with the column name and value

        res = {}  # dictionary returning results

        for key in items:
            res2 = {}
            # get the series for this item
            ser = self.df[key]
            res2["mean"] = ser.mean()
            res2["std"] = ser.std()
            res2["min"] = ser.min()
            res2["max"] = ser.max()
            
            # get the number of items that exceed the threshold
            num = self.df[self.df[key] > items[key] ].shape[0]
            #print(key, num)
            res[key] = res2
        return res

if __name__ == '__main__':

    qc = SummarizeQC("desc-confounds_regressors.tsv")
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


    
