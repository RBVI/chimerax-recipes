# Create command to save an image of each chain of an atomic structure.
#
#  chainimages #1
#
def chain_images(session, structures):
    from chimerax.core.commands import run
    for structure in structures:
        for chain_id in structure.residues.unique_chain_ids:
            run(session, 'show #%s/%s only' % (structure.id_string, chain_id))
            run(session, 'view')
            run(session, 'save ~/Desktop/%s_chain_%s.png' % (structure.name, chain_id))

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import StructuresArg
    desc = CmdDesc(required=[('structures', StructuresArg)],
                   synopsis='Save image of each chain')
    register('chainimages', desc, chain_images, logger=session.logger)

register_command(session)
