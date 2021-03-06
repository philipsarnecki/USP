'''
Image filtering

@author: Damares Resende
@contact: damaresresende@usp.br
@since: Apr 13, 2019

@organization: University of Sao Paulo (USP)
    Institute of Mathematics and Computer Science (ICMC)
    Image Processing Class (SCC5830)
'''
import imageio
import numpy as np
from math import sqrt


class FilterFactory:
    @staticmethod
    def init_filter(method):
        '''
        Returns an object with the filter implementation specified
        
        @return filter
        '''
        if method == 1:
            return LimiarFilter()
        if method == 2:
            return Filter1D()
        if method == 3:
            return LimiarFilter2D()
        if method == 4:
            return MedianFilter2D()


class IMGFiltering:
    def normalize(self, img):
        '''
        Normalizes image in values between 0 and 255
        
        @param img: 2D numpy array to normalize
        '''
        imax = np.max(img)
        imin = np.min(img)
        
        # if both images are of type uint8, any operation on them will be truncated to
        # uint8. However, to calculate the RMSE I cannot truncate the values. So, at least
        # one of the images must accept negative values (to compute the difference), and
        # large integers (to compute the multiplication). Hence, I am converting it to int32
        # instead of uint8
        
        return ((img-imin)/(imax-imin) * (pow(2, 8) - 1)).astype(np.int32)
    
    def calc_rmse(self, img1, img2):
        '''
        Computes RMSE in between two images
        
        @param img1: 2D numpy array
        @param img2: 2D numpy array
        @return integer with RMSE value
        '''
        mse = np.sum(np.multiply(img1 - img2, img1 - img2)) / (img1.shape[0] * img1.shape[1])
        return round(sqrt(mse), 4)

    def find_optimum_threshold(self, img):
        '''
        Updates the threshold until an optimum value is found
        
        @param img: image to check pixel values
        @return optimum value for the threshold
        '''
        optimum_t = self.threshold
        
        while True: 
            g1_sum = 0.0
            g1_count = 0.0
            
            g2_sum = 0.0
            g2_count = 0.0
            
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i][j] > optimum_t:
                        g1_sum += img[i][j]
                        g1_count += 1
                    else:
                        g2_sum += img[i][j]
                        g2_count += 1
                        
            new_t = (g1_sum/g1_count + g2_sum/g2_count) / 2.0
            if new_t - optimum_t <= 0.5:
                return new_t
            else:
                optimum_t = new_t
        return optimum_t
    
    def limiar_filter(self, img):
        '''
        Applies limiar filter to image
        
        @param img: image to be filtered
        @return filtered image
        '''        
        optimum_t = self.find_optimum_threshold(img)
        
        new_img = np.copy(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j] > optimum_t:
                    new_img[i][j] = 1
                else:
                    new_img[i][j] = 0
        
        return new_img


class LimiarFilter(IMGFiltering):
    def __init__(self):
        '''
        Reads inputs
        '''
        self.threshold = int(input()) 
        
    def apply_filter(self, img):
        '''
        Applies filter to image
        
        @param img: image to be filtered
        @return filtered image
        '''        
        return self.limiar_filter(img)
    

class Filter1D(IMGFiltering):
    def __init__(self):
        '''
        Reads inputs
        '''
        self.size = int(input())
        self.weights = np.zeros((self.size,))
        
        for i, value in enumerate(input().strip().split(' ')):
            self.weights[i] = int(value)
            
    def apply_filter(self, img):
        '''
        Transforms the image in a 1D vector, applies 1D convolution with the specified weights 
        and transforms the array to a 2D array again
        
        @param img: image to be filtered
        @return filtered image
        '''
        padding = int((self.size-1) / 2)
        img_1D = self.create_circular_array(img)
        result = np.zeros((img.shape[0] * img.shape[1],))
        
        weights = np.flip(self.weights)
        for k in range(padding, img.shape[0] * img.shape[1] + 1):
            result[k-1] = sum(np.multiply(weights, img_1D[k-1:k+self.size-1]))
            
        return np.reshape(result, img.shape)
        
    def create_circular_array(self, img):
        '''
        Transform a 2D image into a 1D array and pads the borders with values of the circular array
        
        @param img: image to transform to 1D
        @return 1D circular array with image
        ''' 
        padding = int((self.size-1) / 2)
        aux = np.reshape(img, img.shape[0] * img.shape[1])
        img_1D = np.zeros(img.shape[0] * img.shape[1] + 2 * padding)
        
        img_1D[padding:-padding] = aux
        img_1D[0:padding] = aux[-padding:]
        img_1D[-padding:] = aux[0:padding]
        
        return img_1D


class LimiarFilter2D(IMGFiltering):
    def __init__(self):
        '''
        Reads inputs
        '''
        self.size = int(input())
        self.weights = np.zeros((self.size, self.size))
        
        for i in range(self.size):
            for j, v in enumerate(input().strip().split(' ')):
                self.weights[i][j] = int(v)
        
        self.threshold = int(input())
        
    def simple_filter(self, img):
        '''
        Applies convolution to the image with the specified weights
        '''
        img = img.astype(np.int32)
        new_img = np.copy(img)
        padding = int((self.size-1) / 2)
        weights = np.flip(np.flip(self.weights, 0), 1)
        
        for i in range(padding, img.shape[0] - padding):
            for j in range(padding, img.shape[1] - padding):
                new_img[i][j] = np.sum(np.multiply(weights, img[i-padding:i+padding+1, j-padding:j+padding+1]))
                
        return new_img
        
    def apply_filter(self, img):
        '''
        Applies convolution to the image with the specified weights and later a limiar filter
        
        @param img: image to be filtered
        @return filtered image
        '''
        return self.limiar_filter(self.simple_filter(img))
    

class MedianFilter2D(IMGFiltering):
    def __init__(self):
        '''
        Reads inputs
        '''
        self.size = int(input())

    def apply_filter(self, img):
        '''
        Replaces the value of a pixel by the mean value of it's neighborhood
        
        @param img: image to be filtered
        @return filtered image
        '''
        padding = int((self.size-1) / 2)
        
        aux_img = np.zeros((img.shape[0] + 2 * padding, img.shape[1] + 2 * padding))
        aux_img[padding:-padding, padding:-padding] = img
        new_img = np.zeros((img.shape))
        middle = int((self.size * self.size - 1)/2)
        
        for i in range(padding, img.shape[0] + 1):
            for j in range(padding, img.shape[1] + 1):
                neighborhood = aux_img[i-padding:i+padding+1, j-padding:j+padding+1]
                new_img[i-padding][j-padding] = sorted(neighborhood.reshape(self.size * self.size))[middle]
        
        return new_img


def run_filtering():
    '''
    Applies filter according to specified parameters 
    '''
    img_name = str(input()).rstrip()
    method = int(input())
     
    img = imageio.imread(img_name) # img is of type uint8
    filt = FilterFactory.init_filter(method)
    filtered_img = filt.apply_filter(img)
    rmse = filt.calc_rmse(img, filt.normalize(filtered_img)) # result of normalization is of type int32
    
    return img, filtered_img, rmse

def main():
    _, _, rmse = run_filtering()
    print(rmse)
    
if __name__ == '__main__':
    main()    


