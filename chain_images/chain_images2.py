# Create command to save an image of specified chains of an atomic structure.
#
#  chainimages #1/A,B,C
#
def chain_images(session, atoms):
    from chimerax.core.commands import run
    for structure, chain_id, chain_atoms in atoms.by_chain:
        run(session, 'show #%s/%s only' % (structure.id_string, chain_id))
        run(session, 'view')
        run(session, 'save ~/Desktop/%s_chain_%s.png' % (structure.name, chain_id))

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required=[('atoms', AtomsArg)],
                   synopsis='Save image of each chain')
    register('chainimages', desc, chain_images, logger=session.logger)

register_command(session)
