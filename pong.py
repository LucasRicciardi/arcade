# -*- coding: utf-8 -*-

import asyncio
import pygame
import random
import math
import time
import sys
import os

# -- Screen size
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (640, 480)

# -- Colors
BLACK = (0x00, 0x00, 0x00)
WHITE = (0xff, 0xff, 0xff)
RED   = (0xff, 0x00, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE  = (0x00, 0x00, 0xff)

# -- Default size for ball and paddles
BALL_SIZE = (20, 20)
PADDLE_SIZE = (25, 90)
PADDLE_SPEED = 5

#########################################################################################
#
#   # # #     #              #       #       #     # # # #      # # # #
#   #    #    #             # #        #   #       #            #      # 
#   # # #     #            #   #         #         # # # #      # # # #
#   #         #           # # # #        #         #            # # 
#   #         # # # #    #       #       #         # # # #      #   # #
#
##########################################################################################

class Player(pygame.sprite.Sprite):
    '''
        Player that controls the paddles
    '''
    def __init__(self, app):
        # -- Call parent's constructor
        super(Player, self).__init__()

        # -- Register to receive the events notifications
        app.subscribe(self, (pygame.KEYDOWN, pygame.KEYUP))

        # -- Create a paddle with default size
        self.paddle = paddle = pygame.Surface(PADDLE_SIZE)
        self.rect = paddle.get_rect()

        # -- Player's paddle will be on the left
        self.rect.x = 0

        # -- Paddles can only move in Oy axis
        self.dy = 0

        # -- Player's paddle will be blue
        self.color = BLUE

        # -- Player's current score
        self.score = 0

    def update(self, ball):
        # -- Move in the Oy axis
        self.rect.y += self.dy

        # -- Stop at the top of the screen
        if self.rect.top <= 0:
            self.rect.top = 0

        # -- Or at the bottom
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
    def draw(self, screen):
        screen.fill( self.color, self.rect)

    def notify(self, e):
        # If users press some button
        if e.type == pygame.KEYDOWN:
            # -- If up arrow pressed
            if e.key == pygame.K_UP:
                self.dy = -PADDLE_SPEED
            # -- If down arrow pressed
            if e.key == pygame.K_DOWN:
                self.dy = PADDLE_SPEED
        
        # -- If users 'unpress' the button
        if e.type == pygame.KEYUP:
            # -- If he was pressing down or up arrows, stop the movement
            if e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                self.dy = 0

#########################################################################################
#
#       #     #          #      # # # #   #     #   #   #       #   # # # #
#      # #   # #        # #     #         #     #   #   # #     #   #
#     #   # #   #      #   #    #         # # # #   #   #   #   #   # # # #
#    #     #     #    # # # #   #         #     #   #   #     # #   #
#   #      #      #  #       #  # # # #   #     #   #   #       #   # # # #
#
##########################################################################################

class Machine(Player):
    '''
        AI for we to play against
    '''
    def __init__(self, app):
        # -- Call parent's constructor
        super(Machine, self).__init__(app)

        # -- Machine's paddle will be located on the right of the screen
        self.rect.x = SCREEN_WIDTH - self.rect.width

        # -- Machine paddle will be red
        self.color = RED

    def notify(self, e):
        pass 

    def update(self, ball):
        # -- If the ball is above the y coordinate, move up
        if ball.rect.y > self.rect.y:
            self.dy = PADDLE_SPEED + 1
        # -- If the ball is below the bottom of the paddle, move down
        elif (ball.rect.y + ball.rect.width) < self.rect.y:
            self.dy = -(PADDLE_SPEED + 1)
        else:
            self.dy = 0

        # Update just like parent's class
        super(Machine, self).update(ball)

#########################################################################################
#
#   # # #        #         #          #
#   #    #      # #        #          #
#   # # #      #   #       #          #
#   #    #    #  #  #      #          #   
#   # # #    #       #     # # # #    # # # # 
#   
##########################################################################################

class Ball(pygame.sprite.Sprite):
    '''
        Simple ball that bounces against the player's paddles
    '''
    def __init__(self):
        # -- Call parent's constructor
        super(Ball, self).__init__()

        # -- Create a simple surface to represent the ball
        self.image = image = pygame.Surface(BALL_SIZE)
        self.rect = image.get_rect()

        # -- Put the ball at the center
        self.center()

        # -- Give the ball a initial speed
        self.push()        

    def acelerate(self):
        self.dx *= (-1.5)

    def push(self):
        self.dx = (random.random() + 1) * ((-1) ** random.randrange(1, 3))
        self.dy = (random.random() + 1) * ((-1) ** random.randrange(1, 3))

    def center(self):
        ''' Put the ball at the center of the screen '''
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2

    def update(self):
        # -- Move the ball
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # -- If it hits the ceil
        if self.rect.y <= 0 or (self.rect.y + self.rect.height) >= SCREEN_HEIGHT:
            self.dy *= (-1.1)
            self.dx *= (1.1)
        
    def draw(self, screen):
        screen.fill( BLACK, self.rect)

#########################################################################################
#
#   # # # #      # #     #     #     # # #
#   #      #   #    #    # #   #    #      
#   # # # #   #      #   #  #  #   #    # #
#   #         #     #    #   # #   #      #
#   #           # #      #     #    # # # 
#
##########################################################################################

class Pong():
    '''
        Simple pong game implementation 
    '''
    def __init__(self):
        # -- Init game
        self.running = True

        # -- General timeout for other things to be done
        self.timeout = (1 / 60)

        # -- Topics to notify users
        self.topics = {}

    def subscribe(self, who, topics):
        for what in topics:
            if what in self.topics:
                self.topics[what].append(who)
            else:
                self.topics[what] = [ who ]

    async def run(self, screen):        
        # -- Init things
        await self.onInit(screen)

        clock = pygame.time.Clock()

        # -- Game main loop
        while self.running:
            # -- Notify subscribers about new events
            quit = await self.onEvent()
            
            # -- If quit is True, break the loop
            if quit: break

            # -- Give a chance for game objects to update
            await self.onUpdate()

            # -- Give a chance for game objects to draw
            await self.onDraw(screen)

            # Give chance for other things to be done
            await asyncio.sleep(self.timeout)

    # -- Init all things before the game starts
    async def onInit(self, screen):
        # -- Create a human player and a machina to play against
        self.players = { 
            'human': Player(self),
            'machine': Machine(self)
        }

        # -- Create a simple ball to play
        self.ball = Ball()

        # -- Font for rendering scores
        pygame.font.init()
        self.font = pygame.font.SysFont('comicsansms', 72 * 2)

    # -- Notify all registered listeners about incoming events
    async def onEvent(self):
        for event in pygame.event.get():
            # -- If users closes the window, quit
            if event.type == pygame.QUIT:
                # -- Stop the program
                self.running = False
                # -- Return True saying that the loop must quit
                return True

            # -- Notify interesteds
            if event.type in self.topics:
                for interested in self.topics[event.type]:
                    interested.notify(event)

        # -- Return False saying that the program cna continue
        return False

    # -- Give a chance to objects to update themselves
    async def onUpdate(self):
        # -- First, let the players move
        for what, player in self.players.items():
            player.update(self.ball)

        # -- Then move the ball
        self.ball.update()

        # -- Check if ball hits some of the paddles
        for what, player in self.players.items():
            if pygame.sprite.collide_rect(self.ball, player):
                self.ball.acelerate()

        # If the ball is off the screen, who scores ?       
        # -- If it exits on left
        if self.ball.rect.x < 0:
            self.ball.center()
            self.ball.push()
            self.players['machine'].score += 1
       
        # -- If it exist on the right
        elif self.ball.rect.x > SCREEN_WIDTH:
            self.ball.center()
            self.ball.push()
            self.players['human'].score += 1

    # -- Give a chance to objects to draw themselves
    async def onDraw(self, screen):
        # -- Fill the screen in white
        screen.fill( WHITE)

        # Draw a line separating the two sides of the field
        start_pos = (SCREEN_WIDTH // 2, 0)
        end_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        width = 1
        pygame.draw.line(screen, BLACK, start_pos, end_pos, width)

        # -- Draw a black circle at the center
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        radius = int(math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT) // 4)
        width = 1
        pygame.draw.circle(screen, BLACK, center, radius, width)

        # -- Display the score
        (w, h) = center
        radius = radius // 3

        # ---- Human display and rect
        human_score = self.font.render( str(self.players['human'].score), True, GREEN)
        human_score_rect = human_score.get_rect()
        screen.blit(human_score, (w - human_score_rect.width - radius, h - radius // 2))
        
        # ---- Machine display and rect
        machine_score = self.font.render( str(self.players['machine'].score), True, GREEN)
        machine_score_rect = machine_score.get_rect()
        screen.blit(machine_score, (w  + radius, h - radius // 2))
        
        # -- Draw the player's position
        for what, player in self.players.items(): 
            player.draw(screen)

        # -- Draw the ball
        self.ball.draw(screen)

        # -- Draw everything on the screen
        pygame.display.flip()

    def quit(self):
        # -- Stop the main loop
        self.running = False

        # -- Quit pygame.font
        pygame.font.quit()

        # -- Wait for it to close
        time.sleep(0.25)

#########################################################################################
#
#       #     #          #       #    #       #
#      # #   # #        # #      #    # #     #
#     #   # #   #      #   #     #    #   #   #
#    #     #     #    # # # #    #    #     # #
#   #      #      #  #       #   #    #       #
#
##########################################################################################

def main(loop):
    try:
        # -- Create game
        game = Pong()
        
        # -- Init pygame
        pygame.init()
        pygame.display.set_caption('Pong')
        screen = pygame.display.set_mode(SCREEN_SIZE)

        # Run game until something happens
        loop.run_until_complete( game.run(screen))

    except KeyboardInterrupt:
        # -- Quit game ( blocking )
        game.quit()
    
    finally:
        # -- Quit pygame
        pygame.quit()

        # -- Quit asyncio
        loop.close()

if __name__ == '__main__':
    main( asyncio.get_event_loop())