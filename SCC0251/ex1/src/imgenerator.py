'''
Image generator

@author: Damares Resende
@contact: damaresresende@usp.br
@since: Mar 17, 2019

@organization: University of Sao Paulo (USP)
    Institute of Mathematics and Computer Science (ICMC)
    Image Processing Class (SCC0251)
'''

import random
import numpy as np
from math import sin, cos, pow, floor


class IMGenerator():
    
    def __init__(self, r, C, f, Q, N, B, S):
        '''
        Initialize main variables. r, C, f, Q, N, B, S
        
        @param r: reference image path
        @param C: scene size
        @param f: function
        @param Q: weight
        @param N: image size
        @param B: number of bits per pixel
        @param S: random number seed
        '''
        self.r = r
        self.C = C
        self.f = f
        self.Q = Q
        self.N = N
        self.B = B
        self.S = S
        
    def __call__(self):
        '''
        Generates images
        '''
        if self.f == 1:
            return self.func_one()
        if self.f == 2:
            return self.func_two()
        if self.f == 3:
            return self.func_three()
        if self.f == 4:
            return self.func_four()
        if self.f == 5:
            return self.func_five()

    def func_one(self):
        '''
        Function 1: generates images from f(x,y) = (xy + 2x)
        '''
        img = np.ones((self.C, self.C), dtype='float32')
        
        for x in range(self.C):
            for y in range(self.C):
                img[x][y] = x * y + 2 * y
        
        return img
    
    def func_two(self):
        '''
        Function 2: generates images from f(x,y) = |cos(x/Q + 2sin(y/Q)|
        '''
        img = np.ones((self.C, self.C), dtype='float32')
        
        for x in range(self.C):
            for y in range(self.C):
                img[x][y] = abs(cos(x / self.Q) + 2 * sin(y / self.Q))
                                
        return img
    
    def func_three(self):
        '''
        Function 3: generates images from f(x,y) = |3(x/Q) - (y/Q) ^ (1/3)|
        '''
        img = np.ones((self.C, self.C), dtype='float32')
        
        for x in range(self.C):
            for y in range(self.C):
                img[x][y] = abs(3 * (x / self.Q) - pow(y/self.Q, 1/3))
                                
        return img
    
    def func_four(self):
        '''
        Function 4: generates images from f(x,y) = random(0,1,S)
        '''
        random.seed(self.S)
        img = np.ones((self.C, self.C), dtype='float32')
        
        for x in range(self.C):
            for y in range(self.C):
                img[x][y] = random.randint(0, 1)
                                
        return img
    
    def func_five(self):
        '''
        Function 5: generates images from f(x,y) = randomwalk(S)
        '''
        random.seed(self.S)
        img = np.zeros((self.C, self.C), dtype='float32')
        
        x = 0
        y = 0
        for _ in range(0, 1 + self.C * self.C):
                x = (x + random.randint(-1,1)) % self.C
                y = (y + random.randint(-1,1)) % self.C
                img[x][y] = 1
                                
        return img
    
    def normalize(self, img, B):
        '''
        Normalizes image in values between 0 and 2^B - 1
        
        @param img: 2D numpy array to normalize
        @param B: number of bits to define normalization maximum
        '''
        imax = np.max(img)
        imin = np.min(img)
        
        return (img-imin)/(imax-imin) * (pow(2, B) - 1)  
    
    def downsampling(self, img):
        '''
        Reduces the resolution of the input image
        
        @param img: 2D numpy array to reduce dimensions
        '''
        new_img = np.zeros((self.N, self.N))
        
        for x in range(0, self.N):
            for y in range(0, self.N):
                new_img[x][y] = img[floor(x * self.C / self.N)][floor(y * self.C / self.N)]
            
        return new_img
