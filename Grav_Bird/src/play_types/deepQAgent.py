from constants import *
from play_types.defaultAgent import RunDefaultAgent
import pygame

class RunBestAgent(RunDefaultAgent):
    def __init__(self, screen):
        super().__init__(screen)

    #-------------------------------------------------------------------------------
    # overriding run methods
    #-------------------------------------------------------------------------------
    