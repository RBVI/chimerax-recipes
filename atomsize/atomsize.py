def atomsize(session, atoms, attribute = 'bfactor', scale = 0.02, offset = 0.0):
    for a in atoms:
        value = getattr(a, attribute, None)
        if value is None:
            value = getattr(a.residue, attribute, None)  # Try residue attribute
        if value is not None:
            a.radius = offset + scale * value
            a.draw_mode = a.SPHERE_STYLE

def register_command(logger):
    from chimerax.core.commands import register, CmdDesc, StringArg, FloatArg
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required = [('atoms', AtomsArg)],
                   keyword = [('attribute', StringArg),
                              ('scale', FloatArg),
                              ('offset', FloatArg),
                              ],
                   synopsis='Set atom sizes proportional to an attribute value')
    register('atomsize', desc, atomsize, logger=logger)

register_command(session.logger)
