print("")
print("Copy subset of model")
print("Command: copy model-sepc")
print("e.g.copy sel")

from chimerax.core.commands import CmdDesc, register, run
from chimerax.atomic import AtomsArg

def copy_sel(session, atoms):
    # Get unique structures from selected atoms
    structures = atoms.unique_structures

    run(session, f"sel {atoms.spec}")
    for s in structures:

        # Get current model IDs
        existing_ids = {m.id for m in session.models}
        
        # Find smallest available ID starting from 1
        placeholder_id = 1000
        
        # Use a placeholder ID for the new model
        original_ID = s.id_string
        original_name = s.name 
        run(session, f"rename #{s.id_string} id #{placeholder_id} name 'copy of {s.name}'")
        run(session, f"combine #{placeholder_id} model {original_ID} name '{original_name}'")
        # Invert selection to select unselected regions and delete them
        run(session, f"select ~sel & ##selected")
        run(session, f"del sel")
        run(session, f"combine #{placeholder_id} name '{s.name}'")
        run(session, f"del #{placeholder_id}")



def register_copy(session):
    desc = CmdDesc(
        required=[('atoms', AtomsArg)],
        synopsis='Copy selected atoms into new models, delete unselected regions, and combine original models.'
    )
    register('copy', desc, copy_sel, logger=session.logger)

register_copy(session)
