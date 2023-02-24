# Create command to copy all atom coordiates from one conformer to another.
# Opening this file in ChimeraX defines the copycrds command.
#
#  copycrds #1 to #2

def copycrds(session, from_struct, to=None):
    from chimerax.core.errors import UserError
    if from_struct.num_atoms != to.num_atoms:
        raise UserError("Both structures must have the same number of atoms")
    from_atoms = from_struct.atoms
    to_atoms = to.atoms

    from_info = [a.string(style="command", omit_structure=True) for a in from_atoms]
    to_info = [a.string(style="command", omit_structure=True) for a in to_atoms]
    if from_info == to_info:
        # safe to just copy coordinates directly
        to_atoms.coords = from_atoms.coords
        return

    fi_set = set(from_info)
    ti_set = set(to_info)
    if fi_set != ti_set:
        # different atoms and/or residues
        differences = fi_set ^ ti_set
        raise UserError("The two structures have different atoms (e.g. %s)" % differences.pop())

    # have the same atoms but in a different order -- assign coordinates "by hand"
    to_atom_lookup = {}
    for to_string, to_atom in zip(to_info, to_atoms):
        to_atom_lookup[to_string] = to_atom
    for from_string, from_atom in zip(from_info, from_atoms):
        to_atom_lookup[from_string].coord = from_atom.coord


def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import StructureArg
    desc = CmdDesc(
           required = [('from_struct', StructureArg)],
           required_arguments = ['to'],
           keyword = [('to', StructureArg)],
           synopsis = 'copy atom coordinates between structures')
    register('copycrds', desc, copycrds, logger=session.logger)

register_command(session)
