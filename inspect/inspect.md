# Inspecting molecule data structures

Here is how to inspect the Python molecular data structures, atoms, residues, and chains.  Start ChimeraX and open a PDB atomic model

    open 8aie

and show the Python Shell, menu Tools / General / Shell and type the following Python into the shell

<pre>
    <b>session.models.list()</b>
    [<chimerax.atomic.structure.AtomicStructure at 0x7fa771aeceb0>]

    <b>m = session.models[0]</b>
    <b>print(m.name, m.num_atoms, 'atoms', m.num_residues, 'residues', m.num_chains, 'chains')</b>
    8aie 4609 atoms 792 residues 2 chains

    <b>a = m.atoms[50]</b>
    <b>print('Atom', a, 'at', a.coord, 'with bfactor', a.bfactor)</b>
    Atom /A ILE 6 O at [5.626 -27.109 17.19] with bfactor 32.77000045776367

    <b>r = a.residue</b>
    <b>print('Residue', r, 'has atoms', ', '.join(atom.name for atom in r.atoms))</b>
    Residue /A ILE 6 has atoms N, CA, C, O, CB, CG1, CG2, CD1

    <b>c = r.chain</b>
    <b>print('Chain', c.chain_id, 'is', c.description, 'with', c.num_residues, 'residues')</b>
    Chain A is Aminotransferase class IV with 277 residues
</pre>

There is information about the attributes of atoms, residues, chains, bonds, structures in the programming manual [here](https://www.cgl.ucsf.edu/chimerax/docs/devel/modules/atomic/atomic.html), for instance, [Atom properties](https://www.cgl.ucsf.edu/chimerax/docs/devel/modules/atomic/atomic.html#chimerax.atomic.cymol.CyAtom).

Tom Goddard, November 23, 2022
