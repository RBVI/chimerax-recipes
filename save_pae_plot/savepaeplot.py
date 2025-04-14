def save_pae_plot(session, structure, path):
    from chimerax.alphafold.pae import AlphaFoldPAEPlot
    for tool in session.tools.list():
        if isinstance(tool, AlphaFoldPAEPlot) and tool._pae.structure is structure:
            tool._pae_view.save_image(path)

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, SaveFileNameArg
    from chimerax.atomic import StructureArg
    desc = CmdDesc(
        required = [('structure', StructureArg),
                    ('path', SaveFileNameArg)],
        synopsis = 'Save an image of a PAE plot'
    )
    register('savepaeplot', desc, save_pae_plot, logger=logger)

register_command(session.logger)    

    
