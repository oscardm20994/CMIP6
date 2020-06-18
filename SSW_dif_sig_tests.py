#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 08:40:52 2020

@author: oscar
"""

import numpy as np
import scipy


#### function to perform a parametric stats test on two sets of SSW data
#### arguements are time series of SSW years
def parametric_test(chems, no_chems):
    
	#### lenghts of the data series
	l1 = sum([len(chems[i].years) for i in range(len(chems))])
	l2 = sum([len(no_chems[i].years) for i in range(len(no_chems))])
	rho = l1/np.float(l2)
	
	#### total SSWs in each dataset
	n1 = sum([len(chems[i].SSW_year) for i in range(len(chems))])
	n2 = sum([len(no_chems[i].SSW_year) for i in range(len(no_chems))])
	
	##W test statistic
	W = 2*(np.sqrt(n1 + 3/8.) - np.sqrt(rho*(n2 + 3/8.)))/np.sqrt(1+rho) 
	
	### p value for this test statistic
	p = 1 - np.abs(1-2*scipy.stats.norm.cdf(W))

	return p

#### function to perform a bootstrap stats test on two sets of SSW data
#### this is done by pooling both SSW year datasetc, randomly selecting
#### 2 random subsets of the same size as original data and taking SSW length difference
def bootstrap_sig_test(chems, no_chems):
	
    all_no_chems = np.array(no_chems[0].SSW_timeseries)
    for i in range(1,len(no_chems)):
        all_no_chems = np.append(all_no_chems, no_chems[i].SSW_timeseries)
        
    all_chems = np.array(chems[0].SSW_timeseries)
    for i in range(1,len(chems)):
        all_chems = np.append(all_chems, chems[i].SSW_timeseries)
    
     #### lenghts of the data series
	l1 = sum([len(chems[i].years) for i in range(len(chems))])
	l2 = sum([len(no_chems[i].years) for i in range(len(no_chems))])
	
	#### total SSWs in each dataset
	n1 = sum([len(chems[i].SSW_year) for i in range(len(chems))])
	n2 = sum([len(no_chems[i].SSW_year) for i in range(len(no_chems))])   
        
	### real difference in SSW rates
	real_dif = np.abs(n1/np.float(l1) - n2/np.float(l2))
		
	### pool SSW years datasets
	SSW_pooled = np.append(all_chems, all_no_chems)
		
	## loop over bootstrapping, partition into 2 subsets (same size as original SSW arrays)
	## store difference in SSW rates in dif array
	dif = np.empty(0)
	for j in range(10000):
		print j
		ind = np.random.choice(range(SSW_pooled.shape[0]), size=len(all_chems), replace=False)
		rest = np.array([i for i in range(0,SSW_pooled.shape[0]) if i not in ind])
		
		dummy1 = SSW_pooled[ind]
		dummy2 = SSW_pooled[rest]
		
		dif = np.append(dif, np.abs(np.sum(dummy1)/np.float(l1) - np.sum(dummy2)/np.float(l2)))
	
	percentiles = np.percentile(dif, np.arange(0,100.001,0.001))
	idx = (np.abs(percentiles - real_dif)).argmin()
	
	return dif, real_dif, 1-idx

