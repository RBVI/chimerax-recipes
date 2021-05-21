#
# Read an MRC file and save a subbox region as another MRC file.
#
from chimerax.map_data import mrc, GridSubregion
g = mrc.open('/Users/goddard/Downloads/ChimeraX/EMDB/emd_11997.map')[0]
gbox = GridSubregion(g, ijk_min = (130,100,160), ijk_max = (190,180,220))
mrc.save(gbox, '/Users/goddard/Desktop/subregion.mrc')

# If you want to use the 3D numpy array for the subregion here is how to get it
m = gbox.matrix()
