import matplotlib.pyplot as plt
import numpy as np

DEFAULT_NB_EXPERIMENTS = 10
DEFAULT_NB_RUNS = 1000
DEFAULT_NB_SAMPLES = [2**i for i in range(1, 16)]

###################################################################################################################################################################################
## Characteristic Values
################################################################################################################################################################################### 
def calculate_bias(f, mean, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    size = len(nb_samples)
    bias = np.zeros((size))
    for i in range(size):
        samples = np.array([f(nb_samples[i]) for run in range(nb_runs)])
        bias[i] = np.mean(samples) - mean
    return bias / mean #relative bias

def calculate_MSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    size = len(nb_samples)
    MSE = np.zeros((size))
    for i in range(size):
        samples = np.array([f(nb_samples[i]) for run in range(nb_runs)])
        if mean is None:
            MSE[i] = np.var(np.abs(samples - np.mean(samples)), ddof=1)
        else:
            MSE[i] = np.var(np.abs(samples - mean), ddof=0)
    return MSE

def calculate_RMSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    size = len(nb_samples)
    RMSE = np.zeros((size))
    for i in range(size):
        samples = np.array([f(nb_samples[i]) for run in range(nb_runs)])
        if mean is None:
            RMSE[i] = np.std(np.abs(samples - np.mean(samples)), ddof=1)
        else:
            RMSE[i] = np.std(np.abs(samples - mean), ddof=0)
    return RMSE
    
###################################################################################################################################################################################
## Visualization of Characteristic Values
###################################################################################################################################################################################
from global_configuration import nb_cpus
from multiprocessing.pool import ThreadPool

def _task(f, nb_experiments=DEFAULT_NB_EXPERIMENTS):
    pool = ThreadPool(processes=nb_cpus())
    result = np.array(pool.map(f, range(nb_experiments)))
    pool.close()
    pool.join() 
    return result

def vis_bias(f, mean, nb_experiments=DEFAULT_NB_EXPERIMENTS, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    bias = _task(lambda x: calculate_bias(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_experiments=nb_experiments)
    _vis_bias(f.__name__, bias=bias, nb_samples=nb_samples)

def _vis_bias(name, bias, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    bias_mean = np.mean(bias, axis=0)
    bias_std = np.std(bias, axis=0, ddof=1)
    plt.errorbar(nb_samples, bias_mean, yerr=bias_std, ls='None', marker='o', color='g', label=name)
    
    plt.title('Bias')
    plt.xscale('log')
    plt.xlabel('# samples')
    plt.ylabel('# bias')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('bias_' + name + '.png', bbox_inches='tight')

def vis_MSE(f, mean=None, nb_experiments=DEFAULT_NB_EXPERIMENTS, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    MSE = _task(lambda x: calculate_MSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_experiments=nb_experiments)
    _vis_MSE(f.__name__, MSE=MSE, nb_samples=nb_samples)

def _vis_MSE(name, MSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    # MC data
    MSE_mean = np.mean(MSE, axis=0)
    MSE_std = np.std(MSE, axis=0, ddof=1)
    plt.errorbar(nb_samples, MSE_mean, yerr=MSE_std, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.plot(nb_samples, np.power(nb_samples, -1.0), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    log_nb_samples = np.log2(nb_samples)
    log_MSE_mean = np.log2(MSE_mean)
    fitted_coefficients = np.polyfit(log_nb_samples, log_MSE_mean, 1)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.plot(nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Mean Square Errors [rico={0:0.4f}]'.format(fitted_coefficients[0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('# samples')
    plt.ylabel('MSE')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('MSE_' + name + '.png', bbox_inches='tight')
    
def vis_RMSE(f, mean=None, nb_experiments=DEFAULT_NB_EXPERIMENTS, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    RMSE = _task(lambda x: calculate_RMSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_experiments=nb_experiments)
    _vis_RMSE(f.__name__, RMSE=RMSE, nb_samples=nb_samples)
    
def _vis_RMSE(name, RMSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    # MC data
    RMSE_mean = np.mean(RMSE, axis=0)
    RMSE_std = np.std(RMSE, axis=0, ddof=1)
    plt.errorbar(nb_samples, RMSE_mean, yerr=RMSE_std, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.plot(nb_samples, np.power(nb_samples, -0.5), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    log_nb_samples = np.log2(nb_samples)
    log_RMSE_mean = np.log2(RMSE_mean)
    fitted_coefficients = np.polyfit(log_nb_samples, log_RMSE_mean, 1)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.plot(nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Root Mean Square Errors [rico={0:0.4f}]'.format(fitted_coefficients[0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('# samples')
    plt.ylabel('RMSE')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('RMSE_' + name + '.png', bbox_inches='tight')