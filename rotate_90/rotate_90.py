# Create command "volume rotate90" to rotate a map 90 degrees about z.
#
#  volume rotate90 #1

def volume_rotate90(session, volume):
    # Swap x and y axes then flip sign of x axis.
    m = volume.full_matrix().transpose((0,2,1))[:,:,::-1].copy()
    from chimerax.map_data import ArrayGridData
    ox,oy,oz = volume.data.origin
    sx,sy,sz = volume.data.step
    grid = ArrayGridData(m, origin = (oy,ox,oz), step = (sy,sx,sz),
                             name = volume.name + 'rotate 90')
    from chimerax.map import volume_from_grid_data
    v = volume_from_grid_data(grid, session)
    return v
    
def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.map import MapArg
    desc = CmdDesc(required=[('volume', MapArg)],
                   synopsis='Rotate map 90 degrees about z axis')
    register('volume rotate90', desc, volume_rotate90, logger=session.logger)

register_command(session)
