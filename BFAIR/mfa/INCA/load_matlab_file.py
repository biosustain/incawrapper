import numpy as np
from scipy.io import loadmat, matlab

def load_matlab_file(filename):
    """
    This function should be called instead of direct scipy.io.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    Thanks to Jeff Lin for this solution
    From: https://stackoverflow.com/questions/48970785/complex-matlab-struct-mat-file-read-by-python
    """

    def _check_vars(d):
        """
        Checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        """
        for key in d:
            if isinstance(d[key], matlab.mat_struct):
                d[key] = _todict(d[key])
            elif isinstance(d[key], np.ndarray):
                d[key] = _toarray(d[key])
        return d

    def _todict(matobj):
        """
        A recursive function which constructs from matobjects nested dictionaries
        """
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, matlab.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _toarray(elem)
            else:
                d[strg] = elem
        return d

    def _toarray(ndarray):
        """
        A recursive function which constructs ndarray from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        """
        if ndarray.dtype != "float64":
            elem_list = []
            for sub_elem in ndarray:
                if isinstance(sub_elem, matlab.mat_struct):
                    elem_list.append(_todict(sub_elem))
                elif isinstance(sub_elem, np.ndarray):
                    elem_list.append(_toarray(sub_elem))
                else:
                    elem_list.append(sub_elem)
            return np.array(elem_list)
        else:
            return ndarray

    # if the file is not found, load_matlab_file will raise an OSError. We catch this error and
    # raise a FileNotFoundError instead, which is more informative.   
    try:
        data = loadmat(filename, struct_as_record=False, squeeze_me=True, appendmat=False)
    except OSError:
        raise FileNotFoundError(f"Could not find the file {filename}")
        
    return _check_vars(data)
