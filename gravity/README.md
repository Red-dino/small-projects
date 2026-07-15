# gravity 🪐
Simple 2D Newtonian gravity sim with momentum based collisions.

The simulation is pretty slow because there are no optimizations. One easy and typical optimization for this type of sim would be to only consider force vectors for close objects, ignoring or using a coarse mass calculation for far away objects.

Controls:
- p: toggle printing object coords each frame
- a: add a new set of particles
- f: zoom and pan to fit all the particles into the window
- c: center on the sun at the current zoom
- minus: zoom out
- equals: zoom in
- left: pan left
- right: pan right
- up: pan up
- down: pan down
- escape: quit

I originally created this sim in October 2023.
