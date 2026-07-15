# debruijn
Find A) an image that contains all n x n images and B) the smallest image that contains all n x n images.

*nxn.py* does the A naively. I generated up to all 5x5 images, which was 20480x40960! 2.png and 3.png are for 2x2 and 3x3 respectively.

*smallestnxn_\*.png* try to create the smallest possible image that contains all n x n images using a genetic algorithm to optimize toward having more unique sub images. 5x5.png is the smallest for 2x2. 25x34.png is the smallest I found for 3x3, though an 18x34 image is the smallest possible image with enough pixels (2^4 + (3-1) x 2^5 + (3-1)). I ran smallestnxn_smart.py at this size but the best I got had only ~90% of all 3x3s... the search continues! smallestnxn_graph.py uses an Eulerian path approach, which considers options much faster since there's no image manipulation, but it didn't get particularly close either since there's so many possible images (2^(18*34)).

Later I learned this is a known problem called de Bruijn Torus. My implementations don't consider wrapping, but you could construct mine from duplicating the top and left of the torus image to the bottom and right. There are already 16x32 solutions, but I haven't dove into their construction yet: https://demonstrations.wolfram.com/TheDeBruijnTorus/. Wikipedia gives a 4x4 image too! https://en.wikipedia.org/wiki/De_Bruijn_torus.
