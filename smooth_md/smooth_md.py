window = 2  # number of adjacent frames to average
stride = 1  # only use every Nth frame of trajectory (to save memory for large trjectories)

from chimerax.atomic import Structure
for s in session.models:
	if not isinstance(s, Structure) or s.num_coordsets == 1:
		continue
	session.logger.status("Smoothing trajectory %s" % s)

	session.logger.status("Gathering coordinates", secondary=True)
	if stride > 1:
		coordset_ids = s.coordset_ids
		coord_sets = [s.coordset(coordset_ids[i]).xyzs for i in range(0, len(coordset_ids), stride)]
	else:
		coord_sets = [s.coordset(cs_id).xyzs for cs_id in s.coordset_ids]

	session.logger.status("Computing smoothed coordinates", secondary=True)
	import numpy
	smoothed = numpy.zeros((len(coord_sets), len(coord_sets[0]), 3), type(coord_sets[0][0][0]))
	for i in range(len(coord_sets)):
		weight_tot = 0
		avg = smoothed[i]
		for j in range(i-window, i+window+1):
			if j < 0 or j >= len(coord_sets):
				continue
			weight = window + 1 - abs(i-j)
			weight_tot += weight
			avg += weight * coord_sets[j]
		avg /= weight_tot

	session.logger.status("Setting coordinates", secondary=True)
	s.add_coordsets(smoothed)

	session.logger.status("Smoothed trajectory %s" % s)
