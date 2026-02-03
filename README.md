# small-projects
Random small projects I've done.

## evolved_houses (Mar 2021)
A genetic algorithm to evolve houses evaluating on weather, economic, and cultural factors. The home can be graphed in matplotlib or my custom 3D renderer.

I was inspired by the idea of a game where you're in a town the culture and conditions of the town are procedurally generated.

Evaluation parameters include:
- sun protection
- water protection
- x/z symmetry
- resource availability
- material sweetspot
- height

`home.py` contains the main genetic algorithm, with generic functions for culling, evaluating, mutating, and crossing over.
`render_house.py` contains a 3D graphics engine built on top of pygame. It renders polygons with basic normal lighting.

A roof for a house that favors symmetry on x and asymmetry on z, sun protection is necessary, and there's a material constraint.

![](evolved_houses/roof.png)
![](evolved_houses/house_3d.PNG)

A sphere and part of a car rendered in the 3D renderer.

![](evolved_houses/sphere.PNG)
![](evolved_houses/car.PNG)

## function_vis (Nov 2021)
Contains a skeleton for writing and visualizing functions of x, y, t in 2D.

I like visualizing functions. :) I would like to make it generate a random function, one day with time and inspiration.

![](function_vis/hyper_beam.PNG)

## Kalimba (Dec 2023)
A Kalimba practice tool. You can input a tab or set `use_random` and then play the Kalimba. If your microphone is on, it'll detect the frequency of the note you played and move you to the next note once you play it. 

It doesn't currently support chords or non-C-major scales.
