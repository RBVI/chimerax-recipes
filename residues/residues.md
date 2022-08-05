# Find residues from specified residue numbers

Here is a Python routine to find residues with specified residue numbers in specified chains.  One way to do this is to run a

    from chimerax.core.commands import run
    residues = run(session, 'select #1/A:105,107/B:228,301').residues

This can be relatively slow for parsing thousands of residues because the command parser in ChimeraX 1.4 is rather slow.  So below is equivalent Python code that will run faster.

    from chimerax.atomic import all_structures
    structures = all_structures(session)
    chain_res = [('A', (105,107)), ('B', (228,301))]
    residues = find_residues(structures[0].residues, chain_res)

Here is the [residues.py](residues.py) code:

    def find_residues(residues, chain_id_and_res_numbers):
        '''
        Return Residues for specified chain identifiers and residue numbers
        given as a list of (chain_id, res_number_list) pairs.
        '''
        chain_ids = residues.chain_ids
        res_nums = residues.numbers
        from numpy import zeros, bool, isin
        mask = zeros((len(residues),), bool)
        for chain_id, res_numbers in chain_id_and_res_numbers:
            mask |= (chain_ids == chain_id) & isin(res_nums, res_numbers)
        return residues[mask]

Tom Goddard, August 2, 2022
