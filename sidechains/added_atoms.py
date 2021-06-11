def added_atoms(session, atoms, to_atoms):
    amap = {(a.residue.chain_id, a.residue.number, a.name):a for a in atoms}
    from chimerax.atomic import Atoms
    added = Atoms([a for a in to_atoms
                   if (a.residue.chain_id, a.residue.number, a.name) not in amap])
    session.selection.clear()
    added.selected = True
    session.logger.status('Added %d atoms' % len(added), log = True)
    return added

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required=[('atoms', AtomsArg)],
                   keyword=[('to_atoms', AtomsArg)],
                   required_arguments = ['to_atoms'],
                   synopsis='Select atoms in second set that are not in first set.')
    register('addedatoms', desc, added_atoms, logger=session.logger)

register_command(session)
