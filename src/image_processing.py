import os,sys
import math, operator
from functools import reduce
from PIL import Image, ImageChops

class ImageProcessing:

    def getfilename(self, filepath):
        return os.path.basename(filepath).split(".")[0]

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
        print("image diff:{}".format(res))
        return res
    
    def widespace_remover(self,image):
        '''
        Remove widespace before and after text
        '''
        im = self.checkImageOrObject(image)
        if im: 
            bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
            diff = ImageChops.difference(im, bg)
            # diff = ImageChops.add(diff, diff, 2.0, -100)
            bbox = diff.getbbox()
            if bbox:
                return im.crop(bbox)
    
    def split_image(self, base_imagelist, global_config):
        '''
        This method will split single into multiple test-case images 
        '''
        result_list = list()
        for count in range(int(len(base_imagelist)/2)):
            
            split_image_list    = list()
            
            imagename1          = self.getfilename(base_imagelist[count])
            imagename2          = self.getfilename(base_imagelist[count+int(len(base_imagelist)/2)])

            img1                = self.checkImageOrObject(base_imagelist[count])        
            img2                = self.checkImageOrObject(base_imagelist[count+int(len(base_imagelist)/2)])
            
            # check if image path or object was invalid
            if img1 and img2:
                cropped_text1       = self.widespace_remover(img1)
                cropped_text2       = self.widespace_remover(img2)
                
                width, height       = cropped_text1.size
                
                for line_number in range(global_config["no_of_test_case"]):

                    box = (0, line_number*(height/global_config["no_of_test_case"]), width, height/global_config["no_of_test_case"]*(line_number+1))
                    
                    cropped_image1 = cropped_text1.crop(box)
                    cropped_image1 = self.widespace_remover(cropped_image1)
                    
                    cropped_image2 = cropped_text2.crop(box)
                    cropped_image2 = self.widespace_remover(cropped_image2)

                    cropped_image1.save("{}/{}_{}".format(global_config["cropped_img_dir"], imagename1, line_number),format=global_config["image_file_extension"])
                    cropped_image2.save("{}/{}_{}".format(global_config["cropped_img_dir"], imagename2, line_number),format=global_config["image_file_extension"])
                    
                    # check if images are same or not as per threshold specified 
                    if self.check_image_diff(cropped_image1, cropped_image2) > global_config["diff_threshold"]:
                        # merge both error into single image 
                        img = self.merge_image(cropped_image1, cropped_image2)
                        outfilename = "{}/{}_{}".format(global_config["result_img_dir"], imagename1+imagename2, line_number)
                        img.save(outfilename ,format=global_config["image_file_extension"])
                        result_list.append(outfilename)
                return result_list 
                

    def merge_image(self, img1, img2):
        image1 = self.checkImageOrObject(img1)
        image2 = self.checkImageOrObject(img2)
        
        if image1 and image2:
            width_1, height_1 = image1.size
            width_2, height_2 = image2.size
            # create a blank image with white background 
            new_im = Image.new(mode="RGB", size=(width_1, height_1+height_2+25), color=(255,255,255,255))        
            new_im.paste(image1, (0,10))
            new_im.paste(image2, (0,height_1+15))
            return new_im

    