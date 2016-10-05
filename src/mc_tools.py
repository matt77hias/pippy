import matplotlib.pyplot as plt
import numpy as np

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
            MSE[i] = np.var(np.abs(samples - np.mean(samples)), ddof=0)
        else:
            MSE[i] = np.var(np.abs(samples - mean), ddof=1)
    return MSE

def calculate_RMSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    size = len(nb_samples)
    RMSE = np.zeros((size))
    for i in range(size):
        samples = np.array([f(nb_samples[i]) for run in range(nb_runs)])
        if mean is None:
            RMSE[i] = np.std(np.abs(samples - np.mean(samples)), ddof=0)
        else:
            RMSE[i] = np.std(np.abs(samples - mean), ddof=1)
    return RMSE
    
###################################################################################################################################################################################
## Visualization of Characteristic Values
###################################################################################################################################################################################
def vis_bias(f, mean, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    _vis_bias(f.__name__, bias=calculate_bias(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)

def _vis_bias(name, bias, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    plt.semilogx(nb_samples, bias, ls='None', marker='o', color='g', label=name)
    
    plt.title('Bias')
    plt.xlabel('# samples')
    plt.ylabel('# bias')
    plt.legend()

def vis_MSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    _vis_MSE(f.__name__, MSE=calculate_MSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)

def _vis_MSE(name, MSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    # MC data
    plt.loglog(nb_samples, MSE, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.loglog(nb_samples, np.power(nb_samples, -1.0), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    log_nb_samples = np.log2(nb_samples)
    log_MSE = np.log2(MSE)
    fitted_coefficients = np.polyfit(log_nb_samples, log_MSE, 1)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.loglog(nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Mean Square Errors [rico={0:0.2f}]'.format(fitted_coefficients[0]))
    plt.xlabel('# samples')
    plt.ylabel('MSE')
    plt.legend()
    
def vis_RMSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    _vis_RMSE(f.__name__, RMSE=calculate_RMSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)
    
def _vis_RMSE(name, RMSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    
    # MC data
    plt.loglog(nb_samples, RMSE, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial reference
    plt.loglog(nb_samples, np.power(nb_samples, -0.5), ls='-', color='b', label='ref')
    # 1 degree polynomial fit
    log_nb_samples = np.log2(nb_samples)
    log_RMSE = np.log2(RMSE)
    fitted_coefficients = np.polyfit(log_nb_samples, log_RMSE, 1)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_data = [2**fitted_polygon(s) for s in log_nb_samples]
    plt.loglog(nb_samples, fitted_data, ls='-', color='g', label='fit')
    
    plt.title('Root Mean Square Errors [rico={0:0.2f}]'.format(fitted_coefficients[0]))
    plt.xlabel('# samples')
    plt.ylabel('RMSE')
    plt.legend()