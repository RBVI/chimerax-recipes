from chimerax.atomic import selected_atoms
for a in selected_atoms(session):
  a.radius = a.bfactor
