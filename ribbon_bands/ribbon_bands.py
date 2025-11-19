# Example of setting per-vertex colors on a molecular ribbon depiction.
#
# See the RibbonsDrawing class in Python code file chimerax/src/bundles/atomic/src/ribbon.py
#
default_color = (255,255,255,255)  # white rgba
def ribbon_bands(session, residues, color = default_color):
    for structure, res in residues.by_structure:
        ribbons_drawing = structure._ribbons_drawing
        if ribbons_drawing is not None:
            vertex_colors = ribbons_drawing.vertex_colors
            if vertex_colors is None:
                from numpy import empty, uint8
                vertex_colors = empty((len(ribbons_drawing.vertices),4), uint8)
                vertex_colors[:] = ribbons_drawing.color
            res_colors = res.ribbon_colors
            rib_res = ribbons_drawing._residues
            xs_mgr = structure.ribbon_xs_mgr	# Ribbon cross-section info for helix, sheet, coil.
            helix_sides = xs_mgr.params[xs_mgr.style_helix]['sides']  # Number of vertices around circumference
            for i,ts,te,vs,ve in ribbons_drawing._triangle_ranges:
                if ve > vs:
                    r = rib_res[i]
                    if r in res:
                        if r.is_helix:
                            # Color every other ring of vertices the specified color.
                            # Vertices are in two half residue segments and consecutive vertices
                            # run along the ribbon length.
                            nrings = ((ve-vs)//helix_sides)//2
                            for s in range(0,nrings,2):
                                vertex_colors[vs+s:ve:nrings] = color
            ribbons_drawing.vertex_colors = vertex_colors
    
def register_command(session):
    from chimerax.core.commands import CmdDesc, register, Color8Arg
    from chimerax.atomic import ResiduesArg
    desc = CmdDesc(required=[('residues', ResiduesArg)],
                   optional = [('color', Color8Arg)],
                   synopsis='Make color bands on ribbon helices')
    register('bands', desc, ribbon_bands, logger=session.logger)

register_command(session)
