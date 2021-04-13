import numpy as np
from lab2.tools2 import *

import matplotlib.pyplot as plt

def concatHMMs(hmmmodels, namelist):
    """ Concatenates HMM models in a left to right manner

    Args:
       hmmmodels: list of dictionaries with the following keys:
           name: phonetic or word symbol corresponding to the model
           startprob: M+1 array with priori probability of state
           transmat: (M+1)x(M+1) transition matrix
           means: MxD array of mean vectors
           covars: MxD array of variances
       namelist: list of model names that we want to concatenate

    D is the dimension of the feature vectors
    M is the number of states in each HMM model (could be different for each)

    Output
       combinedhmm: dictionary with the same keys as the input but
                    combined models

    Example:
       wordHMMs['o'] = concatHMMs(phoneHMMs, ['sil', 'ow', 'sil'])
    """

    final_startprob = hmmmodels[namelist[0]]['startprob'][:-1]

    single_num_states = hmmmodels[namelist[0]]['startprob'].shape[0]
    final_num_states = len(namelist) * (single_num_states - 1) + 1

    final_transmat = np.zeros((final_num_states, final_num_states))
    final_means = hmmmodels[namelist[0]]['means']
    final_covars = hmmmodels[namelist[0]]['covars']

    for i in range(0, len(namelist)):
        start = i * (single_num_states - 1)
        end = start + single_num_states
        final_transmat[start:end, start:end] = hmmmodels[namelist[i]]['transmat']

        if (i != 0):
            final_means = np.vstack((final_means, hmmmodels[namelist[i]]['means']))
            final_covars = np.vstack((final_covars, hmmmodels[namelist[i]]['covars']))
            final_startprob = np.concatenate((final_startprob, hmmmodels[namelist[i]]['startprob'][:-1]))

    # convert to log space
    final_startprob = np.log(final_startprob)
    final_transmat = np.log(final_transmat[:-1, :-1])

    combinedhmm = {'name': namelist, 'means': final_means, 'startprob': final_startprob, 'covars': final_covars,
                   'transmat': final_transmat}

    return combinedhmm


def gmmloglik(log_emlik, weights):
    """Log Likelihood for a GMM model based on Multivariate Normal Distribution.

    Args:
        log_emlik: array like, shape (N, K).
            contains the log likelihoods for each of N observations and
            each of K distributions
        weights:   weight vector for the K components in the mixture

    Output:
        gmmloglik: scalar, log likelihood of data given the GMM model.
    """

def forward(log_emlik, log_startprob, log_transmat):
    """Forward (alpha) probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: log transition probability from state i to j

    Output:
        forward_prob: NxM array of forward log probabilities for each of the M states in the model
    """

    # N frames, M states
    N, M = np.shape(log_emlik)

    forward_prob = np.zeros((N, M))

    log_alpha_0 = np.add(log_startprob, log_emlik[0, :])
    forward_prob[0, :] = log_alpha_0

    for timestep in range(1, N):
        for state in range(M):
            sum = np.add(forward_prob[timestep-1, :],
                         log_transmat[:, state])
            lse = logsumexp(sum)
            log_alpha = lse + log_emlik[timestep, state]

            forward_prob[timestep, state] = log_alpha

    return forward_prob

def backward(log_emlik, log_startprob, log_transmat):
    """Backward (beta) probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        backward_prob: NxM array of backward log probabilities for each of the M states in the model
    """
    num_states = log_transmat.shape[0]
    num_observations = log_emlik.shape[0]

    backward_prob = np.zeros((num_observations, num_states)) #initialize with zero

    for t in range(num_observations-2, -1, -1):
        for s in range(num_states):
            # compute sum
            sum_mat = log_transmat[s, :] + log_emlik[t+1, :] + backward_prob[t+1, :]
            backward_prob[t, s] = logsumexp(sum_mat)

    return backward_prob


