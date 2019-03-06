import os,sys
import math, operator
from functools import reduce
from PIL import Image, ImageChops

class ImageProcessing:
            
    def checkImageOrObject(self, src_image):
        '''
        This method will check if the parameter "src_image" is image file path or image object  
        '''
        try:
            if type(src_image) == str:
                if not os.path.exists(src_image):
                    print("{} : invalid image path given".format(src_image))
                    return False
                else:
                    return Image.open(src_image)
            else:
                return src_image
        except Exception as e:
            print(e)

    def check_image_diff(self, image_1, image_2):
        '''
        This method will check if two images are different and return diff count 
        '''
        image_h1 = self.checkImageOrObject(image_1).histogram()
        image_h2 = self.checkImageOrObject(image_2).histogram()
        res = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, image_h1, image_h2))/len(image_h1))
        if self.debug:
            print("image diff:{}".format(res))
        return res
    
    def widespace_remover(self,image):
        '''
        Remove widespace before and after text
        '''
        im = self.checkImageOrObject(image)
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        # diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox)
    

    def split_image(self, image, image_no=0, file_no=0, size_no=0):
        '''
        This method will split single into multiple test-case images 
        '''
        split_image_list    = list()
        im                  = self.checkImageOrObject(image)        
        cropped_text        = self.widespace_remover(im)
        width, height       = cropped_text.size
        
        for line_number in range(self.no_of_test_case):
            box = (0, line_number*(height/self.no_of_test_case), width, height/self.no_of_test_case*(line_number+1))
            cropped_image = cropped_text.crop(box)
            cropped_image = self.widespace_remover(cropped_image)
            split_image_list.append(cropped_image)
            if self.debug:
                cropped_image.save("tmp/cropped_images/cropped_image_{}_{}_{}_{}".\
                    format(image_no, file_no, line_number, size_no), format=self.image_file_extension)
        return split_image_list

    def merge_image(self, img1, img2):
        image1 = self.checkImageOrObject(img1)
        image2 = self.checkImageOrObject(img2)
        width_1, height_1 = image1.size
        width_2, height_2 = image2.size
        # create a blank image with white background 
        new_im = Image.new(mode="RGB", size=(width_1, height_1+height_2+25), color=(255,255,255,255))        
        new_im.paste(image1, (0,10))
        new_im.paste(image2, (0,height_1+15))
        return new_im

    