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
