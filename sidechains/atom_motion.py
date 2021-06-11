def atom_motion(session, atoms, to_atoms):
    amap = {(a.residue.chain_id, a.residue.number, a.name):a for a in atoms}
    count = 0
    from chimerax.geometry import distance
    for a in to_atoms:
        a2 = amap.get((a.residue.chain_id, a.residue.number, a.name))
        if a2:
            d = distance(a.scene_coord, a2.scene_coord)
            a2.motion = a.motion = d
            count += 1
    session.logger.status('%d atom pairs' % count, log = True)

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required=[('atoms', AtomsArg)],
                   keyword=[('to_atoms', AtomsArg)],
                   required_arguments = ['to_atoms'],
                   synopsis='Set motion atom attribute to distance between corresponding atoms.')
    register('atommotion', desc, atom_motion, logger=session.logger)

register_command(session)
