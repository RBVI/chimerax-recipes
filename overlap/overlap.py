#
# Select atoms that overlap previous atoms within a specified distance.
# Opening this Python defines the "overlapped" command.  Example use
#
#	overlap #1 distance 0.3
#

def overlapped_atoms(session, atoms, distance = 0.1):
    xyz = atoms.scene_coords
    from numpy import zeros
    dup = zeros((len(atoms),), bool)
    from chimerax.geometry import find_close_points
    for i,a in enumerate(atoms):
        if not dup[i]:
            i1, i2 = find_close_points([a.scene_coord], xyz, distance)
            dup[i2] = True
            dup[i] = False
    session.selection.clear()
    datoms = atoms[dup]
    datoms.selected = True
    n = len(datoms)
    session.logger.status(f'{n} overlapped atoms', log=True)
    return datoms

def register_command(logger):
    from chimerax.core.commands import register, CmdDesc, FloatArg
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required = [('atoms', AtomsArg)],
                   keyword = [('distance', FloatArg)],
                   synopsis='Select overlapped atoms')
    register('overlapped', desc, overlapped_atoms, logger=logger)

register_command(session.logger)
