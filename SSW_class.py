##### script to define the SSW class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the polar vortex and SSWs
##### in a given dataset. This includes climatologies of various variables, wave driving, SSW time
##### series, wavelet power spectra etc


#import necessary packages
import iris
import numpy as np
import iris.coord_categorisation as coord_cat
from collections import Counter



## build class
class SSW:
	
	## init function
	def __init__(self, dataset_name, years):
		self.dataset_name = dataset_name
		self.years = years

	# function to add month, season and year metadata
	def add_times(cube, time):
		coord_cat.add_month(cube, time, name='month')
		coord_cat.add_season(cube, time, name='clim_season')
		coord_cat.add_year(cube, time, name='year')
		coord_cat.add_day_of_year(cube, time, name='day_number')
		coord_cat.add_season_year(cube, time, name='season_year')
		return cube
	
	#callback function necessary for concatenating cubes	
	def callback(cube, field, filename): 
		del cube.attributes['history']
		del cube.attributes['valid_max']
		del cube.attributes['valid_min']
	
	
	## define a loader function. this loads cubes of data. adds extra time coordinates
	## using the user defined "add_times" function
	def loader(fname):
		##load all files defined in fname
		cubes = iris.load(fname)
		
		#check how many cubes
		if len(cubes) == 1:
			cube = cubes[0]
			cube = add_times(cube, 't')
		
		else:
			cube = cubes
		
		return cube

	
	## function to give the SSW rate in a given dataset over the whole time period
	def get_SSW_rate(self):
	
		#load presaved SSW year and month lists
		#self.SSW_month = genfromtxt(self.fnameSSWmonth)
		#self.SSW_year  = genfromtxt(self.fnameSSWyear)
		
		self.SSWrate = len(self.SSW_month)/np.float(len(self.years))
		
		return
	
	### function to give the error bounds on a given SSW rate
	### using bootstrap resampling. gives the mean +-
	def SSW_rate_Er(self, SSW_timeseries):
		
		## resample SSW time series and calculate set of rates
		rates = np.empty(0)
		for i in range(10000):
			rates = np.append(rates, np.mean(np.random.choice(SSW_timeseries, self.resample_interval, replace = False)))
		
		#get percentile of each of these rates		
		percentiles = np.percentile(rates, np.arange(0,101,1))
		
		#extract desired error % and return
		upper = percentiles[100 - self.bound]
		lower = percentiles[self.bound]
		
		SSWrate_Er = np.array([upper, lower])
		
		return SSWrate_Er, rates
	
	
	##call above function
	def get_SSW_rate_Er(self):
	
		self.SSWrate_Er = self.SSW_rate_Er(self.SSW_timeseries)[0]
		self.SSWrate_Er[0] = self.SSWrate_Er[0] - self.SSWrate
		self.SSWrate_Er[1] = np.abs(self.SSWrate - self.SSWrate_Er[1])
		return
	
	
	## function to produce a time series of the number of SSW events
	## in each winter season.
	def get_SSWs_timeseries(self):
		year_count = []
		SSW_year_counter = Counter(self.SSW_year)
		for i in range(len(self.years)):
			year_count = np.append(year_count, SSW_year_counter[self.years[i]])
		
		self.SSW_timeseries = np.array(year_count)
		
		return 

	##function for finding monthly SSW rate    
	def SSW_rate_1_month(self, mon):
        	#copy SSW year array
        	SSW_year2 = np.copy(self.SSW_year)
        	year_count = np.empty(0)
		
		#### filter to warmings of a single month
        	for i in range(len(self.SSW_month)):
                	if self.SSW_month[i] != str(mon):
                 		SSW_year2[i] = 0
        	
		SSW_year2 = filter(lambda a: a != 0, SSW_year2)
		
		#### count number per season
        	SSW_year_counter = Counter(SSW_year2)
        	for i in range(len(self.years)):
        	        year_count = np.append(year_count, SSW_year_counter[self.years[i]])
		
		Er = self.SSW_rate_Er(year_count)
        	per_season = np.mean(year_count)
        	
		return per_season, Er
   
  
	#function to find the monthly SSW rate and associated error
	def get_SSW_rate_months(self):
        	#load SSW month array
		months = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar']
         
         	#call SSW rate for 1 month function
         	rates = np.array([self.SSW_rate_1_month(i)[0] for i in months])
                Ers = np.array([self.SSW_rate_1_month(i)[1] for i in months])
         	
		self.SSWrates_mon = rates
		self.SSWrates_mon_Er = Ers         
         	
		return
	

	
	
	
	



	
	
	
	
	
		
		
