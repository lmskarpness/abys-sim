# abys-sim - A simple gravity simulator written in Python.

![White Twist](https://github.com/lmskarpness/abys-sim/blob/main/img/twist-white.png?raw=true)

After being met with computation power limitations when writing a gravity engine that accounted for all particles, I discovered an optimization technique that sampled a set of Level of Detail (LOD) grids. This technique examines the masses of surrounding cells on different LODs, capturing nearby particle interactions accurately while coarsely aggregating further away forces. While this brought the O(N^2) complexity of comparing each particle-to-particle interaction to around O(n), the CPU can only do so much. I plan to revisit that project in the near future and utilize GPU-based programming for NVIDIA drivers.

For now, while not completely physically accurate, particle-to-particle interactions are ignored and instead interact with a singular massive object.

## Dependencies
- Pygame
- Numpy

## Features
- Custom UI: Integrate additional controls using the Slider and Toggler classes provided in ui.py.
- Particle creation and positioning with access to initial velocity.

## Areas of Expansion
- Cluster Bubbles: periodically check for areas of high density mass, and replace particles there with a new massive object 
- Universe builder (place massive objects or particles) (UI or easy-to-use generators)
- Port to lower-level language