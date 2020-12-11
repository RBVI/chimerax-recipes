# Save an Image of each Chain

Here is Python code that defines a command that saves an image of each chain of an atomic structure

    open chain_images.py

then use the command on the atomic model.

    chainimages #1

<img src="2bbv.jpg">

Here is the [chain_images.py](chain_images.py) code:

    # Create command to save an image of each chain of an atomic structure.
    #
    #  chainimages #1
    #
    def chain_images(session, atoms):
        from chimearx.core.commands import run
        for structure, chain_id, chain_atoms in atoms.by_chain:
           run(session, 'show #%s/%s only' % (structure.id_string, chain_id))
           run(session, 'view all')
           run(session, 'save ~/Desktop/%s_chain_%s.png' % (structure.name, chain_id))

    def register_command(session):
        from chimerax.core.commands import CmdDesc, register
        from chimerax.atomic import AtomsArg
        desc = CmdDesc(required=[('atoms', AtomsArg)],
                       synopsis='Save image of each chain')
        register('chainimages', desc, chain_images, logger=session.logger)

    register_command(session)

Tom Goddard, December 11, 2020
