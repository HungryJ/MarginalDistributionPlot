import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import kurtosis, skew

def mdp(data_object, summary_stat='mean', variable_choice = 'equally_spaced', label = None):
	'''
	Plot marginal distribution plot which is a distribution of summary statistic of each variabel
	and distribution of 15 variables

	Parameters
	data_object : 2D numpy array or pandas dataframe.
		Rows have to be variables and columns have to be objects.
	summary_stat : Summary statistic to use for representing each variable
		Should be either one of ['mean', 'median', 'std', 'skewness', 'kurtosis', 'unique_obs'] 
		or a fuction that takes a vector as input at return a scalar.  
	variable_choice : How to choose 15 variable to be plotted.
		Should be either one of ['equally_spaced', 'min', 'max'] or an length 15 array 
		which is consist of variable indices 
	label : label of each observation to use for color code 
	'''

	# Check if input Data is 2D numpy array or pandas dataframe
	if isinstance(data_object,pd.DataFrame):
		_isname = True
		_obs_names = data_object.columns.values
		_var_names = data_object.index.values
		data_object = np.array(data_object)
		_n_var = data_object.shape[0]
		_n_obs = data_object.shape[1]
	elif isinstance(data_object, np.ndarray):
		_isname = False
		_n_var = data_object.shape[0]
		_n_obs = data_object.shape[1]
		_obs_names = np.arange(1,_n_obs+1)
		_var_names = np.arange(1,_n_var+1)
	else: raise ValueError('Input object should be either 2 dimensional array or dataframe')
	
	if len(data_object.shape)!=2: raise ValueError('Input object should be either 2 dimensional array or dataframe')
	
	# get summary statistic for each variable
	if isinstance(summary_stat, str):
		statistic_wrapper = get_statistic_wrapper()
		if summary_stat in statistic_wrapper.keys():
			statistic = statistic_wrapper[summary_stat](data_object)
		else: raise ValueError('Should be either one of [mean, median, std, skewness, kurtosis, unique_obs] or a function that returns a vector of length same as the number of variables')
	
	else : statistic = summary_stat(data_object)

	if len(statistic) != data_object.shape[0]: raise ValueError('Should be either one of [mean, median, std, skewness, kurtosis, unique_obs] or a function that returns a vector of length same as the number of variables')

	# decide which 15 variables to show in marginal distribution plot
	if isinstance(variable_choice, str):
		variable_wrapper = get_variable_wrapper(_n_var)
		if variable_choice in variable_wrapper.keys():
			_slice = variable_wrapper[variable_choice]
		else: raise ValueError('_slice has to be either one of [equally_spaced, min, max] or an array of length 15')
	else : 
		_slice = variable_choice
		if len(_slice) != 15: raise ValueError('_slice has to be either one of [equally_spaced, min, max] or an array of length 15')
	
	_rep_indices = np.argsort(statistic)[_slice] 

	f, axes = plt.subplots(4,4, figsize=(15,12))
	plt.subplots_adjust(wspace=0.4, hspace=0.4)
	axes[0,0].plot(np.sort(statistic), linewidth=2)
	axes[0,0].vlines(_slice, min(statistic), max(statistic), linestyle='dashed', linewidth=1.3)
	axes[0,0].set_title("Summary Statistic: "+summary_stat)
	axes[0,0].set_xlabel("Sorted Variable index")
	for i, ax in enumerate(axes.flatten()[1:]):
	    _data = data_object[_rep_indices[i],:]
	    bw = (max(_data)-min(_data))/20
	    sns.kdeplot(_data, kernel='gau', bw=bw, color='gray', ax=ax)
	    if label is not None:
	        _n_label = len(np.unique(label))
	        for j in range(len(np.unique(label))):
	            kde = sm.nonparametric.KDEUnivariate(_data[label==np.unique(label)[j]].astype('double'))
	            kde.fit(bw=bw)
	            prop = sum(label==np.unique(label)[j])/_n_obs
	            sns.lineplot(kde.support, prop*kde.density, ax=ax)
	    ax.set_xlabel("Variable "+str(_var_names[_rep_indices[i]]))
	    ax.set_title(summary_stat+" : "+str(statistic[_rep_indices[i]].astype('float16')))
	    ymin, ymax = ax.get_ylim()
	    h = ymax-ymin
	    if label is not None:
	        sns.scatterplot(_data, h/2+np.random.uniform(-h/10,h/10,size=(_n_obs,)), s=10, hue=label, ax=ax)
	        if i!=0 : ax.legend().set_visible(False)
	    else :
	        sns.scatterplot(_data, h/2+np.random.uniform(-h/10,h/10,size=(_n_obs,)), s=10, ax=ax)

def get_statistic_wrapper():
	statistic_wrapper = {}
	statistic_wrapper['mean'] = lambda x: np.mean(x,axis=1)
	statistic_wrapper['std'] = lambda x : np.std(x,axis=1)
	statistic_wrapper['median'] = lambda x : np.median(x,axis=1)
	statistic_wrapper['zero_obs'] = lambda x : np.sum(x==0,axis=1)
	statistic_wrapper['unique_obs'] = lambda feat : np.apply_along_axis(lambda x: len(np.unique(x)), axis=1, arr=feat)
	statistic_wrapper['skewness'] = lambda x : skew(x, axis=1)
	statistic_wrapper['kurtosis'] = lambda x : kurtosis(x, axis=1)
	return statistic_wrapper

def get_variable_wrapper(_n_var):
	variable_wrapper = {}
	variable_wrapper['equally_spaced'] = np.rint((np.arange(1,16))*_n_var/16).astype('int')
	variable_wrapper['min'] = np.arange(15)
	variable_wrapper['max'] = np.arange(_n_var-1, _n_var-16, -1)
	return variable_wrapper