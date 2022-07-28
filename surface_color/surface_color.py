def surfcolor(session, surface, values_file, palette = None):
    '''
    Color surface using vertex values read from a file.
    '''
    with open(values_file, 'r') as f:
        values = [float(line) for line in f.readlines() if line.strip() != '']
    if len(values) != len(surface.vertices):
        raise ValueError(f'File {values_file} has {len(values)} values which does not match '
                         f'the number of vertices ({len(surface.vertices)} in {surface.name}')
    if palette is None:
        from chimerax.core.colors import BuiltinColormaps
        palette = BuiltinColormaps['red-white-blue'].rescale_range(min(values), max(values))
    surface.vertex_colors = palette.interpolated_rgba8(values)
    
def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, SurfaceArg, OpenFileNameArg, ColormapArg
    desc = CmdDesc(
        required = [('surface', SurfaceArg)],
        keyword = [('values_file', OpenFileNameArg),
                   ('palette', ColormapArg)],
        required_arguments = ['values_file'],
        synopsis = 'Color a surface using values at each vertex read from a file'
    )
    register('surfcolor', desc, surfcolor, logger=logger)

register_command(session.logger)
