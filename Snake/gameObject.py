'''
Created on 16 de jul de 2017

@author: lucas
'''

import pygame
import abc
from bs4.tests.test_docs import __metaclass__

def error_msg(function, cls):
    ''' Mensagem de erro para função não implementada '''
    return 'Função {} não implementada para a classe {}'.format(function, cls.__class__.__name__)

class GameObject(pygame.sprite.Sprite):
    '''
    Interface de objeto genérico da aplicação
    '''

    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        '''
        Construtor da classe
        '''
        
        # Construtor da classe
        super(GameObject, self).__init__()
        
    @abc.abstractclassmethod
    def onInit(self, world):
        '''
        Inicia o objeto
        :param world: Objeto contendo informações gerais sobre a aplicação
        '''
        raise NotImplementedError(error_msg('onInit', self))
    
    
    @abc.abstractclassmethod
    def onUpdate(self, world):
        '''
        Atualiza o objeto
        :param world: Objeto contendo informações gerais sobre a aplicação
        '''
        raise NotImplementedError(error_msg('onUpdate', self))
    
    @abc.abstractclassmethod
    def onEvent(self, evt):
        '''
        Recebe um evento do sistema
        :param evt: Objeto contendo informações sobre o evento
        '''
        raise NotImplementedError(error_msg('onEvent', self))
    
    @abc.abstractclassmethod
    def onDraw(self, screen):
        '''
        Renderiza o objeto na tela
        :param screen: Tela para renderizar o objeto
        '''
        raise NotImplementedError(error_msg('onDraw', self))
        
    @abc.abstractclassmethod
    def onQuit(self, world):
        '''
        Destrói o objeto antes de finalizar a aplicação
        :param world: Objeto contendo informações gerais sobre a aplicação
        '''
        raise NotImplementedError(error_msg('onQuit', self))