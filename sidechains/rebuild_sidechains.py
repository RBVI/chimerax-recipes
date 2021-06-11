# Run swapaa on every residue for each displayed atomic structure.
# This replaces all side chains and is intended to complete the side chains.

def rebuild_sidechains(session, residues):
    '''
    Runs swapaa on each residue to replace the side chain with same amino acid
    in order to complete the side chains.
    '''
    from chimerax.core.commands import run
    from chimerax.core.errors import UserError, LimitationError
    errors = []
    for i,r in enumerate(residues):
        if 'CA' in r.atoms.names:
            command = 'swapaa %s %s log false' % (r.string(style = 'command'), r.name)
            try:
                run(session, command, log = False)
            except (UserError, LimitationError) as e:
                errors.append(str(e))
            session.logger.status('Completed %d of %d residues' % (i+1, len(residues)),
                                  secondary = True)
    if errors:
        msg = '\n'.join(errors)
        session.logger.warning(msg)

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import ResiduesArg
    desc = CmdDesc(required=[('residues', ResiduesArg)],
                   synopsis='Replace side chains to complete side chain atoms')
    register('rebuildsidechains', desc, rebuild_sidechains, logger=session.logger)

register_command(session)
