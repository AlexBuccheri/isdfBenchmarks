---
title: "Results on Molecular Systems Using Density-Fitting in Octopus"
author: "Alexander Buccheri"
date: "September 2025"
geometry: margin=1in
papersize: a4
numbersections: true
---

## Target Error, and Corresponding Molecular Speed-Up

Figures 1 and 2 show a speed-up ranging from $\sim 2-5$ times Octopus's reference ACE implementation, depending on the
number of ISDF (density fitting) vectors used, which varies inversely with the precision of the exact exchange energy
required.

![**Figure 1.** Average SCF time for all molecules (given in terms of their occupied states), for several choices for the number of interpolation vectors.](images/avg_scf_time.png){ width=75% }

![**Figure 2.** Speed-up in average SCF time as a function of the number of interpolation vectors.](images/speedup_barplot.png){ width=75% }

The error associated with each calculation is shown in figure 3.

![**Figure 3.** Error in exact exchange energy per atom, as a function of the number of ISDF vectors used for the calculation, for the four molecules profiled. The black line corresponds to the desired level of precision as defined in [1].](images/exx_error.png){ width=75% }

Rettiig et. al. (Head-Gordon group) [[1]](https://pubs.acs.org/doi/full/10.1021/acs.jctc.3c00407) quote an error of
$10^{-6}$ (Ha/atom) as an acceptable precision in the exact exchange energy (EXX), which is comparable to what one
achieves with other density-fitting methods. They also note that for range-separated hybrids where one uses a percentage
of exact exchange, one may be able to get away with a higher error.

For the current Octopus molecular implementation to achieve the same precision on the systems I've tested (some not
included here), we need a pre-factor ($c$) of 10–12. This currently only corresponds to a speed-up on the
reference implementation of $\sim 2.5 - 3$ for the molecules shown here. If we go to larger molecular systems
(w.r.t number of occupied states), this speed-up improves.

If we compare to the data in _table 1_ of [[2]](https://pubs.acs.org/doi/full/10.1021/acs.jctc.7b01113) (Lin Lin) they
also reach an error $\sim 10^{-6}$ Ha/atom for a pre-factor of 12.0 for semiconducting $Si_{216}$ and metallic
$Al_{176}Si_{24}$. Furthermore, they assert that a moderate choice of the rank parameter is as low as $c = 6.0$, leading
to an error of the energy per atom below the chemical accuracy of 1 kcal/mol ($1.6 \times 10^{-3}$ Ha/atom), and the error
of the force is around $10^{-3}$ Ha/Bohr.

Figure 4 shows the timing breakdown of an Octopus run using the density fitting:

![**Figure 4.** Octopus subroutine profiling for an ISDF run on the ether crown.](images/isdf_profiling_ethercrown.png){ width=75% }

If one looks at figure 4, the majority of calculation time comes from `ISDF_ACE_APPLY_EXCHANGE_OP`, which itself calls
`ISDF_POTENTIAL` (this is true for all calculations). This routine is essentially a loop over Poisson calls; i.e.
the main cost of the algorithm is just solving the Poisson equation for each interpolation vector. There are three clear
implications from this:

1. For molecular systems, one needs to go to a larger number of occupied states to see meaningful speed-ups, where
   $N_{e}^2 \gg 12N_{occ}$. This is referenced by Rettiig et. al. (Head-Gordon) [[1]](https://pubs.acs.org/doi/full/10.1021/acs.jctc.3c00407),
   where they state, "molecular THC was seen to require too many interpolation points to be computationally competitive
   except for very large systems". Looking at this in context with reference [[2]](https://pubs.acs.org/doi/full/10.1021/acs.jctc.7b01113),
   I don't think one should be too surprised at the Octopus molecular results. It indicates everything's working, and
   the code developed for this can be added to (rather than substantially modified) to extend to periodic systems.

2. If one can choose a more optimal set of interpolation points, the same precision could be obtained with fewer
   vectors.

3. Anything one can do to improve the efficiency of our Poisson solver will yield the largest gains—in all
   implementations.

For point 2, I can definitely optimise how I choose interpolation points.
The `KMeans ||` [[3]](https://www.vldb.org/pvldb/vol5/p622_bahmanbahmani_vldb2012.pdf)
and `KMeans++` [[4]](https://proceedings.mlr.press/v97/lattanzi19a.html)
algorithms provide more robust seeding and optimisation of interpolation points, respectively. And I can improve my
convergence criterion, such that points don't "jiggle" between assignments. This could reduce the number of points by
10–20% required for a given precision.

For point 3, as already discussed, we could definitely implement batching of calling the Poisson solver. This could
speed up the FFTs by 2× on CPU (and more on GPU). We could also implement Kresse's FFT cutoff.

Additionally, in _figure 1_, shown above, the increase in time w.r.t. $N_{isdf}$ vectors is not quite linear. I assume this is because of
the communication overhead of transferring the vectors. I should be able to reduce this by refactoring to minimise MPI communications.
This and point 2 get up to $\ge \sim 4\times$ speed-up for molecular systems containing $\ge 60$ occupied states.

### What to Expect from the Periodic Implementation

To achieve $10^{-6}$ precision in the EXX with Rettiig et. al.'s periodic THC-oo-K algorithm (what we will also implement) one
typically needs a pre-factor $\sim 70$ for periodic systems, as shown in figure 1(c)
of [1](https://pubs.acs.org/doi/full/10.1021/acs.jctc.3c00407). In general, they find fewer interpolation
vectors are required for molecules than periodic systems. For a benzene molecule, they use $c=20$, and typically find 25
points is sufficient for all basis sets other than the smallest
[[5]](https://pubs.acs.org/doi/full/10.1021/acs.jctc.9b00820). 

Rettiig et. al. note that for periodic systems their "algorithms rely on the fact that the number of ISDF points
required to yield an accurate solution will plateau quickly with the k-mesh size", and show that the THC-oo-K algorithm
becomes the more efficient than their prior algorithms for a k-grid of $(5,5,5)$. In general in the ISDF approximation,
it is clear that for periodic systems, one can reduce scaling from $N_k^2$ to $N_k$, but due to the associated pre-factors
this is only more efficient for moderate k-grids and above.

### Next Steps  

What I intend to do next is:

 * Optimise the selection of the interpolation points, as this algorithm is identical for molecular and periodic systems, and should improve stability.

 * Benchmark the molecular code in TD, where it's an open question as to how one can/should treat the interpolation points as a function of time.
    * For example, reference [2](https://pubs.acs.org/doi/full/10.1021/acs.jctc.7b01113) perform ab-initio MD on $Si_{64}$. They re-compute the interpolation points at each ionic step, and find that their energy drift per atom is $\sim 10^{-5}$ Ha/ps (they run for 1000 time steps using a 1 fs time step). This is about an order of magnitude larger than the drift in the reference calculation.

 * Then I'll move on to extend the existing code to handle k-points.

Efforts that could be done in parallel include:

* Batching of Poisson solver.
  * Henri looking at this
* Implementation of Kresse's FFT speed-ups.
  * I would be happy to look at this—the existing hybrid implementation could also immediately benefit from this.
* Porting of density-fitting code to GPU.
  * I started to look at this, but Nic has suggested it is lower priority. Alternatively I could work with Alessandro
    at MPCDF, who is a GPU expert.
