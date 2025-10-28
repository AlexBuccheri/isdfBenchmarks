""" Generate ISDF Inputs for KMeans Profiling
From the project root:  python jobs/kmeans_profiling.py
"""
from pathlib import Path

from isdfbenchmarks.molecule_set.molecular_inputs import isdf_base_inputs
from isdfbenchmarks.molecule_set.molecular_xyz import molecular_xyz_str
from isdfbenchmarks.submission.slurm import SlurmConfig, module_25b
from isdfbenchmarks.parser.inp_gen import basic_dict_to_inp


def kmeans(root: Path, molecules: list, slurm_base_settings: dict):
    """
    Create consistent inputs for a KMeans calculation
    """
    isdf_inputs = isdf_base_inputs()

    occupations = {'anthracene': 33,
                   'tetracene': 42,
                   'pentacene': 51,
                   'ether_crown': 54,
                   'chlorophyll': 114,
                   'buckminster': 120}

    print("Generating data in:")
    for molecule in molecules:
        # Make directory
        subdirectory = root / molecule
        print(subdirectory.as_posix())
        subdirectory.mkdir(parents=True, exist_ok=True)

        # Input file. Testing changes to the code, so very few additions to the base inp
        n_isdf = int(10 * occupations[molecule])
        inp_dict = isdf_inputs[molecule] | {"ISDFNpoints": str(n_isdf),
                                            "KMeansRepeatInterval": "1"}
        inpr_str = basic_dict_to_inp(inp_dict)
        with open(file=subdirectory / "inp", mode='w') as fid:
            fid.write(inpr_str)

        # Structure
        with open(file=subdirectory / "structure.xyz", mode='w') as fid:
            fid.write(molecular_xyz_str[molecule])

        # Slurm. Binary specific to this test
        slurm_settings = slurm_base_settings | {'job_name': f'{root.name}_{molecule}'}
        if molecule in {'chlorophyll', 'buckminster'}:
            slurm_settings['time'] = "24:00:00"
        cfg = SlurmConfig(**slurm_settings)
        with open(file=subdirectory / "slurm.sh", mode='w') as fid:
            fid.write(str(cfg))


def kmeans_calcs(root: Path, executable: str):
    """
    Replaced the
    In each case, the
    :return:
    """
    molecules = ['anthracene', 'tetracene', 'pentacene', 'ether_crown', 'buckminster', 'chlorophyll']
    # Fixed for consistent benchmarking
    slurm_base_settings = {'nodes': 1,
                           'ntasks_per_node': 4,
                           'cpus_per_task': 8,
                           'executable': executable,
                           'pre_script': module_25b}
    kmeans(root, molecules, slurm_base_settings)


if __name__ == '__main__':
    # Reference
    # kmeans_calcs(Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeans_ref'),
    #              "/home/bucchera/programs/octopus/cmake-build-foss-full-mpi-release/octopus")

    # L2 Norm
    # kmeans_calcs(Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeans_l2'),
    #              "/home/bucchera/programs/octopus/l2_norm/octopus")

    # L2 norm + initial centroids with k-means++
    kmeans_calcs(Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeans_plus_plus'),
                 "/home/bucchera/programs/octopus/l2_norm/octopus")

    # L2 norm + Lin Lin criterion
    # kmeans_calcs(Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeans_l2_and_preassign'),
    #              "/home/bucchera/programs/octopus/l2_norm_preassign/octopus")

    # L2 norm + inertia
    # kmeans_calcs(Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeans_l2_and_inertia'),
    #              "/home/bucchera/programs/octopus/l2_norm_inertia/octopus")