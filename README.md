# CMIP6
CMIP6 repository contains various python scripts that cleans and processes data from a suite of climate models submitted to the [6th Coupled Model Intercomparison Project](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) (CMIP6). These scripts clean and wrangle raw input data from a suite of models and define classes whose instances contain key cliamte indices output by each model. Also included is a set of sample output figure produced by scripts in this repository which compares model performance across the project. 

# Files
rundown of scripts:

SSW_class.py - definition of an SSW class. [Sudden Stratospheric Warming](https://www.atmos.colostate.edu/~davet/ao/ThompsonPapers/LimpasuvanThompsonHartmann.pdf) events are key climate indicators for polar vortex strength and interannual cliamte variability in a model. Instances of this class contain SSW rates, SSW timeseries, SSW temporal distribution for a given model.

SSW_dif_sig_tests.py - a set of significance testing methods to compare SSW instances for a number of models.

O3_class.py - definiton of an ozone (O3) class whose instances contain indices tracking ozone representation in a given model. These include seasonal cycles of ozone mole fraction, response of ozone to winds and equatorial ozone variability. 

equator_class.py, mean_state_class.py - definiton of a two classes which contain temperature and wind metrics from the equatorial region and mean state variables for each model.

initialise_all.py - script which loads data from all models, cleans data where necessary and initialises instances of classes defined above. N.B. to run this initialisation, user must have required CMIP6 data only available to those with [ESGF](https://esgf-node.llnl.gov/search/cmip6/) credentials. 

plotting_routines.py - set of plotting functions

# Sample Outputs

SSWs_CMIP6_ALL_models.png - Comparison of mean SSW rates from each model





