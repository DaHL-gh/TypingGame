import pygame as pg

class EventHandler:
    def __init__(self, window):
        self.window = window

    def handle_events(self):
        for event in pg.event.get():
            pass
