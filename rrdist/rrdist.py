# Compute all pairwise distances between residues and write to a JSON file in AlphaFold PAE
# format so that the distance map can be displayed as a 2D plot with menu entry
# Tools / Structure Prediction / AlphaFold Error Plot.

def rr_distance_map(session, structure, json_output_path):
    residues = structure.residues

    # Choose atom for each residue to measure distances
    atoms = []
    for r in residues:
        a = r.principal_atom
        if a is None:
            # Use the first atom if no principal atom.
            # The distance matrix must have the same size as the number of residues
            # in the structure for the AlphaFold PAE plot to work.
            a = r.atoms[0]
        atoms.append(a)

    # Compute distance matrix
    from chimerax.atomic import Atoms
    xyz = Atoms(atoms).scene_coords
    n = len(xyz)
    from numpy import empty, float32, sqrt
    dist = empty((n,n), float32)
    for i in range(n):
        row = xyz - xyz[i]
        dist[i,:] = sqrt((row*row).sum(axis = 1))

    # Write matrix in JSON AlphaFold PAE format
    # {"pae": [[17.14, 18.75, 17.91, ...], [5.32, 8.23, ...], ... ]}
    dists = ', '.join(('[ ' + ', '.join('%.2f' % dist[i,j] for j in range(n)) + ' ]')
                      for i in range(n))
    with open(json_output_path, 'w') as file:
        file.write('{"pae": [')
        file.write(dists)
        file.write(']}')

    # Open PAE plot
    from chimerax.core.commands import run, quote_if_necessary
    open_cmd = f'alphafold pae #{structure.id_string} file {quote_if_necessary(json_output_path)}'
    run(session, open_cmd)

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, SaveFileNameArg
    from chimerax.atomic import StructureArg
    desc = CmdDesc(
        required = [('structure', StructureArg),
                    ('json_output_path', SaveFileNameArg)],
        synopsis = 'Compute residue-residue distance map and show with AlphaFold PAE plot'
    )
    register('rrdist', desc, rr_distance_map, logger=logger)

register_command(session.logger)
