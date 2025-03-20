# breakfastSim

# Description
simulate the breakdast process at a hotel to
optimise the placement of item and guest

# Programme working
### class window
define the canva (the canva is 1500 by 1000 px) and the windows can be bigger but not smaller and the canva size stay constant,

draw a dot grid (every 10 px)
offer a function to draw a circle of a given color and a given diameter (in px) and given position (in px) with a number between 0 and 999 written in the middle (the color can also be set but default to white)
offer a function to draw a square of a given color and a given side (in px) and given position (in px) with a number between 0 and 999 written in the middle (the color can also be set but default to white)
offer a function to draw line with a start point and end point with a given width in px (default 2px width) and given color (default black)

has a set of label to display text and another set of label that will display a value ( each text will have a value attached)

a function to update a given text. (the function take into argument the name of the label and the value to write) the name are of the label (and their description) "simulation time", "clean dish", "dirty dish", "free seat", "served guest"

when pressed, the space bar will call step function from class simulation

### class agent
they have a position, shape (circle or square), color, id (between 0 and 999), state and offer a step function.
the state is publicly accessible.

### class customer (inherit from agent)
red circle, id is given at object instanciation and step will contain a logic with a state machine that I will write myself.

### class worker (inherit from agent)
blue square, id is given at object instanciation and step will contain a logic with a state machine that I will write myself.

### class dish
has a position.
as a state (clean or dirty)
is displayed by a circle of radius 2 px (white if clean, brown if dirty)
expose a funtion to move it to a desired location that the customer and worker can use when performing their steps.

### class simulation
has a global state (boolean) called simmulation_running and a public function step and a public function run.
it also has a function to toggle the simulation state 

the function run logic : 
whenever simulation_running is set to true, it will check the current time and if 1 second has elapsed since last run, it will call step.

the step function logic is :

1) Increment the time counter of 1 min and update the displayed time in hh:mm format (use the window class function to change the label value) time start at 6h00 and end at 
2) the time and thus the simulation stop at 11h30 (the function return)
3) if the time is 6h00, spawn 40 dish at position 20,20 (put them in a list)
4) between 6h30 and 10h00, spawn customer following a gaussian probability distribution. (add them to a list)
5) between 6h30 and 10h00, from the list of customer, run their step function
6) between 6h30 and 10h00, from the list of dish, count how many are clean and dirty and update the window value

### main
create the window object
create an object simulation and call simulation.run