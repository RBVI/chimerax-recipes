# ChimeraX copy selected atoms recipe

A utility to create new models containing only selected atoms while preserving original structures.

## Features
- Creates copies of selected regions as new models


## Installation
1. Save the following code as [copysel.py](copysel.py)
2. Place the file in your ChimeraX scripts folder:
   - `~/ChimeraX/scripts/` (Linux/Mac)
   - `C:\Users\<you>\AppData\Roaming\ChimeraX\scripts\` (Windows)

## Usage
1. Copy defined selection:

         copy #1/A:100-200

3. Copy selected region:  
   
         copy sel

## Code Implementation

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

## Alternative implementation using only commands

Here is an alternative implementation of this command [Copy.py](copy.py) that uses just ChimeraX commands Python functions.  ⚠️ Important: Temporary models use ID 1000 - ensure this ID is available

     print("Copy subset of model")
     print("Command: copy model-spec")
     print("e.g. copy sel")
     
     from chimerax.core.commands import CmdDesc, register, run
     from chimerax.atomic import AtomsArg
     
     def copy_sel(session, atoms):
         structures = atoms.unique_structures
         run(session, f"sel {atoms.spec}")
         
         for s in structures:
             placeholder_id = 1000
             original_ID = s.id_string
             original_name = s.name 
             
             run(session, f"rename #{s.id_string} id #{placeholder_id} name 'copy of {s.name}'")
             run(session, f"combine #{placeholder_id} model {original_ID} name '{original_name}'")
             run(session, f"select ~sel & ##selected")
             run(session, f"del sel")
             run(session, f"combine #{placeholder_id} name '{s.name}'")
             run(session, f"del #{placeholder_id}")
     
     def register_copy(session):
         desc = CmdDesc(
             required=[('atoms', AtomsArg)],
             synopsis='Create new models from selected atoms'
         )
         register('copy', desc, copy_sel, logger=session.logger)
     
     register_copy(session)

Jackie NG, May 2025
