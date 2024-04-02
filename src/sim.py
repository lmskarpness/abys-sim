# Written by Lucas Skarpness (2024)

import sys, math, random, pygame
import numpy as np
from ui import UI, Menu

FRAME_WIDTH = 1200
FRAME_HEIGHT = 800
CENTER = np.array((FRAME_WIDTH // 2, FRAME_HEIGHT // 2))

G = 0.2
M = 10e7
DEFAULT_PARTICLE_MASS = 2
DEFAULT_PARTICLE_RADIUS = 1
DEFAULT_PARTICLE_MOMENTUM = np.array((500, 500), dtype=float)
AXIS_SIZE = 20

class Particle:
    def __init__(self, position, mass = DEFAULT_PARTICLE_MASS):
        self.position = position
        self.mass = mass
        self.momentum = DEFAULT_PARTICLE_MOMENTUM.copy()
        self.velocity = self.momentum / self.mass
        self.vmagnitude = np.sqrt(self.velocity.dot(self.velocity))
    def display(self, sim):
        if sim.menu is not None:
            if sim.menu.togglers[0].toggled:
                pygame.draw.circle(sim.screen, self.velocity_color(sim), self.position, DEFAULT_PARTICLE_RADIUS);
            else:
                pygame.draw.circle(sim.screen, UI.color['white'], self.position, DEFAULT_PARTICLE_RADIUS);
            if sim.menu.togglers[1].toggled:
                self.show_axes()
        else:
            pygame.draw.circle(sim.screen, UI.color['white'], self.position, DEFAULT_PARTICLE_RADIUS);
    def velocity_color(self, sim):
        self.vmagnitude = np.sqrt(self.velocity.dot(self.velocity))
        alpha = (self.vmagnitude - 10) / (1000 - 10)
        alpha = np.clip(alpha, 0, 1)
        interpolated_color = sim.SPECTRUM_L + alpha * (sim.SPECTRUM_R - sim.SPECTRUM_L)
        # Convert to RGB
        color = tuple(int(c) for c in interpolated_color)
        return color
    def move(self, sim, dt):
        dir = CENTER - self.position
        hyp = (self.position[0] - CENTER[0]) ** 2 + (self.position[1] - CENTER[1]) ** 2
        dist = np.sqrt(hyp)
        unit_dir = dir / dist
        if sim.menu is not None:
            force = (G * sim.menu.sliders[0].get_value() * self.mass) / hyp
        else:
            force = (G * M * self.mass) / hyp
        force_vec = force * unit_dir
        self.momentum += force_vec * dt
        self.velocity = self.momentum / self.mass
        self.position += (self.velocity) * dt
        self.vmagnitude = np.sqrt(self.velocity.dot(self.velocity))
    def show_axes(self):
        v_axis = (self.velocity / np.linalg.norm(self.velocity)) * AXIS_SIZE
        pygame.draw.line(sim.screen, "red", self.position, self.position + v_axis) # Velocity axis

        direction = CENTER - self.position
        a_axis = (direction / np.linalg.norm(direction)) * AXIS_SIZE
        pygame.draw.line(sim.screen, "blue", self.position, self.position + a_axis) # Acceleration axis


class Simulator:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Gravity Simulator")
        self.display_size = (FRAME_WIDTH, FRAME_HEIGHT)
        self.screen = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()
        UI.init(self)
        self.menu = Menu(self)
        # self.color_mode = self.menu.togglers[0].toggled
        self.SPECTRUM_L = pygame.Color(UI.spectrum2['O'])
        self.SPECTRUM_R = pygame.Color(UI.spectrum2['M'])
        self.particles = []
    def clean_far_particles(self):
        for particle in self.particles:
            if np.linalg.norm(CENTER - particle.position) > 6500:
                self.particles.remove(particle)
    def run(self):
        self.running = True
        direction_tick = 0

        # Choose a shape here

        self.circle()
        # self.one()
        # self.two()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Limit framerate
            dt_ms = self.clock.tick(120)
            dt = dt_ms / 5000

            direction_tick += dt
            if (direction_tick > 1.0):
                self.clean_far_particles()

            # Clear the screen
            self.screen.lock()
            self.screen.fill(UI.color["black"])
            pygame.draw.circle(self.screen, UI.color['white'], CENTER, 3)

            for particle in self.particles:
                particle.move(self, dt)
                particle.display(self)
            
            self.screen.unlock()

            self.menu.run()

            pygame.display.flip()
    def circle(self):
        for i in range(1000):
            ang = random.uniform(0, 1) * 2 * math.pi
            hyp = math.sqrt(random.uniform(0, 1)) * 200
            adj = math.cos(ang) * hyp
            opp = math.sin(ang) * hyp
            x = (self.display_size[0] // 2) + adj
            y = (self.display_size[1] // 2) + opp
            particle = Particle(np.array((x, y)))
            self.particles.append(particle)
    def two(self):
        particle1 = Particle(np.array((300, 300)))
        particle2 = Particle(np.array((800, 500)))
        self.particles.append(particle1)
        self.particles.append(particle2)
    def one(self):
        particle = Particle(np.array((300, 300), dtype = float))
        self.particles.append(particle)

sim = Simulator()
sim.run()
