##### script to define the equator class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the QBO and SAO
##### in a given dataset. This includes climatologies of various variables, power spectra
##### holton tan strength etc requires a cube of monthly U as input.




#import necessary packages
import iris
import numpy as np
import iris.coord_categorisation as coord_cat
import matplotlib.pyplot as plt


class mean_state:
		## init function
	def __init__(self, dataset_name, T, U_day, tname):
		self.dataset_name = dataset_name
		#self.U = U
		#self.V = V
		self.T = T
		self.U_day = U_day
       
		self.tname = tname
	
	
	### function to generate the daily climatology of [V'T'] for the mean state object
	def trop_wavedrive(self):
		
		#define latitude constraint
		def correct_lat(cell):
			return 40 < cell < 70
		lat_constraint = iris.Constraint(latitude = correct_lat)
		
		V = V.extract(lat_constraint)
		T = T.extract(lat_constraint)
		
		#calculate meridional heat flux
		T_Zon = T.collapsed('longitude', iris.analysis.MEAN)
		V_Zon = V.collapsed('longitude', iris.analysis.MEAN)	
		Tprime = T - T_Zon
		Vprime = V - V_Zon
		V.coord('latitude').guess_bounds()
		V.coord('longitude').guess_bounds()
		grid_areas = iris.analysis.cartography.area_weights(V)
		VpTp = Tprime*Vprime.data
		VpTp = VpTp.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights = grid_areas)
		
		# take daily clims
		VpTp_means = VpTp.aggregated_by('day_number', iris.analysis.MEAN)
		VpTp_std = VpTp.aggregated_by('day_number', iris.analysis.STD_DEV)
		self.meanVT = np.append(VpTp_means[int(len(VpTp_means.data)/2):-1].data, VpTp_means[0:int(len(VpTp_means.data)/2)].data)
		self.stdVT = np.append(VpTp_std[int(len(VpTp_std.data)/2):-1].data, VpTp_std[0:int(len(VpTp_std.data)/2)].data)
		
		return 
	
	#function to take monthly climatology
	def clim(U):
		U_months = U.aggregated_by('month', iris.analysis.MEAN)
		return U_months
	
	 
	## lat-heigt climatologies
	def get_clims(self):
		self.climT = self.T.aggregated_by('month', iris.analysis.MEAN)
		#self.climU = self.U.aggregated_by('month', iris.analysis.MEAN)
	
		return
	
	##mean state vortex strength (10hPa daily winds as inputs)
	def vortex_clim(self):
         coord_cat.add_day_of_year(self.U_day, self.tname, name='day_number')
         
         ## quick find nearest latitude to 60 function
         def find_nearest(array, value):
             array = np.asarray(array)
             idx = (np.abs(array - value)).argmin()
             return array[idx]
         
         lat = find_nearest(self.U_day.coord('latitude').points, 60)
         U_vortex = self.U_day.extract(iris.Constraint(latitude = lat))
         plt.plot(np.arange(365), U_vortex[0:365].data)
         plt.show()
         self.vortex_clim = U_vortex.aggregated_by('day_number', iris.analysis.MEAN)
         self.vortex_climSTD = U_vortex.aggregated_by('day_number', iris.analysis.STD_DEV)

         return
	
	
	
	
	
	
	
	
	
	
	
