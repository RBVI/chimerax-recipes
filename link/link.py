def link(session, linker_start, linker_end, template_start, template_end,
         force_constant = 1000, steps = 100, frames = 50):
    '''
    Connect several linkers between starting and ending templates.
    A linker's start atoms are aligned to a starting template and then the linker's end
    atoms are tugged towards a nearby ending template using molecular dynamics.

    Each linker has its start atoms rigidly aligned to a start template.
    The end template for a linker is chosen as the closest to the template start that
    is not yet used.  The start atoms for all linkers are in linker_start and each linker
    is a separate model.  Likewise the end atoms to match for all linkers are in linker_end.
    
    The template start atoms must be in the same order and equal in number to the linker
    start atoms, and each template start must be a separate chain.  There must be the
    same number of template start chains as there are linkers and they are paired with
    linkers in order.

    The template end atoms must match in order the linker end atoms.
    Each template end must be in a separate chain, and there must be at least as
    many template ends as there are linkers.
    '''
    lstart = {s:latoms for (s,latoms) in linker_start.by_structure}
    lend = {s:latoms for (s,latoms) in linker_end.by_structure}
    lpairs = [(latoms, lend[s]) for s,latoms in lstart.items()]
    tstart = [catoms for (s,cid,catoms) in template_start.by_chain]
    tend = [catoms for (s,cid,catoms) in template_end.by_chain]
    used = set()  # Used template ends
    from chimerax.std_commands.align import align
    from chimerax.tug.tugcommand import tug
    from chimerax.atomic import concatenate
    for (ls,le),ts in zip(lpairs, tstart):
        # Find which template end to use
        i0, i1 = nearest_linker_atoms(ls, le)
        tavailable = [te for te in tend if id(te) not in used]
        te = closest_template_end(ts[i0].scene_coord, tavailable, i1)
        used.add(id(te))
        # Align linker start to template start
        align(session, ls, ts, log_info = False)
        # Tug linker end to template end and linker start to template start.
        tug(session, concatenate((ls,le)), concatenate((ts,te)),
            force_constant = force_constant, steps = steps, frames = frames,
            finish = True)
        
def nearest_linker_atoms(start_atoms, end_atoms):
    '''Find atom indices of atoms closest in sequence number.'''
    s = sorted(start_atoms, key = lambda a: a.residue.number)
    e = sorted(end_atoms, key = lambda a: a.residue.number)
    if start_atoms[0].residue.number < end_atoms[0].residue.number:
        a0,a1 = s[-1], e[0]
    else:
        a0,a1 = s[0], e[-1]
    return start_atoms.index(a0), end_atoms.index(a1)

def closest_template_end(xyz, template_ends, atom_index):
    from chimerax.geometry import distance
    dists = [(distance(xyz, te[atom_index].scene_coord), te) for te in template_ends]
    return min(dists)[1]

def register_command(logger):
    from chimerax.core.commands import register, CmdDesc, FloatArg, IntArg
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(keyword = [('linker_start', AtomsArg),
                              ('linker_end', AtomsArg),
                              ('template_start', AtomsArg),
                              ('template_end', AtomsArg),
                              ('force_constant', FloatArg),
                              ('steps', IntArg),
                              ('frames', IntArg),
                              ],
                   required_arguments = ['linker_start', 'linker_end',
                                         'template_start', 'template_end'],
                   synopsis='Position linkers')
    register('link', desc, link, logger=logger)

register_command(session.logger)

