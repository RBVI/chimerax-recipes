# Select residues that cross periodic box faces

Molecular dynamics simulations using a periodic box will typically have structural elements that cross the periodic box boundaries during the course of the simulation.  Even simulations that have been "re-imaged" to keep the principal solute from crossing the box boundaries will frequently have other elements, such as solvents or lipids, that cross the box faces.  When viewing the trajectory such elements will seem to "leap" from one side of the simulation to the other, which may be an undesirable distraction in a presentation, web page, or other contexts.

The Python code below (box_crossers.py) will select residues that cross a periodic boundary during the course of the simulation.  Once selected they then could be hidden, deleted, or otherwise manipulated, such as further reducing the selection to just solvent (*e.g.* "sel sel & solvent").
Opening the box_crossers.py code in ChimeraX selects the boundary-crossing residues:

    open box_crossers.py

Here is the [box_crossers.py](box_crossers.py) code:

	from chimerax.atomic import all_atomic_structures
	crossers = set()
	for s in all_atomic_structures(session):
		if s.num_coordsets < 2:
			continue
		s.atoms.selecteds = False
		coords = s.atoms.coords
		min_size = None
		for axis in range(3):
			axis_coords = coords[:,axis]
			size = max(axis_coords) - min(axis_coords)
			if min_size is None or size < min_size:
				min_size = size
		cross_distance = min_size / 2
		cs_ids = s.coordset_ids
		for i, cs_id in enumerate(cs_ids[:-1]):
			xyzs = s.coordset(cs_id).xyzs
			next_xyzs = s.coordset(cs_ids[i+1]).xyzs
			for r in s.residues:
				if r in crossers or not r.atoms:
					continue
				coord_index = r.atoms[0].coord_index
				for axis in range(3):
					if abs(xyzs[coord_index][axis] - next_xyzs[coord_index][axis]) > cross_distance:
						crossers.add(r)
						r.atoms.selecteds = True
						break
