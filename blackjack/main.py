import pygame
pygame.init()

screen = pygame.display.set_mode([640, 480])
def main():
    running = True
    while(running):
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #update

        #render
        screen.fill((255, 255, 255))
        pygame.display.flip()
    
    pygame.quit()
    return

main()