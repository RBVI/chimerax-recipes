# Create command fitsearch to run fitmap with the search option,
# then save the results that have correlation higher than a specified value.
#
#  fitsearch #1 in #2 resolution 11.5 search 50 cutoff 0.9 save ~/Desktop/results/mol.pdb

def fit_search(session, atoms, in_map, resolution = None, search = 10, cutoff = 0.5,
               save = None):
    if resolution is None:
        resolution = 3*min(in_map.grid.step)
        
    from chimerax.map_fit.fitcmd import fitmap
    fits = fitmap(session, atoms, in_map, resolution = resolution, search = search)
    good_fits = [f for f in fits if f.correlation() >= cutoff]
    from chimerax.map_fit.search import save_fits
    save_fits(session, good_fits, save)

def register_command(session):
    from chimerax.core.commands import CmdDesc, register, ObjectsArg, FloatArg, IntArg, SaveFileNameArg
    from chimerax.map import MapArg
    desc = CmdDesc(required=[('atoms', ObjectsArg)],
                   keyword=[('in_map', MapArg),
                            ('resolution', FloatArg),
                            ('search', IntArg),
                            ('cutoff', FloatArg),
                            ('save', SaveFileNameArg)],
                   required_arguments = ['in_map'],
                   synopsis='Save atomic structures fit in a map')
    register('fitsearch', desc, fit_search, logger=session.logger)

register_command(session)
