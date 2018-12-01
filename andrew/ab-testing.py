from scipy import stats
import numpy as np

def get_pdf(x_range, store_data):
    ''' The function will return the pdf for a given beta distribution.
    
    Args:
        x_range: Array of x values for the plot.
        store_data: Array of values for a store. A value of 1 represents a positive customer
                    result while an value of 0 represents a negative result. 
                    
    Returns:
        A numpy array representing the PDF for the given beta distribution.
    '''
    alpha = sum(store_data)
    beta = len(store_data) - alpha
    return stats.beta(a=alpha, b=beta).pdf(x_range)