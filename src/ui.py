# Written by Lucas Skarpness (2024)

import pygame
import numpy as np

class UI:
    @staticmethod
    def init(sim) -> None:
        # Fonts
        UI.fps_font = pygame.font.Font(None, 30)
        UI.controls = pygame.font.Font(None, 20)
        
        # Screen sizes areas
        UI.width = sim.display_size[0]
        UI.height = sim.display_size[1]
        UI.half_width = UI.width // 2
        UI.half_height = UI.height // 2
        UI.center = np.array((UI.half_width, UI.half_height))
        UI.top_left = np.array((0, 0))

        # Basic Colors
        UI.color = {
            'black': (0, 0, 0),
            'dgray': (169,169,169),
            'lgray': (211,211,211),
            'white': (255, 255, 255),
            'red':   (255, 0, 0),
            'green': (0, 255, 0),
            'blue' : (0, 0, 255),
        }

        # Hottest (fast) to coldest (slow)
        # UI.spectrum = {
        #     'O': UI.color['blue'],  # Blue
        #     'B': (174, 204, 228),   # Light Steel Blue
        #     'A': UI.color['white'], # White
        #     'F': (255, 248, 207),   # White yellow (Lemon Chiffon)
        #     'G': (251, 212, 77),    # Yellow (Gargoyle Gas)
        #     'K': (249, 110, 21),    # Orange (Pumpkin)
        #     'M': (249, 110, 21)     # Orange Red (Tangelo)
        # }

        UI.spectrum2 = {
            'O': UI.color['blue'],  # Blue
            'M': (249, 110, 21)     # Orange Red (Tangelo)
        }

        UI.fonts = {
            'fps': UI.fps_font,
            'ctrl': UI.controls
        }


class Menu:
    def __init__(self, sim) -> None:
        self.sim = sim
        self.sliders = [
            Slider(UI.top_left, np.array((100, 30)), 0.99, 10e6, 10e7)
        ]
        self.togglers = [
            Toggler(UI.top_left + np.array((0, 30)), np.array((30,30))),
            Toggler(UI.top_left + np.array((0, 60)), np.array((30,30)))
        ]
        fps_x = UI.width - 60
        fps_y = 10
        self.fps_counter = FPS(np.array((fps_x, fps_y)), sim)
    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed() # 0: left mb, 1 = middle mb, 2 = right mb
        for slider in self.sliders:
            # If mouse is on slider and lmb is clicked, will drag the slider button around or
            # snap to mouse location.
            if slider.container.collidepoint(mouse_pos) and mouse[0]:
                slider.move_slider(mouse_pos)
                print(slider.get_value())
            slider.render(self.sim)
        
        
        for toggler in self.togglers:
            if toggler.container.collidepoint(mouse_pos) and mouse[0]:
                toggler.toggle()
            toggler.render(self.sim)
        self.fps_counter.render()

class Slider:
    def __init__(self, pos, size, init_val: float, min: int, max: int):
        # Corrects invalid inputs
        if (min > max or max < min):
            min = 0
            max = 1

        self.pos = pos
        self.size = size
        self.min = min
        self.max = max

        self.left_pos = self.pos[0]
        self.right_pos = self.pos[0] + self.size[0]
        self.top_pos = self.pos[1]
        self.init_val = (self.right_pos - self.left_pos) * init_val

        self.container = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.button = pygame.Rect(self.left_pos + self.init_val - 4, self.top_pos, 8, self.size[1])
    def move_slider(self, mouse_pos):
        self.button.centerx = mouse_pos[0];
    def render(self, sim):
        pygame.draw.rect(sim.screen, "lightgray", self.container)
        pygame.draw.rect(sim.screen, "darkgray", self.button)
    def get_value(self):
        value_range = self.right_pos - self.left_pos - 1 # Adjust to get full range
        button_val = (self.button.centerx) - self.left_pos
        return (button_val / value_range) * (self.max - self.min) + self.min

class Toggler:
    def __init__(self, pos, size, toggled: bool = False):
        self.pos = pos
        self.size = size
        self.toggled = toggled
        self.container = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.button = pygame.Rect(self.pos[0] + 1, self.pos[1] + 1, self.size[0] - 2, self.size[0] - 2)
    def render(self, sim):
        pygame.draw.rect(sim.screen, "lightgray", self.container)
        if self.toggled:
            pygame.draw.rect(sim.screen, "red", self.button)
        else:
            pygame.draw.rect(sim.screen, "darkgray", self.button)
    def toggle(self):
        self.toggled = False if self.toggled else True
    def get_value(self):
        return self.toggled

class FPS:
    def __init__(self, pos, sim):
        self.pos = pos
        self.sim = sim
    def render(self):
        fps_rounded = "{:.2f}".format(round(self.sim.clock.get_fps(), 2))
        self.fps = UI.fonts['fps'].render(fps_rounded, True, UI.color['green'])
        self.sim.screen.blit(self.fps, (self.pos[0], self.pos[1]))
