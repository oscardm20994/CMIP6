##### script to define the ozone class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of equatorial ozone and how it
##### relates to the QBO, SAO, polar vortex and SSWs
##### in a given dataset. This includes climatologies of various variables, wave driving, SSW time
##### series, wavelet power spectra etc
##### requires pre loading and some processing of an SSW iris list and O3 iris cube


#import necessary packages
import iris
import numpy as np
import iris
import iris.coord_categorisation as coord_cat
import iris.plot as iplt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import math
import pandas as pd
from collections import Counter
from netCDF4 import num2date, date2num
from datetime import datetime, timedelta
from eofs.standard import Eof


	

class O3_class_def:	
	
	## init function
	def __init__(self, dataset_name, years, O3_eq, U, SSW_list, U_eq, O3_SPC):
		self.dataset_name = dataset_name
		self.years = years         
		self.O3 = O3
		self.SSW = SSW_list
		self.U = U
		self.U_eq = U_eq
	### function to get the 
	
	def extract_SSW_from_Y(self, Y_list):
	
		Y_years_plus1 = []
		Y_years = []
		SSW_decimal = np.empty(0)
	
		## get Y years from cube list
		for i in range(len(Y_list)):
			Y_years_plus1.append(Y_list[i].coord('year').points[0] + 1)
			Y_years.append(Y_list[i].coord('year').points[0])

	
		## extract other variable years from SSW years
		SSW_DJFM = self.SSW.extract(iris.Constraint(month = ['Jan','Feb','Mar']))
		SSW_DJFM = SSW_DJFM.extract(iris.Constraint(season_year = Y_years_plus1))	
		SSW_N = self.SSW.extract(iris.Constraint(month = ['Dec','Nov']))
		SSW_N = SSW_N.extract(iris.Constraint(season_year = Y_years))
		SSW_new = SSW_DJFM
	
		## add SSW_N to SSW_DJFM
		for i in range(len(SSW_N)):
			SSW_new.append(SSW_N[i])
	
		### get months and years out of SSW_new
		months = get_coord_from_list(SSW_new, 'month')
		years = get_coord_from_list(SSW_new, 'season_year')		



		return	SSW_new, months, years

	
	### find anomalous O3 years and get SSW rates in these years
	def O3_bands_vs_SSWs(self):
		
		#isolate 10-20hPa ozone in early winter
		ASON = self.O3_SPC.extract(iris.Constraint(month = ['Aug','Sep','Oct'])).extract(iris.Constraint(air_pressure = 10000.))
		ASON_all = ASON.aggregated_by('year', iris.analysis.MEAN)#ASON.collapsed(['air_pressure'], iris.analysis.MEAN)
		
		##year array	
		years = self.years
	
		#divide time series into bands. take the years in which data lies in the bands and
		#count SSWs
		O3_bands = np.percentile(ASON_all.data, np.arange(0,110,10))
		print O3_bands
		rates_in_bands = np.empty(0)
		sigs = np.empty(0)
		Er = np.zeros([10, 2])

		#loop over bands counting SSWs
		for i in range(len(O3_bands) - 1):
			years_in_band = years[np.where(np.logical_and(ASON_all.data>=O3_bands[i], ASON_all.data<=O3_bands[i+1]))]
			SSWs_in_band = self.SSW.extract(iris.Constraint(year = years_in_band))
			
			if len(SSWs_in_band.data) == 0:
				rates_in_bands = np.append(rates_in_bands, 0) 
			else:
				rates_in_bands = np.append(rates_in_bands, np.float(len(SSWs_in_band.data))/np.float(len(years_in_band)))
			#Er[i,:] = warmings_per_decade(SSWs_in_band.coord('year').points, SSWs_in_band.coord('month').points, years_in_band)
		
		
		#Er[:,0] -= rates_in_bands
		#Er[:,1] = np.abs(Er[:,1] - rates_in_bands)
		#print Er
		#wrap the SSW rate for each band over time dimension
		rate_2d = np.tile(rates_in_bands, (len(ASON_all.data),1))
		
		#asign temporary variables to instance of class
		self.ASON_O3 = ASON_all
		self.rates_in_bands = rates_in_bands
		self.rate_2d = rate_2d
		self.O3_bands = O3_bands
		#self.Er_in_O3_bands = Er		
		print
		return
	
	##function to produce the seasonal cycle in equatorial ozone mole fraction
	def O3_cycles(self):
		self.O3cycle = self.O3.aggregated_by('month', iris.analysis.MEAN)
		self.O3cycle_std = self.O3.aggregated_by('month', iris.analysis.STD_DEV)
	
		return
	
	#call composite function and EOFs above for T, U and SW heating
	def get_composites(self):
         self.U_inO3 = O3_bands_vs_EPdiv(self.O3, self.U, self.years )
         #self.U_inQBO = O3_bands_vs_EPdiv(self.U_eq, self.U, self.years )

         #self.T_inO3 = self.O3_bands_vs_EPdiv(self.O3, self.T)
		#self.SW_inO3 = self.O3_bands_vs_EPdiv(self.O3, self.SW)
		
         #self.Ueof, self.Upc, self.Uvar_frac = eof(self.U_inO3) 
         #self.UeofinQBO, self.UpcinQBO, self.Uvar_fracinQBO = eof(self.U_inQBO) 

         #self.Teof, self.Tpc, self.Tvar_frac = self.eof(self.T_inO)
		#self.SWeof, self.SWpc, self.SWvar_frac = self.eof(self.SW_inO3)
         return
	
	
	
	##### consider the eof of composites for each band
	def eof(in_bands):
		data = np.array([in_bands[i].data for i in range(len(in_bands))])
	
		#take eof over time dimension
		solver = Eof(data)
	
		eof1 = solver.eofs(neofs=1)[0,:]
		cube = in_bands[0].copy()
		cube.data = eof1

		pc1 = solver.pcs(pcscaling = 1, npcs = 1)[:,0]
		var_frac = solver.varianceFraction(neigs=1)[0]
		return cube, pc1, var_frac
	
	
	

	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
