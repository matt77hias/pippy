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
    return bias

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
    _vis_bias(bias=calculate_bias(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)

def _vis_bias(bias, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    plt.semilogx(nb_samples, bias, ls='-', marker='.', color='g', label='f')
    plt.title('Bias')
    plt.ylabel('# samples')
    plt.xlabel('# bias')

def vis_MSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    _vis_MSE(MSE=calculate_MSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)

def _vis_MSE(MSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    plt.loglog(nb_samples, MSE, ls='-', marker='.', color='g', label='f')
    plt.loglog(nb_samples, np.power(nb_samples, -1.0), ls='-', color='b', label='Reference')
    plt.title('Mean Square Errors')
    plt.xlabel('# samples')
    plt.ylabel('MSE')
    
def vis_RMSE(f, mean=None, nb_runs=DEFAULT_NB_RUNS, nb_samples=DEFAULT_NB_SAMPLES):
    _vis_RMSE(RMSE=calculate_RMSE(f=f, mean=mean, nb_runs=nb_runs, nb_samples=nb_samples), nb_samples=nb_samples)
    
def _vis_RMSE(RMSE, nb_samples=DEFAULT_NB_SAMPLES):
    plt.figure()
    plt.loglog(nb_samples, RMSE, ls='-', marker='.', color='g', label='f')
    plt.loglog(nb_samples, np.power(nb_samples, -0.5), ls='-', color='b', label='Reference')
    plt.title('Root Mean Square Errors')
    plt.xlabel('# samples')
    plt.ylabel('RMSE')