##### script to define the equator class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the QBO and SAO
##### in a given dataset. This includes climatologies of various variables, power spectra
##### holton tan strength etc requires a cube of monthly U as input.




#import necessary packages
import iris
import numpy as np
import cf_units
from scipy.fftpack import fft, fftfreq

class equator:
	## init function
	def __init__(self, dataset_name, U, tname):
		self.dataset_name = dataset_name
		self.U = U
		self.tname = tname
		##isolate pressure coordinate name
		self.pname = 'air_pressure'#[c for c in self.U.coords.long_name() if c.units.definition==cf_units.Unit("hectopascal").definition][0].name()
	
	###function to get the power spectrum at all heights
	#function to find fourier power spectrum of QBO series
	def power_spectrum(self):
		#dt in months
		dt = 1
		
		##define lat constraint
		#contrain latitudes
		def correct_lat(cell):
			return -5.1 < cell < 5.1

		lat_constraint = iris.Constraint(latitude = correct_lat)
		
		#restrcit latitudes and average over lats
		U_QBO = self.U.extract(lat_constraint)
		U_QBO = U_QBO.collapsed('latitude', iris.analysis.MEAN) 
	    
		#compute fast fourier transform
		fft_U = fft(U_QBO.data, axis = 0)
 		#get associated frequencies
		freq = fftfreq(U_QBO.data[:,0].size, d=dt)
	
		#throw away negative freqs
		keep = freq>=0
		fft_U = fft_U[keep,:]
		freq = freq[keep]
		self.spec = np.array([np.abs(fft_U[:,i])/np.std(U_QBO.data, axis = 0)[i] for i in range(len(fft_U[0,:]))])
		self.freq = freq
		return
	
	
	
	## function to pick out dates for low and high QBO ZMZW 
	def pick_QBO_extremes(self, p_constraint):
		#restrict to chosen height 
		U_QBO = self.U.extract(p_constraint)
		
		##define lat constraint
		#contrain latitudes
		def correct_lat(cell):
			return -5.1 < cell < 5.1

		lat_constraint = iris.Constraint(latitude = correct_lat)
		
		#restrcit latitudes and average over lats
		U_QBO = U_QBO.extract(lat_constraint)
		U_QBO = U_QBO.collapsed('latitude', iris.analysis.MEAN) 
	
		#only retain extended winter months
		U_QBO = U_QBO.extract(iris.Constraint(month = ['Oct','Nov','Dec','Jan','Feb','Mar']))

		#take time mean and standard deviation
		mean = np.mean(U_QBO.data)
		std = np.std(U_QBO.data)	
	
		#get indices in increasing order, select the top and bottom 10% of the time array
		indices = np.argsort(U_QBO.data)
	
		#sort cube by magnitude of wind
		U_QBO_sorted = U_QBO[indices]
		time_sorted = U_QBO_sorted.coord(self.tname).points

		#find number of time points in 10% of dataset
		t_10 = np.int(len(U_QBO.data)/10)
	
		low_times = time_sorted[0:t_10]
		high_times = time_sorted[:(-1*t_10)]
	
		#get time units
		timeUnits = U_QBO.coord(self.tname).units

		#convert points to datetime
		low_dates = timeUnits.num2date(low_times)
		high_dates = timeUnits.num2date(high_times)
	
		return low_dates, high_dates

	
	##function to composite differences in E and W QBO time
	def composite_dif(self, low_dates, high_dates):
		#constrain time
		if self.tname == 'time':
			high_comp = self.U.extract(iris.Constraint(time = low_dates))
			low_comp = self.U.extract(iris.Constraint(time = high_dates))
		else:
			high_comp = self.U.extract(iris.Constraint(t = low_dates))
			low_comp = self.U.extract(iris.Constraint(t = high_dates))
		#time mean and std for composite
		low_mean = low_comp.collapsed(self.tname, iris.analysis.MEAN) 
		high_mean = high_comp.collapsed(self.tname, iris.analysis.MEAN)
	
		return high_mean - low_mean.data

    ## quick find nearest latitude to 60 function
	def find_nearest(self, value):
		array = np.asarray(self.U.coord('air_pressure').points)
		idx = (np.abs(array - value)).argmin()
		return array[idx]
         
	## function to get strength of holton tan
	def holton_tan(self):
         nearestp = self.find_nearest(50000)
         low_dates, high_dates = self.pick_QBO_extremes(iris.Constraint(air_pressure = nearestp))
         self.HT = self.composite_dif(low_dates, high_dates)
         return
	


  
	def SAO(self):
         def correct_press(cell):
             return cell < 100.1
		
         press_con_mod = iris.Constraint(air_pressure = correct_press)
         
         def correct_lat(cell):
			return -5.1 < cell < 5.1
   
         lat_con = iris.Constraint(latitude = correct_lat)
         U_equ = self.U.extract(lat_con).collapsed('latitude', iris.analysis.MEAN) 

         
         self.SAO_U_equ = U_equ.extract(press_con_mod)
         self.SAO = U_equ.aggregated_by('month', iris.analysis.MEAN)
	
         return
	
	
	
	
