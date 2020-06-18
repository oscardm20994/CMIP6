from mean_state_class import mean_state
from SSW_class import SSW
from SSW_class import equator
from O3_class import O3
import numpy as np
import iris


#functiont to create instances of the mean state class
def create_mean_state_instance(self, dataset_name, U, V, T, U_day, tname):

	instance = mean_state(dataset_name, U, V, T, U_day, tname)
	instance.trop_wavedrive()
	instance.get_clims()
	instance.vortex_clim()
	
	##save diagnostic values in pickle files
	pre = './data/processed_diagnostics/' + instance.dataset_name + '_' 
	
	## climatologies
	iris.save(instance.climU, pre + 'U_clim.nc')   
	iris.save(instance.climT, pre + 'T_clim.nc')
	
	##wave driving (cycle and standard deviations)
	iris.save(iris.cube.CubeList([instance.meanVT, instance.stdVT]), pre + 'VT.nc')   

	## daily vortex climatology
	iris.save(instance.vortex_clim, pre + '60N_10hPa_clim.nc')
	
	return instance

#functiont to create instances of the SSW class, calculate SSW rate and error bounds
def create_SSW_instance(dataset_name, years, SSWyear, SSWmonth):

	instance = SSW(dataset_name, years)
	instance.SSW_year = SSWyear
	instance.SSW_month = SSWmonth
	instance.resample_interval = 50
	instance.bound = 5
	instance.get_SSW_rate()
	instance.get_SSWs_timeseries()
	instance.get_SSW_rate_Er()
	instance.get_SSW_rate_months()
	
	##save diagnostic values in pickle files
	pre = './data/processed_diagnostics/' + instance.dataset_name + '_' 
	
	## save SSW rates over whole season
	fileObject = open(pre + 'SSW_rates_whole_season','wb')
	array = [instance.SSWrate, instance.SSWrate_Er]
	pickle.dump(array, fileObject)   
		
	## save SSW rates for each month
	fileObject = open(pre + 'SSW_rates_monthly','wb')
	array = [instance.SSWrates_month, instance.SSWrates_month_ER]
	pickle.dump(array, fileObject)
	
	## save SSW rates for each month
	fileObject = open(pre + 'SSW_time_series','wb')
	array = [instance.SSW_timeseries]
	pickle.dump(array, fileObject)
		   
    	return instance

#functiont to create instances of the O3 class
def create_O3_instance(dataset_name, years, O3, U, T, SW, SSW_list):
	
	#initialise instance and assign variables
	instance = O3(dataset_name, years, O3, SSW_list)
	instance.O3_bands_vs_SSWs()
	instance.O3_cycles()
	instance.get_composites()
	
	
	## save each of these diagnostics
	pre = './data/processed_diagnostics/' + instance.dataset_name + '_' 
	
	#iris cubelist for O3 equatorial cycle and STD
	iris.save(iris.cube.CubeList([instance.O3cycle, instance.O3cycle_std]), pre + 'O3_cycles.nc')
	
	# ASO equatorial ozone annual mean
	iris.save(instance.ASON_O3, pre + 'ASO_O3.nc')
	
	#3D array with O3 percentile bands, SSW rates in each band and errors on rates, saved as pickle 
	fileObject = open(pre + 'O3_band_arrays','wb')
	array = [[instance.O3_bands], [instance.rates_in_bands], [instance.Er_in_O3_bands]]
	pickle.dump(array, fileObject) 
	
	# iris cubelists of U,T,SW composites for each band
	iris.save(instance.U_inO3, pre + 'U_inO3.nc')
	iris.save(instance.T_inO3, pre + 'T_inO3.nc')
	iris.save(instance.SW_inO3, pre + 'SW_inO3.nc')
	
	#iris cubes of EOFS and PCs in U,T,SW ozone bands, done in pickle files
	fileObject = open(pre + 'EOF_U_O3_band_arrays','wb')
	array = [[instance.Ueof], [instance.Upc], [instance.Uvar_frac]]
	pickle.dump(array, fileObject) 
	
	fileObject = open(pre + 'EOF_T_O3_band_arrays','wb')
	array = [[instance.Teof], [instance.Tpc], [instance.Tvar_frac]]
	pickle.dump(array, fileObject) 
	
	fileObject = open(pre + 'EOF_SW_O3_band_arrays','wb')
	array = [[instance.SWeof], [instance.SWpc], [instance.SWvar_frac]]
	pickle.dump(array, fileObject) 
	
    return instance



#functiont to create instances of the O3 class
def create_equator_instance(dataset_name, U, tname):

	instance = equator(dataset_name, U, tname)
	instance.power_spectrum()
	instance.SAO()
	instance.holton_tan()
	
	##save variables
	pre = './data/processed_diagnostics/' + instance.dataset_name + '_' 
	
	## save SAO
	iris.save(instance.SAO, pre + 'SAO.nc')
	
	##save holton_tan composite
	iris.save(instance.HT, pre + 'Holton_Tan.nc')

	##save power spectrum composite
	fileObject = open(pre + 'U_power_spectrum','wb')
	array = [instance.spec, instance.freq]
	pickle.dump(array,fileObject)
	
	return instance






