#
# Add bonds between close atoms.  For example,
#
#     connect #1
#
def connect_atoms(session, atoms, to_atoms = None, distance = 2.2):
    if to_atoms is None:
        to_atoms = atoms
    xyz = to_atoms.scene_coords
    bonds = []
    from chimerax.geometry import find_close_points
    for a in atoms:
        i1, i2 = find_close_points([a.scene_coord], xyz, distance)
        for a2 in to_atoms[i2]:
            if a2 is not a and not a2.connects_to(a):
                b = a.structure.new_bond(a, a2)
                bonds.append(b)
    session.logger.status(f'Made {len(bonds)} bonds between'
                          f' {len(atoms)} and {len(to_atoms)} atoms',
                          log = True)
    return bonds

def register_command(logger):
    from chimerax.core.commands import register, CmdDesc, FloatArg
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required = [('atoms', AtomsArg)],
                   keyword = [('to_atoms', AtomsArg),
                              ('distance', FloatArg)],
                   synopsis='Connect close atoms')
    register('connect', desc, connect_atoms, logger=logger)

register_command(session.logger)
