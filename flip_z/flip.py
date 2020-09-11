# Create command to change atom coordiates z -> -z.
# Opening this file in ChimeraX 1.0 defines the flip command.
#
#  flip #1

def flip(session, atoms):
    xyz = atoms.coords
    xyz[:,2] *= -1
    atoms.coords = xyz

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(required=[('atoms', AtomsArg)],
                   synopsis='flip atom z coordinates')
    register('flip', desc, flip, logger=session.logger)

register_command(session)
