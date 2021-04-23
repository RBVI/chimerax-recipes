# Record a movie flipping through planes of a microscopy map

To record a movie showing grayscale planes of a 3D electron microscopy map use the [planes](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/volume.html#planes) option of the [volume](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/volume.html) command.  To put a numeric label giving the plane number on each frame of the video we use the [2dlabel](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/2dlabels.html) command.  To cycle through the planes and update the labels we use the [perframe](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/perframe.html) command that runs the needed volume and 2dlabel commands once for each plane to be shown.

We will try this for a SARS-Cov-2 spike cryoEM map id [22910](https://www.ebi.ac.uk/pdbe/entry/emdb/EMD-22910) from the EM Databank.

Normally I load the data and set the thresholds and zooming using the ChimeraX graphical user interface and then save it as a session in case I want to change the movie in the future.  But here I'll show commands that do the setup for completeness.  I use orthographic camera mode instead of the default perspective mode so that the planes don't change size with distance.

    windowsize 500 500
    open 22910 from emdb
    volume #1 style image level -0.4458,0 level 2.326,1 plane z,100
    view orient
    zoom 2
    camera ortho
    2dlabel text "plane number" xpos 0.8 ypos 0.1

Then use the [movie](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/movie.html) command to record the movie.

    movie record size 500,500
    perframe "volume #1 plane z,$1 ; 2dlabel #2.1 text $1" range 100,300
    wait 201
    movie encode ~/Desktop/planes.mp4 quality high

Here is the movie this set of commands [planes.cxc](planes.cxc) produces:

<video width=500 height=500 controls>
  <source src="planes.mp4" type="video/mp4">
</video>

Tom Goddard, April 22, 2021