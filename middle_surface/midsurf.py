# Move surface vertices along a volume gradient until they reach a maximum.
# Move them normal to the surface and keep the vertices and normals uniform
# by smoothing frequently.
#
# This is to find the center cell membrane surface in a roughly spherical shell
# seen in light microscopy.  For Arthur Charles-Orszag.
#
def middle_surface(session, surface, volume = None, steps = 100, voxel_step = 0.1,
                   smoothing_factor = 0.1, smoothing_iterations = 1):
    from chimerax.map import VolumeSurface
    if volume is None and isinstance(surface, VolumeSurface):
        volume = surface.volume
    points = surface.vertices
    xyz_to_ijk_transform = volume.data.xyz_to_ijk_transform * volume.scene_position.inverse() * surface.scene_position 
    data_array = volume.full_matrix()
    gradients = points.copy()
    max_step = min(volume.data.step) * voxel_step
    from chimerax.map_data import interpolate_volume_gradient
    vertices, normals, triangles = surface.vertices, surface.normals, surface.triangles
    for step in range(steps):
        interpolate_volume_gradient(vertices, xyz_to_ijk_transform, data_array,
                                    gradients = gradients)
        ips = (normals * gradients).sum(axis = 1)
        mag = max(abs(ips.max()), abs(ips.min()))
        ips *= max_step / mag
        vertices += normals*ips[:,None]
        from chimerax.surface import smooth_vertex_positions
        smooth_vertex_positions(vertices, triangles, smoothing_factor, smoothing_iterations)
        from chimerax.surface import calculate_vertex_normals
        normals = calculate_vertex_normals(vertices, triangles)
    surface.set_geometry(vertices, normals, triangles)

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, SurfaceArg, IntArg, FloatArg
    from chimerax.map import MapArg
    desc = CmdDesc(
        required = [('surface', SurfaceArg)],
        keyword = [('volume', MapArg),
                   ('steps', IntArg),
                   ('voxel_step', FloatArg),
                   ('smoothing_factor', FloatArg),
                   ('smoothing_iterations', IntArg)],
        synopsis = 'Move surface to volume maxima'
    )
    register('midsurf', desc, middle_surface, logger=logger)

register_command(session.logger)

