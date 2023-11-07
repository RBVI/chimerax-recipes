# --------------------------------------------------------------------------------------
# Adds ChimeraX "spots" command to run Segger on a map to segment spots above a given
# threshold and output intensity, volume and position as comma-separated-values.
# This was written to segment puncta in 3D light-microscopy for Arthur Charles at UCSF.
# Example command
#
#     spots #1.2 threshold 10 output spots.csv
#
def spots(session, map, threshold_sdev = None, output_csv = None, smoothing_steps = 0):
    '''Segment light microscopy to quantify spots, report intensities.'''

    # Show map in surface style at desired threshold level at full resolution
    map.set_parameters(style = 'surface', step = 1)

    # Use threshold level of mean plus some number of standard deviations
    if threshold_sdev is not None:
        # Compute mean and standard deviation
        mean, sd = map_mean_and_sd(map)
        threshold = mean + threshold_sdev * sd
        map.set_parameters(surface_levels = [threshold])
    elif len(map.surfaces) == 0:
        map.update_drawings()	# Set initial threshold level

    # Run Segger watershed segmentation
    spots = segment_spots(map, smoothing_steps)

    # Log comma-separated values file of spots.
    lines = ['# Spot number, total intensity, mean intensity, max intensity, number of grid points, max x position, max y position, max z position']
    for i,spot in enumerate(spots):
        lines.append(str(i+1) + ',%.5g,%.5g,%.5g,%d,%d,%d,%d' % spot)
    results = '\n'.join(lines) + '\n'
    session.logger.info(results)

    if output_csv:
        with open(output_csv, 'w') as file:
            file.write(results)

def segment_spots(map, smoothing_steps = 0):
    '''
    ChimeraX does not have a command to run the Segger segmentation so do it with Python.
    '''
    from chimerax.segger import segment_dialog
    d = segment_dialog.volume_segmentation_dialog(session, create=True)
    d._map_menu.value = map
    d._num_steps.value = smoothing_steps
    d.cur_seg = None				# Don't reuse previous segmentation
    segmentation = d.Segment()

    # Put segmentation at same level as map for convenience when
    # showing multiple data sets.
    if segmentation.parent is not map.parent:
        session.models.add([segmentation], parent = map.parent)

    # Quantify each region.
    spots = []
    for region in segmentation.regions:
        ijk = region.points()
        num_grid_points = len(ijk)
        im,jm,km = region.max_point
        m = map.matrix(step = 1)
        from numpy import float64
        mean = m.mean(dtype=float64)
        map_values = m[ijk[:,2],ijk[:,1],ijk[:,0]]
        total_intensity = map_values.sum() - num_grid_points * mean
        mean_intensity = map_values.mean(dtype=float64) - mean
        max_intensity = m[km,jm,im] - mean
        spots.append((total_intensity, mean_intensity, max_intensity, num_grid_points, im, jm, km))

    # Sort from largest to smallest intensity.
    spots.sort(reverse = True)
    
    return spots

def map_mean_and_sd(map):
    m = map.matrix(step = 1)
    from numpy import float64
    mean = m.mean(dtype=float64)
    sd = m.std(dtype=float64)
    return mean, sd

def register_command(session):
    from chimerax.core.commands import CmdDesc, register, FloatArg, SaveFileNameArg, IntArg
    from chimerax.map import MapArg
    desc = CmdDesc(required= [('map', MapArg)],
                   keyword = [('threshold_sdev', FloatArg),
                              ('output_csv', SaveFileNameArg),
                              ('smoothing_steps', IntArg)],
                   synopsis = 'quantify spots in volume data')
    register('spots', desc, spots, logger=session.logger)

register_command(session)
