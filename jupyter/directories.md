# List of Directories

## Molecular ACE and ISDF Runs

To create space, I scrapped the restart folder for each run with:
`find . -type d -name restart -execdir rm -rf {} +`

### Filed
* pbe_reference: 
	* Ran the biggest systems with PBE, just to get a feel for convergence
* ace_references:
	* ACE references
	* Some were run previously, and if I want to compare to them, should be re-run:
	* 60_buckminster, 73_chlorophyll, 84_c84
* nisdf_vector_scaling
	* Several molecular systems, computed with differing numbers of ISDF points/vectors


### To File:
* n_interpolation_points
* isdf
	* Prior to distributing ISDF vectors in the Poisson call
	* The main profiling results should be copied across, then scrap this folder
* ~~repeat_reference_ace
	* Deleted
* compare_anthracene
* mpi_isdf
  * Used this for kmeans
* lower_p_isdf
* single_kmeans_isdf
