import pygame
import numpy as np
import keyboard
import time

def initialize_joystick():
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        return joystick

def get_axis(joystick):
    joystick.init()
    pygame.event.get()
    axis = np.array([joystick.get_axis(0), joystick.get_axis(1)])
    return axis


if __name__ == "__main__":

    joystick = initialize_joystick()
    done = False

    while not done:
        if keyboard.is_pressed('esc'):
            done = True

        axis = get_axis(joystick)
        print("Axis: ", axis, "\n")

        time.sleep(0.15)

    pygame.quit()