import warnings
import os,sys
import math, operator
from functools import reduce
from PIL import Image, ImageChops, ImageDraw
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

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
        image_1 = self.widespace_remover(image_1)
        image_2 = self.widespace_remover(image_2)

        image_h1 = self.checkImageOrObject(image_1).histogram()
        image_h2 = self.checkImageOrObject(image_2).histogram()
        res = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, image_h1, image_h2))/len(image_h1))
        print("image diff:{}".format(res))

        ImageChops.difference(image_1,image_2).save("/tmp/aa.png")
        return res


    def widespace_remover(self,image):
        '''
        Remove widespace before and after text
        '''
        im = self.checkImageOrObject(image)
        if im: 
            bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
            diff = ImageChops.difference(im, bg)
            diff = ImageChops.add(diff, diff, 2.0, -100)
            bbox = diff.getbbox()
            if bbox:
                return im.crop(bbox)


    def crop_and_filter_image(self, image_path, global_config):
        '''
        This method will open image, crop image and remove widespaces. 
        split into multiple image chunk(as per no of testcases)
        and will return/yield (image_obj ,testcase line number) 
        '''
        img = self.checkImageOrObject(image_path)
        width, height  = img.size
        for line_number in range(global_config["no_of_test_case"]):
            box = (0, line_number*(height/global_config["no_of_test_case"]), width, height/global_config["no_of_test_case"]*(line_number+1))
            cropped_image = img.crop(box)
            cropped_image = self.widespace_remover(cropped_image)
            cropped_image.save("{0}/{1}_{2}".format(global_config["cropped_img_dir"], self.getfilename(image_path) , line_number),format=global_config["image_file_extension"])                 
            yield(cropped_image, line_number)


    def split_image(self, base_imagelist, global_config):
        '''
        This method will split single into multiple test-case images 
        '''
        result_list = list()
        
        for image1,image2 in zip(base_imagelist[:int(len(base_imagelist)/2)],base_imagelist[int(len(base_imagelist)/2):]):
            cropped_image1 = self.crop_and_filter_image(image1, global_config)
            cropped_image2 = self.crop_and_filter_image(image2, global_config)
            for glyph_img1, glyph_img2 in zip(cropped_image1,cropped_image2):

                if self.check_image_diff(glyph_img1[0], glyph_img2[0]) > global_config["diff_threshold"]:
                    # diff_box = ImageChops.difference(glyph_img1[0], glyph_img2[0]).getbbox()
                    # draw = ImageDraw.Draw(glyph_img2[0])                
                    # draw.rectangle(diff_box, outline="#8B0000")
                    # del draw

                    # # merge both error into single image 
                    img = self.merge_image(glyph_img1[0], glyph_img2[0])
                    outfilename = "{0}/{1}_{2}".format(global_config["result_img_dir"], self.getfilename(image1)+self.getfilename(image2), glyph_img1[1])
                    img.save(outfilename ,format=global_config["image_file_extension"])
                    result_list.append(outfilename)

        return result_list    


    def merge_image(self, img1, img2):
        '''
        This function will merge two error images into one
        '''
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