def viterbi(log_emlik, log_startprob, log_transmat):
    """Viterbi path.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        viterbi_loglik: log likelihood of the best path
        viterbi_path: best path
    """
    num_states = log_transmat.shape[0]
    num_observations = log_emlik.shape[0]   #equal to number of frames
    path_matrix = np.zeros((num_states, num_observations))
    backpointer = np.zeros((num_states, num_observations)) #best previous path for each time step

    #initialization step
    for s in range(num_states-1): #forget about last state
        path_matrix[s, 0] = log_startprob[s] + log_emlik[0,s]
    #recursion step
    for t in range(1, num_observations):
       for s in range(num_states):
           v = path_matrix[:, t - 1] + log_transmat[:, s]
           best = np.argmax(v)
           path_matrix[s,t] = path_matrix[best,t-1] + log_transmat[best, s] + log_emlik[t, s]
           backpointer[s, t] = best

    backpointer[-1, -1] = np.argmax(path_matrix[s, num_observations-1] + log_transmat[best, -1])
    viterbi_loglik = np.max(path_matrix[:, -1])
    # backtracking
    backpointer = backpointer.astype(int)
    viterbi_path = np.zeros((num_observations))
    viterbi_path[0] = 0
    viterbi_path[-1] = int(np.argmax(path_matrix[:, -1]))

    for t in range(num_observations-2, -1, -1):
       best = backpointer[int(viterbi_path[t+1]), t+1]
       viterbi_path[t]= int(best)

    return {'loglik': viterbi_loglik, 'path': viterbi_path}


def statePosteriors(log_alpha, log_beta):
    """State posterior (gamma) probabilities in log domain.

    Args:
        log_alpha: NxM array of log forward (alpha) probabilities
        log_beta: NxM array of log backward (beta) probabilities
    where N is the number of frames, and M the number of states

    Output:
        log_gamma: NxM array of gamma probabilities for each of the M states in the model
    """
    log_alpha = np.where(np.isinf(log_alpha), 0, log_alpha)
    sum_alphas = np.sum(np.exp(log_alpha), axis=1)
    sum_alphas = np.reshape(sum_alphas, (sum_alphas.size, 1))
    log_gamma = log_alpha + log_beta - sum_alphas

    # test state probabilities in linear domain
   # a = np.abs(log_gamma).astype(np.float128)  # convert to float128 to avoid overflow in exp
   # linear_gamma = np.exp(a)
   # sum_prob = np.sum(linear_gamma, axis=1)
   # if (sum_prob.all() == 1):
   #     print('gammas sum to 1!')
   # else:
   #     print('gammas do not sum to 1!')

    return log_gamma


def updateMeanAndVar(X, log_gamma, varianceFloor=5.0):
    """ Update Gaussian parameters with diagonal covariance

    Args:
         X: NxD array of feature vectors
         log_gamma: NxM state posterior probabilities in log domain
         varianceFloor: minimum allowed variance scalar
    were N is the lenght of the observation sequence, D is the
    dimensionality of the feature vectors and M is the number of
    states in the model

    Outputs:
         means: MxD mean vectors for each state
         covars: MxD covariance (variance) vectors for each state
    """
    # number of mixtures equals to M (number of hmm states)
    num_mixtures = log_gamma.shape[1]
    feature_dim = X.shape[1]
    means = np.zeros((num_mixtures, feature_dim))
    covars = np.zeros((num_mixtures, feature_dim))

    for i in range(num_mixtures):
        gamma_sum = np.sum(log_gamma[:, i])
        means[i] = np.dot(log_gamma[:, i].T, X) / gamma_sum

        dif = np.power(X - means[i], 2)
        covars[i] = np.dot(log_gamma[:, i].T, dif) / gamma_sum

    # check if variance is larger that variancefloor
    covars = np.where(covars < varianceFloor, varianceFloor, covars)

    return {'mean': means, 'covar': covars}


