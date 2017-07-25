'''
Created on 16 de jul de 2017

@author: lucas
'''
from gameObject import GameObject
import pygame

class Apple(GameObject):
    '''
    Maçã que é gerada em posição aleatória do mapa e gera pontos ao jogador
    '''


    def __init__(self):
        '''
        Construtor da classe
        '''
        
        # Construtor da classe mãe
        super(Apple, self).__init__()
    
    def changePosition(self, position):
        ''' Muda a posição da maçã '''
        (x, y) = position
        self.rect.x = x
        self.rect.y = y
        
    def onInit(self, world):
        ''' Inicia a maçã '''
        
        # Tamanho da maçã
        self.size = size = (world.width // 32, world.height // 24)
        
        # Cria o retângulo da maçã
        self.image = image = pygame.Surface(size)
        self.rect = image.get_rect()
            
    def onEvent(self, evt):
        pass
    
    def onUpdate(self, world):
        pass
    
    def onDraw(self, screen):
        ''' Renderiza a maçã na tela '''
        red = (0xff, 0x00, 0x00)
        screen.fill(red, self.rect)
        
    def onQuit(self, world):
        pass 