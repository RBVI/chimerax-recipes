# Make hovering mouse over an atom run Python code

The atom names that popup when you hover over the mouse appear because the mode "identify object" is assigned to the mouse pause event.  You can see the active mouse modes by typing the [mousemode](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/ui.html#mousemode) ChimeraX command:

<pre>
<b>mousemode</b>
left: rotate
control left: select
middle: translate
right: translate
wheel: zoom
pause: identify object
</pre>

and setting the pause mode is done using a command like

    mousemode pause "identify object"

You could write some Python code to define a new mouse mode to do whatever you want.  You can copy the current "identify object" mode Python code as a starting point.  It is at the ChimeraX Github source repository [here](https://github.com/RBVI/ChimeraX/blob/7e0a20f26b0de02e63e7ff6a43bc227921aa529e/src/bundles/mouse_modes/src/std_modes.py#L755).  In your ChimeraX distribution on Mac this file would be located here

    ChimeraX.app/Contents/lib/python3.9/site-packages/chimerax/mouse_modes/std_modes.py

Looking at the "identify object" code I see it invokes a [trigger](https://www.rbvi.ucsf.edu/chimerax/docs/devel/modules/core/triggerset.html) which can run other code, so you could leave the pause mouse mode as "identify object" and just add some Python code that will do something when hovering in addition to the usual showing the atom name.  Here is an example that logs the atom x,y,z position when you hover over it.

    def mouse_hover(trigger_name, pick):
        from chimerax.atomic import PickedAtom
        if isinstance(pick, PickedAtom):
            atom = pick.atom
            x,y,z = atom.scene_coord
            message = f'Atom %s position %.2f,%.2f,%.2f' % (str(atom), x, y, z)
            session.logger.status(message, log = True)

    session.triggers.add_handler('mouse hover', mouse_hover)

I put this in a file [hover.py](hover.py) and opened it in ChimeraX (command "open ~/Downloads/hover.py") to register the mouse_hover() callback function.  Then hovering over an atom logs a message

        Atom /A ASN 72 ND2 position -15.70,-23.42,-0.77

Opening that Python could be automatically done at ChimeraX startup using ChimeraX Preferences / Startup / Execute these commands at startup.

Tom Goddard, July 6, 2023
