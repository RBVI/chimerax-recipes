# Show PyMol view direction

Here is Python code defining a command "pymolview" that sets the camera view direction to match a view in PyMol using the parameters from the PyMol [https://pymolwiki.org/index.php/Get_View](cmd.get_view()) function. Open the Python code to define the command

    open pymol_view.py

then use the command to set the camera view using the 18 parameters reported by PyMol.

    open 4v0x
    pymolview 0.5338886380195618, 0.19662711024284363, 0.8223745822906494, 0.1919989138841629, 0.9189900159835815, -0.34437406063079834, -0.8234677910804749, 0.34175243973731995, 0.452885240316391, 0.0, 0.0, -177.17364501953125, -27.024879455566406, 14.224754333496094, -6.485495567321777, 139.68505859375, 214.6622314453125, -20.0

PyMol
<img src="pymol_view.png" height="300">

ChimeraX
<img src="chimerax_view.png" height="300">

This command does not set the clip planes or orthographic projection although those could be easily added.

Here is the [pymol_view.py](pymol_view.py) code:

Tom Goddard, June 24, 2022
