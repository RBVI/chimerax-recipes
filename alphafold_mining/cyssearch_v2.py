# Dengke Ma wants to find all C elegans proteins with pairs of close cysteines in transmembrane regions.
# Can use UniProt to identify transmembrane residues, then use AlphaFold database predicted structures
# to see if there are close cysteines.

def find_uniprot_transmembrane_cysteines(uniprot_xml_path, namespace = '{http://uniprot.org/uniprot}'):
    import xml.etree.ElementTree as ET
    tree = ET.parse(uniprot_xml_path)
    tm = []
    for child in tree.getroot():
        if child.tag == namespace + 'entry':
            rr = transmembrane_residue_ranges(child, namespace)
            uniprot_id = child.find(namespace + 'accession').text
            seq = child.find(namespace + 'sequence').text
            full_name = child.find(f'./{namespace}protein/{namespace}submittedName/{namespace}fullName')
            name = '' if full_name is None else full_name.text
            helix_cys_count = [seq[b-1:e].count('C') for b,e in rr]
            hcc = max(helix_cys_count, default = 0)
            tm.append((uniprot_id, name, hcc, len(seq), rr))
    return tm

def transmembrane_residue_ranges(protein_xml_entry, namespace):
    ranges = []
    for feature in protein_xml_entry.iter(namespace + 'feature'):
        fattrib = feature.attrib
        if 'type' in fattrib and fattrib['type'] == 'transmembrane region':
            for loc in feature.iter(namespace + 'location'):
                b,e = loc.find(namespace + 'begin'), loc.find(namespace + 'end')
                if b is not None and e is not None:
                    if 'position' in b.attrib and 'position' in e.attrib:
                        r = (int(b.attrib['position']), int(e.attrib['position']))
                        ranges.append(r)
    return ranges

def close_cysteines(structure, membrane_residue_ranges, max_distance = 5):
    cys_res = [r for r in structure.residues if r.name == 'CYS']
    cys_xyz = [(r.number, r.find_atom('SG').coord) for r in cys_res]
    mb_res_nums = residue_numbers_from_ranges(membrane_residue_ranges)
    mb_cys = [r for r in cys_res if r.number in mb_res_nums]
    mb_xyz = [(r.number, r.find_atom('SG').coord) for r in mb_cys]

    close_pairs = set()
    from chimerax.geometry import distance
    for rnum, xyz in mb_xyz:
        for rnum2, xyz2 in cys_xyz:
            if rnum2 != rnum and distance(xyz, xyz2) <= max_distance:
                pair = (rnum, rnum2) if rnum < rnum2 else (rnum2, rnum)
                close_pairs.add(pair)

    return list(close_pairs)

def residue_numbers_from_ranges(residue_ranges):
    res_nums = set()
    for b,e in residue_ranges:
        for rnum in range(b,e+1):
            res_nums.add(rnum)
    return res_nums

def check_for_close_cysteines(session, ulist, alphafold_dir, max_distance):
    found = []
    missing = []
    for uniprot_id, ncys, seq_len, tm_res_ranges in ulist:
        if ncys == 0:
            continue
        m = alphafold_database_model(session, uniprot_id, alphafold_dir)
        if m is None:
            missing.append((uniprot_id, seq_len))
            continue
        close_pairs = close_cysteines(m, tm_res_ranges, max_distance)
        if close_pairs:
            found.append((uniprot_id, close_pairs))
        m.delete()
    return found, missing

def alphafold_database_model(session, uniprot_id, alphafold_dir):
    filename = f'AF-{uniprot_id}-F1-model_v4.cif'
    from os.path import join, exists
    path = join(alphafold_dir, filename)
    if not exists(path):
        return None
    from chimerax.mmcif import open_mmcif
    s, msg = open_mmcif(session, path)
    return s[0]

def open_entries(session, entries, alphafold_dir):
    models = []
    for uniprot_id, name, ncys, seq_len, tm_res_ranges in entries:
        m = alphafold_database_model(session, uniprot_id, alphafold_dir)
        models.append(m)
        # Select transmembrane residues
        rnums = residue_numbers_from_ranges(tm_res_ranges)
        for r in m.residues:
            if r.number in rnums:
                r.atoms.selected = True
    session.models.add(models)
    
uniprot_xml_path = 'UP000001940_6239.xml'
alphafold_dir = 'alphafold_models'
max_distance = 5

ulist = find_uniprot_transmembrane_cysteines(uniprot_xml_path)
#uclose, missing = check_for_close_cysteines(session, ulist, alphafold_dir, max_distance)
print(f'{len(ulist)} UniProt entries')
ntm = len([uniprot_id for uniprot_id, name, ncys, seq_len, tm_res_ranges in ulist if tm_res_ranges])
ntmc = len([uniprot_id for uniprot_id, name, ncys, seq_len, tm_res_ranges in ulist if ncys > 0])
print(f'{ntm} entries with annotated transmembrane regions')
print(f'{ntmc} entries with 1 or more transmembrane cysteines')
min_cys = 5
min_helix = 4
u3 = [(uniprot_id, name, ncys, seq_len, tm_res_ranges)
      for uniprot_id, name, ncys, seq_len, tm_res_ranges in ulist if ncys >= min_cys and len(tm_res_ranges) >= min_helix]
print(f'{len(u3)} UniProt entries with {min_cys} cysteines in one transmembrane helix and at least {min_helix} transmembrane helices')
#print(f'{len(uclose)} with two cysteines closer than {max_distance}A, at least 1 being transmembrane')

#entries = []
#for uniprot_id, res_pairs in uclose:
#    rpairs = ' '.join(f'{r1},{r2}' for r1,r2 in res_pairs)
#    entries.append(f'{uniprot_id} {rpairs}')
entries = [f'{uniprot_id},{name},{len(tm_res_ranges)},{ncys}'
           for uniprot_id, name, ncys, seq_len, tm_res_ranges in u3]

print()
print('# UniProt ID, protein name, number of transmembrane segments, maximum single segment cysteines)')
print('\n'.join(entries))
print()

open_entries(session, u3, alphafold_dir)

#me = '\n'.join(f'{uniprot_id} {seq_length}' for uniprot_id, seq_length in missing)
#print(f'No alphafold model for {len(missing)} entries with transmembrane regions:\n{me}')
    
