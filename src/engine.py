import os,sys
import math, operator
from functools import reduce
from PIL import Image, ImageChops
import git 
from src.image_processing import ImageProcessing

class Engine():

    def __init__(self, global_config):
        
        global_config["no_of_test_case"] = sum(1 for line in open(global_config["test_file"]))
        
        if not os.path.exists(global_config["cropped_img_dir"]): 
            os.makedirs(global_config["cropped_img_dir"])
        if not os.path.exists(global_config["result_img_dir"]):
            os.makedirs(global_config["result_img_dir"])

        self.global_config = global_config
        # call respective command method
        getattr(self, global_config["command"])(global_config)

    def render(self, font_filepath, font_sizelist, output_filename, testfile, imagefile_extension):
        '''
        This function will render test file using harfbuzz  
        '''
        file_list = list()
        for size in font_sizelist:
            # hb-view --font-file=filename --text=string --output-file=filename --output-format=format --font-size=10
            filename = "./tmp/{}_{}".format(output_filename,size)
        
            cmd = "hb-view \
                --font-file={} \
                --text-file={} \
                --output-file={} \
                --output-format={} \
                --font-size={}".format(font_filepath, testfile, filename, imagefile_extension, size)
            os.system(cmd)
            file_list.append(filename)
            
        return file_list

    def getfilename(self, filepath):
        return os.path.basename(filepath).split(".")[0]

    def fontdiff(self, global_config):
        '''
        This method will check for font version diff for given two fonts
        '''
        base_image_list = list() 
        for count in range(len(global_config["test_font_files"])):
            tmp = self.render(
                font_filepath = global_config["test_font_files"][count],
                font_sizelist = global_config["font_size_list"], 
                output_filename = "font{}_{}".format(count,self.getfilename(global_config["test_font_files"][count])), 
                testfile = global_config["test_file"], 
                imagefile_extension = global_config["image_file_extension"]
            )
            base_image_list.extend(tmp)
        
        obj = ImageProcessing()
        print(obj.split_image(base_image_list, global_config))

    def git_repoclone(self, global_config):
        '''
        This method will clone give repo
        '''
        dir_name = self.getfilename(global_config["git_url"])
        if os.path.exists("./tmp/"+dir_name) and os.path.isdir("./tmp/"+dir_name):	
            os.system("rm -rf ./tmp/"+dir_name)
        git.Git("./tmp/").clone(global_config["git_url"])
        
        return "./tmp/"+dir_name+"/fonttest"

    def fonttest(self, global_config):
        '''
        This method will clone/use local reference image and check for rendering errors
        '''
        ref_image_dir = None 
        if global_config["git_url"]:
            ref_image_dir = self.git_repoclone(global_config)
        else:
            ref_image_dir = global_config["local_ref_dir"]

        base_image_list = self.render(
            font_filepath = global_config["test_font_file"],
            font_sizelist = global_config["font_size_list"], 
            output_filename = "{}".format(self.getfilename(global_config["test_font_file"])), 
            testfile = global_config["test_file"], 
            imagefile_extension = global_config["image_file_extension"]
        )

        tmp_list = [ref_image_dir+"/"+ self.getfilename(fontfilename) for fontfilename in base_image_list]
        base_image_list.extend(tmp_list)
        
        obj = ImageProcessing()
        print(obj.split_image(base_image_list, global_config))


    def generate_reference_image(self, global_config):
        '''
        This method will generate refrence image 
        '''
        
        self.render(
            font_filepath = global_config["test_font_file"],
            font_sizelist = global_config["font_size_list"], 
            output_filename = "{}".format(self.getfilename(global_config["test_font_file"])), 
            testfile = global_config["test_file"], 
            imagefile_extension = global_config["image_file_extension"]
        )
