#
# Register a Python callback to log the coordinates of an atom when
# the mouse hovers over the atom.
#
def mouse_hover(trigger_name, pick):
    from chimerax.atomic import PickedAtom
    if isinstance(pick, PickedAtom):
        atom = pick.atom
        x,y,z = atom.scene_coord
        message = f'Atom %s position %.2f,%.2f,%.2f' % (str(atom), x, y, z)
        session.logger.status(message, log = True)

session.triggers.add_handler('mouse hover', mouse_hover)
