# basic script by: thomas.kirk at eng.ox.ac.uk
# accessed via this website: https://mail.python.org/pipermail/neuroimaging/2019-February/001941.html

# How to save a surface in GIFTI format (.surf.gii)

# The surface is represented by a GiftiImage object, containing two GiftiDataArrays, each of which contain the points and triangles arrays respectively.
# Each GiftiDataArray requires some extra metadata to denote the fact that they should be interpreted as surface data.

# The example below is for the left white/gray surface of the cortex
# ps and ts are np.array objects, size M x 3 and N x 3, float and int types respectively.
import nibabel as nib
import numpy as np

HCP_dir = os.path.join(os.sep, 'Users', 'neichert', 'code', 'Brainhack', 'local_only_nicole', 'data')
rootdir = os.path.join(os.sep, 'Users', 'neichert', 'code', 'Brainhack', 'Brainhack_Oxbridge')
out_fname = os.path.join(rootdir, 'segment.surf.gii')


# function to delete duplicate rows from a numpy array
def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)] * a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


# load example surface
fname_surf = os.path.join(HCP_dir, '103414', 'MNINonLinear', 'fsaverage_LR32k', f'103414.L.inflated.32k_fs_LR.surf.gii')
my_surface = nib.load(fname_surf)

# array of points with x,y,z coordinates
ps = my_surface.darrays[0].data
# array of faces with coordinates of vertices that it connects
ts = my_surface.darrays[1].data

# mask of indices for vertices to keep in the output
# TODO: works only for indices starting at 0
fname_label = os.path.join(rootdir, 'labels', '103414', 'segments_L.func.gii')
my_labels = nib.load(fname_label)

# #mask indices based on label (doesn't work atm...)
# my_inds = np.where(my_labels.darrays[1].data == 1)

# select the first 1000 vertices of the surface
my_inds = np.arange(0, 1000)

# selection of vertices
ps_sel = ps[my_inds, :]

# selection of triangles

# initialize with zeros
ts_sel = np.zeros((1, 3), dtype=int)

for ind in my_inds:
    # all triangles that connect to those indices
    inside = ts[np.where(ts[:, 0] == ind) and np.where(ts[:, 1] == ind) and np.where(ts[:, 2] == ind) ]
    for row in inside:
        # don't add triangles, if they don't connect to three valid vertices
        if np.isin(row, my_inds).sum() == 3:
            ts_sel = np.vstack((ts_sel, row))

# delete first row
ts_sel = np.delete(ts_sel, 0, 0)
# remove duplicates
ts_sel = unique_rows(ts_sel)

# change order of triangles to match the original one
ind_2 = np.array([], dtype=int)
for ind_ts in np.arange(0, ts_sel.shape[0]):
    ind_2 = np.append(ind_2, np.int(np.where(np.all(ts_sel[ind_ts] == ts, axis=1))[0][0]))

ts_sel = ts_sel[ind_2.argsort()]

# change file type
ts_sel = ts_sel.astype(np.int32)


# The points array
# Prepare the metadata for this array as a dict.
# Strictly speaking, the user is free to add to these as necessary
# (see the GIFTI specification, page 14), but note that some programs
# eg wb_view expect certain fields as below to be present.
pmeta = {
    'description': 'anything',      # brief info here
    'GeometricType': 'Anatomical',     # an actual surface; could be 'Inflated', 'Hull', etc
    'AnatomicalStructurePrimary': 'CortexLeft', # the specific structure represented
    'AnatomicalStructureSecondary': 'GrayWhite', # if the above field is not specific enough
}

# Prepare the coordinate system.
# The general form is GiftiCoordSystem(X,Y,A) where X is the intial space,
# Y a destination space, and A the affine transformation between X and Y.
# See GIFTI spec, page 9
# By default A = I(4), so X and Y can have the same values, as follows:
# 0: NIFTI_XFORM_UNKNOWN
# 1: NIFTI_XFORM_SCANNER_ANAT
# 2: NIFTI_XFORM_ALIGNED_ANAT
# 3: NIFTI_XFORM_TALAIRACH
# 4: NIFTI_XFORM_MNI_152
pcoord = nib.gifti.GiftiCoordSystem(1, 1)    # surface is in world mm coordinates

parray = nib.gifti.GiftiDataArray(ps_sel,
    intent='NIFTI_INTENT_POINTSET',                     # represents a set of points
    coordsys=pcoord,                                    # see above
    datatype='NIFTI_TYPE_FLOAT32',                      # float type data
    meta=nib.gifti.GiftiMetaData.from_dict(pmeta)   # again, see above.
)

# The triangles array
# Triangle metadata dict
tmeta = {
    'TopologicalType': 'Closed',    # a closed surface, could be 'Open', see spec
    'Description': 'anything',      # brief info here
}

# Triangle coordinate system.
# As the triangles are not point data, we put it into NIFTI_XFORM_UNKNOWN space
# for consistency with the behaviour of nib.load() on a GIFTI surface
tcoord = nib.gifti.GiftiCoordSystem(0, 0)

tarray = nib.gifti.GiftiDataArray(ts_sel,
    intent='NIFTI_INTENT_TRIANGLE',                     # triangle surface elements
    coordsys=tcoord,                                    # see above
    datatype='NIFTI_TYPE_INT32',                        # integer indices
    meta=nib.gifti.GiftiMetaData.from_dict(tmeta)   # see above
)

# Finally, create the GiftiImage object and save
gii_obj = nib.gifti.GiftiImage(darrays=[parray, tarray])
nib.save(gii_obj, out_fname)
