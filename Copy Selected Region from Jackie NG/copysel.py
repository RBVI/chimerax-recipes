print("")
print("Copy subset of model")
print("Command: copy atom-spec")
print("e.g.copy sel")

def copy_sel(session, atoms):

    from chimerax.core.commands import run
    for s, s_atoms in atoms.by_structure:
        copied = run(session, f"combine {s.atomspec}")
        copied.atoms[~s.atoms.mask(atoms)].delete()

def register_copy(session):

    from chimerax.core.commands import CmdDesc, register
    from chimerax.atomic import AtomsArg
    desc = CmdDesc(
        required=[('atoms', AtomsArg)],
        synopsis='Copy selected atoms into new models, delete unselected regions, and combine original models.'
    )
    register('copy', desc, copy_sel, logger=session.logger)

register_copy(session)
