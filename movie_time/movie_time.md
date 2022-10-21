# Show a time label while playing a volume series

Here is how to show a time label when recording a movie playing through a volume series.  It uses the  [perframe](https://www.rbvi.ucsf.edu/chimerax/docs/user/commands/perframe.html) command and the [2dlabel](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/2dlabels.html) command to update a label for each frame.  Here is what the recorded movie [cell6.mp4](cell6.mp4) looks like.

<video width="400" height="300" controls>
  <source src="cell6.mp4" type="video/mp4">
</video>


## Setting up the scene

First I open 3D light microscopy data with 30 images, set threshold levels, the camera view angle, the lighting and the window size and save a ChimeraX session file "cell6.cxs" in preparation for making the movie.  I do this with the ChimeraX menus and panels.  But here are commands that do these things

    open cell6_1ch*.tif vseries true
    volume #1 level 130 step 1
    volume #1 voxelSize .1,.1,.25
    lighting soft
    set bgcolor white
    graphics silhouettes true
    windowsize 800 600
    2dlabel create timestamp text "" xpos 0.9 ypos 0.05
    save cell6.cxs

I also created a time stamp label with the 2dlabel command in this session that will be used to show the time.

# Recording the movie
To record the movie I put these commands in a ChimeraX command file [cell6.cxc](cell6.cxc)

    movie record
    perframe "2dlabel change timestamp text $1" frames 30 range 0,6 format %.1f
    vseries play #1
    wait 30
    movie encode cell6.mp4 framerate 5 quality high

and then open that command script in ChimeraX to run it.

    open cell6.cxc

The saved movie file [cell6.mp4](cell6.mp4) will play back at 5 frames per second because of the "framerate 5" option.

## How to show the time in seconds

The example above puts a time in seconds in the lower right corner, assuming that my 30 microscopy images were acquired in a total of 6 seconds.  It shows the time with one digit past the decimal point (the "format %.1f" option). To put an integer frame count I could instead use this perframe command

    perframe "2dlabel change timestamp text $1" frames 30


Tom Goddard, October 21, 2022