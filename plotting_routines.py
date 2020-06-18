import iris
import iris.coord_categorisation as coord_cat
import sys
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
import scipy
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib import gridspec
import scipy as sp
import matplotlib.colors as colors

## add one axis of [V'T']
def VT_axis(VpTp_means, VpTp_std, month_flip, label, c, std, alpha):
	# rearrange months
    if month_flip == True: 
        mean = np.append(VpTp_means[int(len(VpTp_means.data)/2):-1].data, VpTp_means[0:int(len(VpTp_means.data)/2)].data)
    else:
        mean = VpTp_means.data
	#get time array of correct length
	
	
	#if std == True:
         #std = np.append(VpTp_std[int(len(VpTp_std.data)/2):-1].data, VpTp_std[0:int(len(VpTp_std.data)/2)].data)
         #plt.plot(time, mean, color = c , label = label, linewidth = 0.65)
         #plt.plot(time, mean + std, linestyle = '--', color = c, alpha = alpha, linewidth = 0.65)
         #plt.plot(time, mean - std, linestyle = '--', color = c, alpha = alpha, linewidth = 0.65)
	#else:
    print 'here'
    time = np.linspace(0,12,len(mean))

    plt.plot(time, mean, color = c, label = label, alpha = alpha, linewidth = 0.65)
    return

## function to add one axis of equatorial ozone seasonal cycle or STD
def O3_cycle_axis(cycle, std, title, lev):
	##months array
	month = [' ', 'Jul', ' ', 'Aug', ' ', 'Sep', ' ', 'Oct', ' ', 'Nov' , ' ', 'Dec',' ', 'Jan', ' ', 'Feb', ' ', 'Mar', ' ', 'Apr', ' ', 'May', ' ', 'Jun',]

	#initialise axis object for either cycle or STD cycle 
	plt.title(titles[i], fontsize = 12)
	cmap = 'Blues'
	SAO = np.concatenate((np.transpose(cycle.data[6:,:]), np.transpose(cycle.data[0:6,:])), axis = 1)
	cont = plt.contourf(np.arange(12), cycle.coord(pname).points, SAO , lev, cmap=cmap)

	plt.ylabel('Pressure, mb', fontsize = 12)
	plt.xticks(np.arange(0,11,0.4583333333333333), month)
	plt1.set_yscale('log')
	plt.ylim(100,0.03)
	plt.xlim(0,11)
	cbar = fig.colorbar(cont)
	
	return

## add axis of SSW rate in O3 bands
def O3_vs_SSW_axis(O3_bands, rates_in_bands, Er, c, name):
	##find middle of ozone bins
	bin_mids = [O3_bands[i] + (O3_bands[i+1] - O3_bands[i])/2 for i in range(len(O3_bands) - 1)]
	
	## add axis of errorbar plot
	plt.plot(rates_in_bands, bin_mids, color = c, alpha = 0.6, label = name)
	
	return

#figure function for composites of variables in O3 bands
def plot_band_list(List, fname, lev, O3_bands, rates_in_bands):
	fig = plt.figure(figsize=(13, 18), dpi = 100)
	index_grid = np.arange(9).reshape([3,3])
	gs = gridspec.GridSpec(4, 3)							
	for i in range(3):
		for j in range(3):
			plt1 = plt.subplot(gs[i,j])
			divs = List[index_grid[i,j]]

			qplt.contourf(divs, lev , cmap = 'bwr')	
			qplt.contour(divs, levels = [0], colors = 'black')	

			plt.title(str(rates_in_bands[index_grid[i,j]]) + ' events/year, O$_3$ Percentile ' + str(10*index_grid[i,j]) + '-' + str(10+10*index_grid[i,j]))
			plt1.set_yscale('log', basey=10, subsy=None)
			plt.ylim(5,10000)
			plt1.invert_yaxis()
			plt.ylabel('Pressure (Pa)')
			plt.xlabel('Latitude')

	plt1 = plt.subplot(gs[3,0])
	divs = List[9]
	qplt.contourf(divs, lev, cmap = 'bwr')	
	qplt.contour(divs, levels = [0], colors = 'black')	

	plt.title(str(rates_in_bands[index_grid[i,j]]) + ' events/year, O$_3$ Percentile 90-100')
	plt1.set_yscale('log', basey=10, subsy=None)
	plt.ylim(5,10000)
	plt1.invert_yaxis()
	plt.ylabel('Pressure (Pa)')
	plt.xlabel('Latitude')		
	plt.tight_layout()
	plt.show()
	fig.savefig('./figures/' + fname , dpi = 200)

	return
 
