""" Dictionaries for molecular inputs
"""


def reference_inputs() -> dict:
    """ Use for reference ACE calculations, and as base settings
    for ISDF
    :return:
    """

    anthracene = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    tetracene = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    pentacene = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    ether_crown = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    chlorophyll = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    buckminster = {"CalculationMode": "gs",
                  "ExperimentalFeatures": "yes",
                  "ProfilingMode": "yes",
                  "ParStates": "auto",
                  "ParDomains": "no",
                  "BoxShape": "minimum",
                  "Radius": "6.0 * angstrom",
                  "Spacing": "0.16 * angstrom",
                  "XYZCoordinates": "'structure.xyz'",
                  "XCFunctional": "hyb_gga_xc_b3lyp",
                  "Eigensolver": "chebyshev_filter",
                  "ExtraStates": "12",
                  "ConvRelDens": "1e-6",
                  "EigensolverTolerance": "1e-7",
                  "OptimizeChebyshevFilterDegree": "yes"}

    inputs = {'anthracene': anthracene,
              "tetracene":tetracene,
              "pentacene": pentacene,
              "ether_crown": ether_crown,
              "chlorophyll": chlorophyll,
              "buckminster": buckminster}

    return inputs


def isdf_base_inputs() -> dict:

    # ACE size is determined by the number of occupied states
    # and is therefore fixed.
    # Note, this breaks when using smearing, or if one has partial
    # occupations.
    anthracene = {"ACEWithISDF": "yes",
                  "ACESize": "33"}

    tetracene = {"ACEWithISDF": "yes",
                 "ACESize": "42"}

    pentacene = {"ACEWithISDF": "yes",
                 "ACESize": "51"}

    ether_crown = {"ACEWithISDF": "yes",
                  "ACESize": "54"}

    buckminster = {"ACEWithISDF": "yes",
                   "ACESize": "120"}

    chlorophyll = {"ACEWithISDF": "yes",
                   "ACESize": "114"}

    isdf_inputs = {'anthracene': anthracene,
                   "tetracene":tetracene,
                   "pentacene": pentacene,
                   "ether_crown": ether_crown,
                   "buckminster": buckminster,
                   "chlorophyll": chlorophyll
                   }

    ref_inputs = reference_inputs()

    inputs = {}
    for name in list(ref_inputs):
        inputs[name] = ref_inputs[name] | isdf_inputs[name]

    return inputs
