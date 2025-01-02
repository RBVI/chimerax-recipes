# Mean PAE Values

David Fay [asked](https://mail.cgl.ucsf.edu/mailman/archives/list/chimerax-users@cgl.ucsf.edu/thread/BTFIX2DG5YMY6LJ6XA2OJIDHSXZIGKMY/) on the ChimeraX mailing list about how to display average predicted aligned error values from AlphaFold predictions.  Here are two examples of how to modify ChimeraX Python code to print out average PAE values.

To make the alphafold contacts command output the average PAE value I edited the Python file in my ChimeraX 1.9 distribution (on Mac)

    ChimeraX.app/Contents/lib/python3.11/site-packages/chimerax/alphafold/contacts.py
 
where it prints out the "54 residue or atom pairs within distance 5 with pae <= 5” in these lines

    msg = f'Found {len(rapairs)} residue or atom pairs within distance %.3g' % distance
    if max_pae is not None:
        msg += ' with pae <= %.3g' % max_pae

I added a couple more lines that print the average PAE

    from numpy import mean
    msg += ' with average pae %.3g' % mean(pae_values)

Then when I restart ChimeraX and use the alphafold contacts command I get output

    Found 5 residue or atom pairs within distance 3 with average pae 4.1

To make a mouse drag on the PAE plot report the average PAE value within the rectangle dragged I modified ChimeraX 1.9 distribution file (on Mac)

    ChimeraX.app/Contents/lib/python3.11/site-packages/chimerax/alphafold/pae.py

at the bottom of the routine _rectangle_select() I added these lines of code

    pae = self._pae
    ave = pae.pae_matrix[r3:r4+1,r1:r2+1].mean()
    rra = pae.row_residues_or_atoms()
    yres = _residue_and_atom_spec(rra[r3:r4+1])
    xres = _residue_and_atom_spec(rra[r1:r2+1])
    print(f'Mean PAE {"%.3g" % ave} in dragged box {xres} aligned to {yres}')

Restarting ChimeraX and dragging a rectangle on the PAE plot now reports

    Mean PAE 5.97 in dragged box /A:139-176 aligned to /A:2-19

There are harder ways to get average PAE values.   To get the average PAE value from the "alphafold contacts" command you could output all the contacts to a file as described in the [documentation](https://www.rbvi.ucsf.edu/chimerax/docs/user/commands/alphafold.html#contacts) using the outputFile option and then use other software like a speadsheet program to extract the column of PAE values from the file and average it.