class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

 
norm=MidpointNormalize(midpoint=0)
 
## axis function for EOF across band composites
def EOF_axis(EOF, var_frac, plt1, title, lev):
	qplt.contourf(EOF, lev, cmap = 'bwr')	
	plt.title('1st eof (' + str(var_frac) + ' of total variance)' + title)
	plt1.set_yscale('log', basey=10, subsy=None)
	plt.ylim(100,10000)
	plt1.invert_yaxis()
	plt.ylabel('Pressure (Pa)')
	plt.xlabel('Latitude')
	
	return

def PC_axis(pc1, O3_bands, rates_in_bands, Er):
	##get bin middles
	bin_mids = [O3_bands[i] + (O3_bands[i+1] - O3_bands[i])/2 for i in range(len(O3_bands) - 1)]
	
	#axis to plot bin mids vs PC1
	ax2.plot(bin_mids, pc1, color = 'b', alpha = 0.6)
	ax2.set_xlabel('ASO 10-20hPa O$_3$ Mole Fraction (ppm)')
	ax2.set_ylabel('1st pc (scaled)', color = 'b')
	ax2.tick_params(axis = 'y', labelcolor = 'b')
	
	##add rates in bands for comparison
	ax3 = ax2.twinx()
	ax3.errorbar(bin_mids, rates, yerr = np.transpose(Er), color = 'orange', alpha = 0.6)
	corr = round(np.corrcoef(rates,pc1)[0,1], 3)
	plt.title('r = ' + str(corr))
	ax3.set_ylabel('SSW_rate', color = 'orange')
	ax3.tick_params(axis = 'y', labelcolor = 'orange')
	
	return

## functions to add bar SSW count axes
def bar_axis(rate, Er, c, bar_width, i):
	warm1 = ax.bar(i, rate, bar_width, yerr=Er,  capsize = 7, ecolor = 'black', color = c, linewidth = 2.0)
	return

def bar_axis_month(rate_monthly, Er, c, bar_width, index):
	warm1 = ax.bar(index, rate_monthly, bar_width, yerr=Er,  capsize = 7, ecolor = 'black', color = c, linewidth = 2.0)
	return

def add_power_axis(spec, freq, P, title):
	plt.contourf(1/freq[1:], P, spec[:,1:], cmap = 'summer')
	plt.xlim(3,48)
	plt1.set_yscale('log', basey=10, subsy=None)
	plt1.set_xscale('log', basex = 6, subsx=None)
	plt1.set_xticks([6,12,18,24,36])
	plt1.set_xticklabels(['6','12','18','24','36'])
	plt1.set_ylim(0.05,100)
	plt1.invert_yaxis()
	plt.title(title)
	plt.ylabel('Pressure (hPa)')
	plt.xlabel('Period (months)')	
	
	return

def add_SAO_axis(SAO, P, title):
	cs = plt1.contourf(np.arange(12), P, np.transpose(SAO.data), lev, plt1, cmap = 'RdBu')
	plt.xlim(0,11)
	plt.colorbar(cs)
	plt1.contour(np.arange(12), P, np.transpose(SAO.data),[0], cmap = 'RdBu')

	plt1.set_yscale('log', basey=10, subsy=None)
	#plt1.set_xticks([6,12,18,24,36])
	#plt1.set_xticklabels(['6','12','18','24','36'])
	plt1.set_ylim(0.05,100)
	plt1.invert_yaxis()
	plt.title(title)
	plt.ylabel('Pressure (hPa)')
	
	return



