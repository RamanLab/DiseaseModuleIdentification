cimport numpy as np
np.import_array()

# cdefine the signature of our c function
cdef extern from "pprgrow_min_cond.h":
	void init(long *data, long n_data, long *indices, long n_indices, long *indptr, long n_indptr, long *seed, long n_seed,
		long *community, double *mincond, double alpha, double curexpand)

# create the wrapper code, with numpy type annotations
def pprgrow_min_cond_func(np.ndarray[long, ndim=1, mode="c"] data not None, long n_data,
	np.ndarray[long, ndim=1, mode="c"] indices not None, long n_indices,
	np.ndarray[long, ndim=1, mode="c"] indptr not None, long n_indptr,
	np.ndarray[long, ndim=1, mode="c"] seed not None, long n_seed,
	np.ndarray[long, ndim=1, mode="c"] community not None,
	double mincond, double alpha, double curexpand):
	init(<long*> np.PyArray_DATA(data), n_data,
		<long*> np.PyArray_DATA(indices), n_indices,
		<long*> np.PyArray_DATA(indptr), n_indptr,
		<long*> np.PyArray_DATA(seed), n_seed,
		<long*> np.PyArray_DATA(community),
		&mincond, alpha, curexpand)
