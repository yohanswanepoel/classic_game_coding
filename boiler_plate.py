import pygame_sdl2 as pygame
import scene
 
pygame.init()
 
class Example(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        # scene variables here
 
    def blit(self, surface):
        surface.fill((0,0,120))
        # draw code here
 
    def event(self, event):
        # event code here
        if event.type == pygame.QUIT:
            scene.quit_scene()
 
if __name__ == '__main__':
    handler = scene.Handler('Example', (800,600))
    E = Example()
    scene.add_scene('Example', E)
    handler.loop('Example')
 
    pygame.quit()