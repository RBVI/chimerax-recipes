# Move a surface to highest intensity in 3D microscope image

A fluorescently labeled membrane will be seen in 3D microscopy with a thickness that is much greater than the actual membrane due to limited microscope resolution.  Here is a ChimeraX command that tries to place a surface at the highest intensity in the middle of the shell seen in a 3D microscope image.  It starts with surfaces at a specified intensity level (an isosurface).  That will show inner and outer surfaces of the shell.  The command moves those surface toward the higher intensity following the intensity gradient.

Do define the midsurf command opening the Python code [midsurf.py](midsurf.py)

    open midsurf.py

And here is an example opening a 3 channel 3D microscope image [cell14.tif](cell14.tif) and moving the isosurfaces for channel 1.

    open cell14.tif
    volume #1.1 level X
    midsurf #1.1

The first image shows the cell with the membrane cut in half, and the second image shows the computed middle surface in transparent yellow.

<img src="cell14.png" width="500">
<img src="cell14_midsurf.png" width="500">

The midsurf command has several additional options

    midsurf #2 volume #1 steps 100 voxelStep 0.1 smoothingIterations 1 smoothingFactor 0.1

You can specify an initial surface to move (#2 in the example) that is not a map isosurface and then you also need to specify the map ("volume #1" in the example).  The motion is done in steps, by default 100 steps, each step moving at most a certain fraction of the grid spacing (voxelStep 0.1) perpendicular to the surface.  To avoid creases in the surface the vertices are also moved toward the average of the neighbor vertices at each step.  That smoothing is does some number of iterations (smoothingIterations 1) moving each vertex a fraction of the way (smoothingFactor 0.1) to the average neighbor position.  The smoothing can make the surface smaller tending to contract a spherical surface and can pull the surface away from the intensity maximum.  It is useful to try smoothingIterations 0 after the surface is moved to see if it changes the position.

The middle surface can be colored according to the image intensity using menu Tools / Volume Data / Surface Color or the equivalent command

    color sample #1.1 map #1.1 palette bluered
    transparency #1.1 50

<img src="cell14_heatmap.png" width="500">

Here is the Python code [midsurf.py](midsurf.py)

<pre>
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
</pre>

Tom Goddard, July 27, 2022
