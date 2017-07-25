# -*- coding: utf-8 -*-

'''
Created on 15 de jul de 2017

@author: lucas
'''

import pygame
import time
import random

import snake
import apple

class Game():
    '''
    Classe mais básica da aplicação, responsável pela criação do componentes
    e também do loop principal da aplicação
    '''
    def __init__(self):
        '''
        Construtor da classe
        '''
        
        # Tamanho da tela, usado pelas componentes durante a inicialização para um tamanho relativo
        self.size = (self.width, self.height) = (640, 480)
        
        # Dicionário de objetos da aplicação
        self.objects = self.createObjects()
                
    def createObjects(self):
        ''' Cria os objetos da aplicação '''
        return {
            # Objeto da snake
            'snake': snake.Snake(),
            
            # Fábrica de maçãs
            'apple': apple.Apple(),
        }
    
    def newApple(self):
        ''' Muda a posição da maçã '''
                
        # Vê se a maçã não está sobre a snake
        done = False
        while not done:
            done = True
            position = random.randrange(self.width), random.randrange(self.height)
            self.objects['apple'].changePosition(position)
            for segment in self.objects['snake'].segment_list:
                if pygame.sprite.collide_rect(segment, self.objects['apple']):
                    done = False
                    break
                
    def run(self):
        ''' Entra no loop principal '''        
        # Inicia pygame
        pygame.init()
        
        # Inicia o display e cria uma tela para renderizar os objetos
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Snake')
        
        # Inicia todos os objetos do jogo
        for obj in self.objects.values():
            obj.onInit(self)
        
        ###############################################################     
        # Variáveis para controle de tempo
        ############################################################### 
        
        # -- Retorna o tempo passado deste o início da aplicação em ms
        def GetTickCount():
            ''' Retorna o tempo passado desde o início da aplicação em ms '''
            return time.clock() * 1000
        
        # -- Quantos updates por segundo a snake faz
        updates_per_second = 8
        
        # -- Intervalo de tempo entre uma atualização e outra
        skip_ticks = 1000 / updates_per_second
        
        # -- Quantos frames são 'puladas' em caso de lag muito grande
        max_frameskip = 5
        
        # -- Variável que armazena quando será a próxima atualização
        next_game_tick = GetTickCount()
        
        ############################################################### 
        # Loop principal
        ############################################################### 
        
        # Cria uma nova maçã para o início do jogo
        self.newApple()

        done = False
        while not done:
            
            ############################################################### 
            # Recebe eventos
            ############################################################### 
            for evt in pygame.event.get():
                
                # -- Se for evento de saída, encerra a aplicação
                if evt.type == pygame.QUIT:
                    done = True
                    
                # -- Se não, distribui pelos objetos da aplicação
                else:
                    for obj in self.objects.values():
                        obj.onEvent(evt)
            
            ###############################################################
            # Atualiza os objetos da aplicação
            ###############################################################            
            
            # -- A 'snake' só é atualizada em um intervalo de 0.2s
            loops = 0
            while GetTickCount() > next_game_tick and loops < max_frameskip:
            
                # Atualiza a snake
                self.objects['snake'].onUpdate(self)
                
                # Vê quando será a próxima atualização e soma o contador para que não trave no loop em caso de lag
                next_game_tick += skip_ticks
                loops += 1
                
            # -- Vê se a 'snake' comeu a maçã
            if self.objects['snake'].ate( self.objects['apple'] ):
                
                # Atualiza o score
                
                
                # Cria uma nova maçã
                self.newApple()
                
                # Cresce a snake
                self.objects['snake'].addSegment()
                
            # -- Vê se a 'snake' colidiu consigo mesma
            if not self.objects['snake'].isAlive():
                # Zera o placar
                
                # Reseta a snake
                self.objects['snake'].onInit(self)
                
                # Espera 2s
                time.sleep(2)
            
            ############################################################### 
            # Renderiza os objetos da aplicação
            ############################################################### 
            
            # -- Limpa a tela antes
            black = (0x00, 0x00, 0x00)
            screen.fill(black)
            for obj in self.objects.values():
                obj.onDraw(screen)
                
            # -- Atualiza o display
            pygame.display.flip()
            
        ###############################################################                 
        # Finaliza os objetos antes de encerrar a aplicação
        ############################################################### 
        
        # -- Finaliza todos os objetos
        for obj in self.objects.values():
            obj.onQuit(self)
            
def main():
    # Cria o objeto do jogo e inicia
    game = Game()
    game.run()

if __name__ == '__main__':
    main()