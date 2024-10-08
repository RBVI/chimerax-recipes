# Record a movie with a static background image

Here is how to record a movie with a static background image.  The idea is to record all the movie frames with transparent background and then overlay those on a static background image during the movie encoding.  Here is an example rotating an atomic structure in front of a static image of the cryoEM map used to determine that structure.  Make a directory on your Desktop called "movie" to save the image frames.  Then use these ChimeraX commands

    open 8of8
    movie record dir ~/Desktop/movie transparentBackground true format png ; turn y 3 120 ; wait 120 ; movie stop

    open 16850 from emdb
    save ~/Desktop/movie/background.png

To combine the transparent image frames and the background into a movie I'll use the ffmpeg movie encoder that comes with ChimeraX in a shell window on a Mac.

	$ cd ~/Desktop/movie
	$ ~/Desktop/ChimeraX-1.8.app/Contents/bin/ffmpeg -loop 1 -i background.png -i chimovie_Umkk-%05d.png -filter_complex overlay=shortest=1 movie.mp4

Here is where I got this ffmpeg compositing trick

	[https://stackoverflow.com/questions/10438713/overlay-animated-images-with-transparency-over-a-static-background-image-using-f](https://stackoverflow.com/questions/10438713/overlay-animated-images-with-transparency-over-a-static-background-image-using-f)

<video width="538" height="563" controls>
  <source src="movie.mp4" type="video/mp4">
</video>

Tom Goddard, October 8, 2024