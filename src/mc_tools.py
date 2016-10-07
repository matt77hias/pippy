import matplotlib.pyplot as plt
import numpy as np

###################################################################################################################################################################################
## Configuration
################################################################################################################################################################################### 
class Configuration(object):
    
    def __init__(self, nb_merges=100, nb_experiments=10, nb_runs=1000, nb_samples=[2**i for i in range(1, 16)]):
        # Number of merges for bootstrapping
        self.nb_merges = nb_merges
        # Number of experiments to obtain one _beta_ estimator
        # _beta_ distribution available
        self.nb_experiments = nb_experiments
        # Number of runs to obtain one estimator _beta_ of the MSE/RMSE of one estimator _alpha_
        # _alpha_ distribution available
        self.nb_runs = nb_runs
        # Number of samples to obtain one estimator _alpha_
        self.nb_samples = nb_samples
        
###################################################################################################################################################################################
## Sequential calculation of characteristic values
################################################################################################################################################################################### 
def calculate_bias(f, mean, config=Configuration()):
    size = len(config.nb_samples)
    bias = np.zeros((size))
    for i in range(size):
        samples = np.array([f(config.nb_samples[i]) for run in range(config.nb_runs)])
        bias[i] = (np.mean(samples) - mean) / mean #relative bias
    return bias

def calculate_MSE(f, config=Configuration()):
    size = len(config.nb_samples)
    MSE = np.zeros((size))
    for i in range(size):
        samples = np.array([f(config.nb_samples[i]) for run in range(config.nb_runs)])
        MSE[i] = np.var(samples, ddof=1)
    return MSE

def calculate_RMSE(f, config=Configuration()):
    size = len(config.nb_samples)
    RMSE = np.zeros((size))
    for i in range(size):
        samples = np.array([f(config.nb_samples[i]) for run in range(config.nb_runs)])
        RMSE[i] = np.std(samples, ddof=1)
    return RMSE
   
###################################################################################################################################################################################
## Parallel calculation of characteristic values
###################################################################################################################################################################################  
from global_configuration import nb_cpus
from multiprocessing.pool import ThreadPool as Pool

def calculate(f, config=Configuration()):
    pool = Pool(nb_cpus())
    result = np.array(pool.map(f, range(config.nb_experiments)))
    pool.close()
    pool.join() 
    return result
    
###################################################################################################################################################################################
## Bootstrap sampling
################################################################################################################################################################################### 
def bootstrap_coefficients(data, config=Configuration()):
    # nb_experiments x len(nb_samples) -> len(nb_samples) x nb_experiments
    tdata = np.transpose(data)

    w = 1.0 / np.std( data, axis=0, ddof=1)

    log_nb_samples = np.log2(config.nb_samples)
    coefficients = np.zeros((config.nb_merges, 2))
    for i in range(config.nb_merges):
        values = tdata[[\
                        np.arange(len(config.nb_samples)), \
                        np.random.randint(size=(len(config.nb_samples)), low=0, high=config.nb_experiments)]]
        log_values = np.log2(values)
        coefficients[i] = np.polyfit(log_nb_samples, log_values, 1, w=w)
    
    # coefficients 
    return np.std(coefficients, axis=0, ddof=1)
 
###################################################################################################################################################################################
## Visualization of characteristic values
###################################################################################################################################################################################
def vis_bias(f, mean, config=Configuration()):
    # nb_experiments x len(nb_samples)
    biass = calculate(f=lambda x: calculate_bias(f=f, mean=mean, config=config), config=config)
    
    # Visualization
    _vis_bias(name=f.__name__, biass=biass, config=config)

def vis_MSE(f, config=Configuration()):
    # nb_experiments x len(nb_samples)
    MSEs = calculate(f=lambda x: calculate_MSE(f=f, config=config), config=config)
    
    # Bootstrapping coefficients
    coefficients_std = bootstrap_coefficients(MSEs, config=config)
    print('MSE slope std:\t\t' + str(coefficients_std[0]))
    print('MSE intercept std:\t' + str(coefficients_std[1]))
    
    # Visualization
    _vis_MSE(name=f.__name__, MSEs=MSEs, config=config)

def vis_RMSE(f, config=Configuration()):
    # nb_experiments x len(nb_samples)
    RMSEs = calculate(f=lambda x: calculate_RMSE(f=f, config=config), config=config)
    
    # Bootstrapping coefficients
    coefficients_std = bootstrap_coefficients(RMSEs, config=config)
    print('RMSE slope std:\t\t' + str(coefficients_std[0]))
    print('RMSE intercept std:\t' + str(coefficients_std[1]))
    
    # Visualization
    _vis_RMSE(name=f.__name__, RMSEs=RMSEs, config=config)

def _vis_bias(name, biass, config=Configuration()):
    plt.figure()
    
    # MC data
    biass_mean = np.mean(biass, axis=0)
    biass_std  = np.std( biass, axis=0, ddof=1)
    plt.errorbar(config.nb_samples, biass_mean, yerr=biass_std, ls='None', marker='o', color='g', label=name)
    
    plt.title('Bias')
    plt.xscale('log')
    plt.xlabel('# samples')
    plt.ylabel('# bias')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('bias_' + name + '.png', bbox_inches='tight')

def _vis_MSE(name, MSEs, config=Configuration()):
    plt.figure()
    
    # MC data
    MSEs_mean = np.mean(MSEs, axis=0)
    MSEs_std  = np.std( MSEs, axis=0, ddof=1)
    plt.errorbar(config.nb_samples, MSEs_mean, yerr=MSEs_std, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.plot(config.nb_samples, np.power(config.nb_samples, -1.5), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    w = 1.0 / MSEs_std
    log_nb_samples = np.log2(config.nb_samples)
    log_MSEs_mean = np.log2(MSEs_mean)
    fitted_coefficients = np.polyfit(log_nb_samples, log_MSEs_mean, 1, w=w)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.plot(config.nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Mean Square Errors [slope={0:0.4f}]'.format(fitted_coefficients[0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('# samples')
    plt.ylabel('MSE')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('MSE_' + name + '.png', bbox_inches='tight')
  
def _vis_RMSE(name, RMSEs, config=Configuration()):
    plt.figure()
    
    # MC data
    RMSEs_mean = np.mean(RMSEs, axis=0)
    RMSEs_std  = np.std( RMSEs, axis=0, ddof=1)
    plt.errorbar(config.nb_samples, RMSEs_mean, yerr=RMSEs_std, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.plot(config.nb_samples, np.power(config.nb_samples, -0.5), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    w = 1.0 / RMSEs_std
    log_nb_samples = np.log2(config.nb_samples)
    log_RMSEs_mean = np.log2(RMSEs_mean)
    fitted_coefficients = np.polyfit(log_nb_samples, log_RMSEs_mean, 1, w=w)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.plot(config.nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Root Mean Square Errors [slope={0:0.4f}]'.format(fitted_coefficients[0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('# samples')
    plt.ylabel('RMSE')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('RMSE_' + name + '.png', bbox_inches='tight')