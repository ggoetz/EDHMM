from emission_new import Gaussian
from duration_new import Poisson
from transition_new import Transition
from initial import Initial
from edhmm import EDHMM

import pylab as pb
import numpy as np
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    #filename="EDHMM.log", 
    #filemode="w",
    level=logging.DEBUG
)

A = Transition(
    K=3,
    A=pb.array([[0, 0.3, 0.7], [0.6, 0, 0.4], [0.3, 0.7, 0]])
)
O = Gaussian(
    nu = 1,
    Lambda = np.array([1]), 
    mu_0 = [0, 0, 0], 
    kappa = 0.01, 
    mu = [-4, 0, 4], 
    tau = [
        np.array([[1]]),
        np.array([[1]]),
        np.array([[1]])
    ]
)

D = Poisson(
    mu = [5,15,30], 
    alpha=[1, 1, 1],
    beta=[0.0001, 0.0001, 0.0001],
    support_step = 20
)
pi = Initial(K=3,beta=0.001)
m = EDHMM(A,O,D,pi)

T = 500

X,Y,Dseq = m.sim(T)

Z = zip(X,Dseq)
L_prior = m.loglikelihood([Z], [Y])
print L_prior

np.save("X.npy", X)
np.save("D.npy", Dseq)
np.save("Y.npy", Y)
np.save("Z.npy", zip(X,Dseq))

if True:
    
    m.A.A = pb.array(
       [[0, 0.5, 0.5], 
        [0.5, 0, 0.5], 
        [0.5, 0.5, 0]]
    )
    m.O.mu = [-1,0,1]
    m.D.mu = [1,1,1]
    
    As, O_means, O_precisions, D_mus, Zs, L = m.beam(
        [Y], min_u = 0, its=1000, burnin=500, name="test", online=True, sample_U=True
    )
    np.save("As",As)
    np.save("O_m", O_means)
    np.save("O_p", O_precisions)
    np.save("D_mus", D_mus)
    np.save("Zs", Zs)
    np.save("L", L)


pb.figure()
pb.plot(L)
pb.plot([L_prior for l in L],'r')
pb.savefig("L.pdf")
pb.figure()
for i in range(3):
    pb.hist(D_mus[:,i], alpha=0.5)
pb.savefig("D_mus.pdf")
