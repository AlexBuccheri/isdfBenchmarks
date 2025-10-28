""" Generate ACE+ISDF inputs

Need all the slurm inputs

Re-run the references as well so they're all done with 0.16 Ang spacing

Run kmeans once.
Occs: nocc = 33, 42, 51, 54

 5  * Occ: 165, 252, 255, 270
 7  * Occ: 231, 294, 357, 378
10 * Occ: 330, 420, 510, 540
15 * Occ: 495, 630, 765, 810

Variables to set:
              "ISDFNpoints": "424",  A range of these for each
              "KMeansRepeatInterval": "0"

Once done, can look at the timing breakdowns, and the associated EXX error per atom
"""
import copy
from pathlib import Path

from isdfbenchmarks.molecule_set.molecular_inputs import reference_inputs, isdf_base_inputs
from isdfbenchmarks.molecule_set.molecular_xyz import molecular_xyz_str
from isdfbenchmarks.submission.slurm import SlurmConfig, module_25b
from isdfbenchmarks.parser.inp_gen import basic_dict_to_inp


occupations = {'anthracene': 33, 'tetracene': 42, 'pentacene': 51, 'ether_crown': 54}


def ref_ace(root: Path, molecules, slurm_base_settings):
    """

    :param root: Local root directory
    :param molecules: List of molecules
    :param slurm_base_settings: Common slurm settings
    :return:
    """
    inputs = reference_inputs()

    print("Generating data in:")
    for molecule in molecules:
        # Make directory
        subdirectory = root / molecule
        print(subdirectory.as_posix())
        subdirectory.mkdir(parents=True, exist_ok=True)

        # Input file
        inpr_str = basic_dict_to_inp(inputs[molecule])
        with open(file=subdirectory / "inp", mode='w') as fid:
            fid.write(inpr_str)

        # Structure
        with open(file=subdirectory / "structure.xyz", mode='w') as fid:
            fid.write(molecular_xyz_str[molecule])

        # Slurm
        slurm_settings = slurm_base_settings | {'job_name': f'ref_{molecule}'}
        cfg = SlurmConfig(**slurm_settings)
        with open(file=subdirectory / "slurm.sh", mode='w') as fid:
            fid.write(str(cfg))


def isdf_varying_isdf_number(root: Path, molecules: list, slurm_base_settings: dict):
    """
    Vary ISDF number from 5 * Nocc to 15 * Nocc
    such that one can plot scaling w.r.t. reference,
    and changes in error.

    * Smallest number of Nisdf = 5 * Nocc should be the biggest speed-up
    * Most accurate should be Nisdf = 15 * Nocc
    * Expect/hope a happy compromise between speed-up and precision
      between these two

    Plot error per atom.

    Directory structure:
        nisdf_vector_scaling/
            5_nocc/
                24_anthracene/
                30_tetracene/
                36_pentacene/
                42_ether_crown/
            7.5_nocc
                ...
            10_nocc
                ...
            15_nocc
                ...
    """
    isdf_inputs = isdf_base_inputs()

    print("Generating data in:")
    multipliers = [5, 7.5, 10, 15]
    for m in multipliers:
        directory = root / f"{m}_nocc"
        for molecule in molecules:
            # Make directory
            subdirectory = directory / molecule
            print(subdirectory.as_posix())
            subdirectory.mkdir(parents=True, exist_ok=True)

            # Input file
            n_isdf = int(m * occupations[molecule])
            opts = {"ISDFNpoints": str(n_isdf),
                    "KMeansRepeatInterval": "0"}
            inp_dict = isdf_inputs[molecule] | opts
            inpr_str = basic_dict_to_inp(inp_dict)
            with open(file=subdirectory / "inp", mode='w') as fid:
                fid.write(inpr_str)

            # Structure
            with open(file=subdirectory / "structure.xyz", mode='w') as fid:
                fid.write(molecular_xyz_str[molecule])

            # Slurm
            slurm_settings = slurm_base_settings | {'job_name': f'isdf_{m}_nocc_{molecule}'}
            cfg = SlurmConfig(**slurm_settings)
            with open(file=subdirectory / "slurm.sh", mode='w') as fid:
                fid.write(str(cfg))


if __name__ == '__main__':

    # molecules = ['anthracene', 'tetracene', 'pentacene', 'ether_crown']
    #
    # slurm_base_settings = {'executable': "/home/bucchera/programs/octopus/cmake-build-foss-full-mpi-release/octopus",
    #                        'nodes': 1,
    #                        'ntasks_per_node': 4,
    #                        'cpus_per_task': 8,
    #                        'pre_script': module_25b}
    #
    # ref_root = Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/ace_references')
    # isdf_root = Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/nisdf_vector_scaling')
    #
    # isdf_varying_isdf_number(isdf_root, molecules, slurm_base_settings)
    # ref_ace(ref_root, molecules, slurm_base_settings)


    # Pointing to binary that should be using k-means++ as centroid seeding
    molecules = ['anthracene', 'tetracene', 'pentacene', 'ether_crown']

    slurm_base_settings = {'executable': "/home/bucchera/programs/octopus/l2_norm/octopus",
                           'nodes': 1,
                           'ntasks_per_node': 4,
                           'cpus_per_task': 8,
                           'pre_script': module_25b}

    isdf_root = Path('/Users/alexanderbuccheri/Codes/isdfBenchmarks/outputs/kmeanspp_nisdf_vector_scaling')
    isdf_varying_isdf_number(isdf_root, molecules, slurm_base_settings)
