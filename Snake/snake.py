'''
Created on 16 de jul de 2017

@author: lucas
'''

import pygame

from gameObject import GameObject

class SnakeSegment(pygame.sprite.Sprite):
    '''
    Segmento da snake
    '''
    def __init__(self, position, size, direction):
        '''
        Construtor da classe
        '''
        
        # Construtor da classe mãe
        super(SnakeSegment, self).__init__()
        
        # Salva a direção atual da snake
        self.direction = direction
        
        # Cria o retângulo do segmento
        self.image = image = pygame.Surface(size)
        self.rect = image.get_rect()
        
        # Posiciona a snake
        (x, y) = position
        self.rect.x = x
        self.rect.y = y
        
    def move(self, world):
        ''' Move o segmento na direção atual '''
        
        if self.direction == 'up':
            # Move-se para cima
            self.rect.y -= self.rect.height
            
            # Se chegou ao topo da tela, vai para o fundo
            if self.rect.y < 0:
                self.rect.y = world.height
                
        elif self.direction == 'down':
            # Move-se para baixo
            self.rect.y += self.rect.height
            
            # Se chegou ao fundo da tela, vai para o topo
            if (self.rect.y + self.rect.height) > world.height:
                self.rect.y = 0
                
        elif self.direction == 'left':
            # Move-se para esquerda
            self.rect.x -= self.rect.width
            
            # Se chegou à esquerda da tela, vai para a direita
            if self.rect.x < 0:
                self.rect.x = world.width
                
        elif self.direction == 'right':
            # Move-se para direita
            self.rect.x += self.rect.width
            
            # Se chegou à direita da tela, vai para a esquerda
            if (self.rect.x + self.rect.width) > world.width:
                self.rect.x = 0
    
class Snake(GameObject):
    '''
    Snake controlável pelo jogador
    '''

    def __init__(self):
        '''
        Construtor da classe
        '''
        
        # Construtor da classe mãe
        super(Snake, self).__init__()
        
    def snakeHead(self):
        ''' Retorna a cabeça da snake '''
        return self.segment_list[0]
    
    def isAlive(self):   
        ''' Retorna False se a cabeça da snake colidiu com algum dos seus segmentos '''
        
        for n, snakeSegment in enumerate(self.segment_list):
            # Pula o primeiro elemento
            if n == 0:                
                continue
            # Vê se colide com algum dos segmentos da snake
            elif pygame.sprite.collide_rect(self.snakeHead(), snakeSegment):
                return False
        return True
    
    def ate(self, apple):
        ''' Retorna true se a snake comeu a maçã '''
        
        if pygame.sprite.collide_rect(self.snakeHead(), apple):
            return True
        else:
            return False
        
    def addSegment(self):    
        ''' Adiciona um novo segmento ao final da snake '''
        
        # Referência ao último segmento da lista
        last_segment = self.segment_list[-1]
        
        # Cria um novo segmento
        size = self.segment_size
        position = (last_segment.rect.x, last_segment.rect.y)
        direction = last_segment.direction
        new_segment = SnakeSegment(position, size, direction)
        
        # Coloca ele atŕas do último
        if last_segment.direction == 'up':
            new_segment.rect.y += new_segment.rect.height
        
        elif last_segment.direction == 'down':
            new_segment.rect.y -= new_segment.rect.height
        
        elif last_segment.direction == 'left':
            new_segment.rect.x += new_segment.rect.width
        
        elif last_segment.direction == 'right':
            new_segment.rect.x -= new_segment.rect.width
        
        # Insere no vetor
        self.segment_list.append(new_segment)

    def onInit(self, world):
        ''' Inicia a snake '''
        
        # Cria uma nova lista de segmentos da snake
        self.segment_list = []

        # Tamanho default de cada segmento
        self.segment_size = (world.width // 32, world.height // 24)
    
        # Cria a cabeça da snake
        size = self.segment_size
        position = (world.width // 2, world.height // 2)
        direction = 'right'
        self.segment_list.append(SnakeSegment(position, size, direction))
            
        # Cria três segmentos
        for _ in range(3):
            self.addSegment()
            
    def onEvent(self, evt):
        ''' Muda a direção do movimento da snake de acordo com o input '''

        # Se for um evento de tecla pressionada
        if evt.type == pygame.KEYDOWN:
                
            # Seta para cima
            if evt.key == pygame.K_UP:
                
                # Se não estiver indo para baixo
                if self.snakeHead().direction != 'down':
                    self.snakeHead().direction = 'up'
            
            # Seta para baixo
            elif evt.key == pygame.K_DOWN:
                
                # Se não estiver indo para cima
                if self.snakeHead().direction != 'up':
                    self.snakeHead().direction = 'down'
            
            # Seta para esquerda
            elif evt.key == pygame.K_LEFT:
                
                # Se não estiver indo para direita
                if self.snakeHead().direction != 'right':
                    self.snakeHead().direction = 'left'
            
            # Seta para direita
            elif evt.key == pygame.K_RIGHT:
                
                # Se não estiver indo para esquerda
                if self.snakeHead().direction != 'left':
                    self.snakeHead().direction = 'right'
            
            # Barra de espaço, cria um novo segmento da snake, usado para debug
            elif evt.key == pygame.K_SPACE:
                
                # Cria um novo segmento
                self.addSegment()
             
    def onUpdate(self, world):
        ''' Move a snake '''
        
        # Move todas os segmentos e muda o movimento de acordo com o próxim segmento
        for n in range(len(self.segment_list)-1, 0, -1):
            self.segment_list[n].move(world)
            self.segment_list[n].direction = self.segment_list[n-1].direction
            
        # Move a cabeça da snake
        self.snakeHead().move(world)
        
    def onDraw(self, screen):
        ''' Renderiza todas as componentes na tela '''
        # Cores usadas para renderizar
        blue = (0x00, 0x00, 0xff)
        green = (0x00, 0xff, 0x00)
        
        for n, segment in enumerate(self.segment_list):

            # Renderiza a cabeça da snake em azul
            if n == 0:
                color = blue
                
            # Renderiza o resto do corpo em verde
            else:
                color = green
            
            # Renderiza o segmento
            screen.fill(color, segment.rect)
        
    def onQuit(self, world):
        pass
    
    