""" Generate an Octopus inp from a python dict
"""


def basic_dict_to_inp(inp_dict: dict) -> str:
    """ Cannot handle blocks. Only key:value pairs

    For handling blocks, refer to my old project
    :return:
    """
    inp_str = ""
    for key, value in inp_dict.items():
        inp_str += f"{key} = {value}\n"
    return inp_str
