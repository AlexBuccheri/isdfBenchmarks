import numpy as np

from isdfbenchmarks.parser.stdout import parse_scf_time, parse_kmeans_iterations


def test_parse_scf_time():

    substr = """
Density of states:

-----------------------------------------------------------------%----
-----------------------------------------------------------------%----
-----------------------------------------------------------------%----
-----------------------------------------------------------------%----
-----------------------------------------------------------------%----
-------------------------%----%--%-----%-%---------------------%-%%---
-------------------------%----%--%-----%-%---------------------%-%%---
%-%---%%-%%--%---%-%%%---%-%-%%%%%%%%%%%-%--%%--%-------------%%%%%-%%
%-%---%%-%%--%---%-%%%---%-%-%%%%%%%%%%%-%--%%--%-------------%%%%%-%%
%-%---%%-%%--%---%-%%%---%-%-%%%%%%%%%%%-%--%%--%-------------%%%%%-%%
                                                ^


Elapsed time for SCF step    17:         87.48
**********************************************************************

Info: Performing weighted KMeans
Kmeans converged in   26 iterations

*********************** SCF CYCLE ITER #   18 ************************
 etot  = -9.12107128E+01 abs_ev   =  1.71E-04 rel_ev   =  5.13E-06
 ediff =        2.34E-04 abs_dens =  2.94E-04 rel_dens =  4.46E-06
Matrix vector products:     25
Converged eigenvectors:      0

Elapsed time for SCF step    18:         89.13
    """
    scf_times = parse_scf_time(substr)
    itr = list(scf_times)
    times = [t for t in scf_times.values()]
    assert np.array_equal(itr, [17, 18])
    assert np.array_equal(times, [87.48, 89.13])


def test_parse_kmeans_iterations():

    substr = """
*********************** SCF CYCLE ITER #    1 ************************

Elapsed time for SCF step     1:        117.25
**********************************************************************

Info: Performing weighted KMeans
Kmeans converged in   63 iterations

*********************** SCF CYCLE ITER #    2 ************************
 etot  = -9.81055652E+01 abs_ev   =  4.00E+00 rel_ev   =  9.85E-02
 ediff =        1.44E+00 abs_dens =  9.93E-01 rel_dens =  1.51E-02
Matrix vector products:     25
Converged eigenvectors:      0

Elapsed time for SCF step     2:         95.66
**********************************************************************

Info: Performing weighted KMeans
Kmeans converged in   45 iterations

*********************** SCF CYCLE ITER #    3 ************************
 etot  = -8.73830841E+01 abs_ev   =  1.12E+01 rel_ev   =  3.82E-01
2.000000   ( 1.4E-02)

**********************************************************************

Info: Performing weighted KMeans
Kmeans converged in   40 iterations
"""

    kmeans_itr = parse_kmeans_iterations(substr)
    assert kmeans_itr == {1: 63, 2: 45, 3: 40}




