import os,sys
import math, operator
from functools import reduce
from PIL import Image, ImageChops, ImageEnhance
from lib.image_processing import ImageProcessing

class FontTest(ImageProcessing):

    def __init__(self,font_file_list, font_size_list, test_file):
        self.debug                  = True
        self.image_file_extension   = "PNG"
        self.diff_threshold         = 0.0
        self.font_file_list         = font_file_list
        self.font_size_list         = font_size_list
        self.test_file              = test_file
        self.no_of_test_case        = sum(1 for line in open(self.test_file))
        self.cropped_img_dir        = "./tmp/cropped_images"
        self.result_img_dir         = "./tmp/result_images"
        if not os.path.exists(self.cropped_img_dir): 
            os.makedirs(self.cropped_img_dir)
        if not os.path.exists(self.result_img_dir):
            os.makedirs(self.result_img_dir)
            
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

    def render(self, font_file_list, font_size_list):
        file_list = list()
        for i in range(len(font_file_list)):
            for size in font_size_list:
                # hb-view --font-file=filename --text=string --output-file=filename --output-format=format --font-size=10
                output_filename = "{}_{}_{}".format("./tmp/outputfile", str(i), str(size))
                cmd = "hb-view \
                    --font-file={} \
                    --text-file={} \
                    --output-file={} \
                    --output-format={} \
                    --font-size={}".format(font_file_list[i], self.test_file, output_filename, self.image_file_extension, size)
                os.system(cmd)
                file_list.append(output_filename)
        return file_list

    def merge_image(self, img1, img2):
        image1 = self.checkImageOrObject(img1)
        image2 = self.checkImageOrObject(img2)
        width_1, height_1 = image1.size
        width_2, height_2 = image2.size
        # create a blank image with white background 
        new_im = Image.new(mode="RGB", size=(width_1, height_1+height_2+25), color=(255,255,255,255))        
        new_im.paste(image1, (0,10))
        new_im.paste(image2, (0,height_1+15))
        # new_im.save("test",format=self.image_file_extension)
        return new_im

    def compute(self):
        # Render all fonts in all specified sizes 
        font_render_list = self.render(self.font_file_list, self.font_size_list)
        if self.debug:
            print("total image file created: {}".format(len(font_render_list)))
            print("file location list: {}".format(font_render_list))

        # font_render_list has list of rendered fontfile image names from both the font files  
        for i in range(int(len(self.font_size_list))):
            # first half is fontfile one and second half is fontfile two
            font_obj1 = self.checkImageOrObject(font_render_list[i])
            font_obj2 = self.checkImageOrObject(font_render_list[i+int(len(self.font_size_list))])
            
            # check if both the images are same or not as per threshold specified
            if self.check_image_diff(font_obj1,font_obj2) > self.diff_threshold:
                # split single image into multiple sub test-case images 
                font_obj1_list = self.split_image(font_obj1, image_no=1, file_no=i, size_no=self.font_size_list[i])
                font_obj2_list = self.split_image(font_obj2, image_no=2, file_no=i, size_no=self.font_size_list[i])
                
                if self.debug:
                    print("Two font list which has single testcase image\n{}\n{}".format(font_obj1_list,font_obj2_list))
                
                for j in range(self.no_of_test_case):
                    # check if images are same or not as per threshold specified 
                    if self.check_image_diff(font_obj1_list[j], font_obj2_list[j]) > self.diff_threshold:
                        # merge both error into single image 
                        img = self.merge_image(font_obj1_list[j],font_obj2_list[j])
                        img.save("{}/{}_{}_{}".\
                            format(self.result_img_dir, "resultfile", j, self.font_size_list[i]),format=self.image_file_extension)                
            else:
                print("{} & {} both files have no diff".\
                    format(font_render_list[i], font_render_list[i+int(len(font_render_list)/2)]))


if __name__ == "__main__":
     
    font_file_list = ["/usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf","/usr/share/fonts/lohit-marathi/Lohit-Marathi.ttf"]
    font_size_list = [10,100,256]
    test_file = "test.txt"
    obj = FontTest(font_file_list, font_size_list, test_file)    
    obj.compute()
    