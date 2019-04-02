from src import Engine
import argparse
import logging
import os,sys


def arg_parse():

    parser = argparse.ArgumentParser(prog='PROG',description="Fonttest is a font testing tool, it is capable \
        of doing font version diff and font reference glyph compare.")

    subparsers = parser.add_subparsers(help='sub-command help',dest='subparser_name')

    parser_a = subparsers.add_parser("fontdiff", help="fontdiff help")
    parser_a.add_argument("-f", "--fontfiles", required=True, help="This option will get the font version diff,\
        need to pass two version of fontfiles seperated by ','\
        eg:'/<path>/fontfile1.ttf,/<path>/fontfile2.ttf' ")
    
    parser_a.add_argument("-t", "--testfile",required=True, help="Testfile with testcases(test strings)")
    parser_a.add_argument("-s", "--size",  default="50,150,256", help="Different em sizes seperated by ','\
        eg:'10,50,150....256'")
    parser_a.add_argument("-L", "--log", default="./fonttest.log", help="Fonttest execution log file path")


    parser_b = subparsers.add_parser("fonttest", help="This option will compare font with reference glyph file in git/locally")
    parser_b.add_argument("-f", "--fontfile", required=True, help="Pass fontfiles to be tested using glyph compare")
    parser_b.add_argument("-g", "--giturl", help="Git repo url to be cloned for reference glyphs.\
        Note: make sure your repo has fonttest dir and ref images with naming convention as <fontname>_<size>")
    parser_b.add_argument("-l", "--local", help="Directory path to local reference glyph directory\
        Note: make sure you have ref images with naming convention as <fontname>_<size>")
    parser_b.add_argument("-t", "--testfile",required=True, help="Testfile with testcases(test strings)")
    parser_b.add_argument("-s", "--size", default="50,150,256", help="Different em sizes seperated by ','\
        eg:'10,50,....,256'")
    parser_b.add_argument("-L", "--log", default="./fonttest.log", help="Fonttest execution log file path")


    parser_c = subparsers.add_parser("generate_reference_image", help="This option will generate reference glyph files in ./tmp/ dir")
    parser_c.add_argument("-f", "--fontfile", required=True, help="Pass fontfiles ")
    parser_c.add_argument("-t", "--testfile",required=True, help="Testfile with testcases(test strings)")
    parser_c.add_argument("-s", "--size", default="50,150,256", help="Different em sizes seperated by ','\
        eg:'10,50,....,256'")
    parser_c.add_argument("-L", "--log", default="./fonttest.log", help="Fonttest execution log file path")

    return parser.parse_args()


if __name__ == "__main__":
    
    args = arg_parse()
    
    config = dict()
    config["image_file_extension"]     = "PNG"
    config["test_file"]                 = args.testfile
    config["font_size_list"]           = args.size.split(",")
    config["cropped_img_dir"]          = "./tmp/cropped_images"
    config["result_img_dir"]           = "./tmp/result_images"
    config["diff_threshold"]           = 0.0

    if args.subparser_name == "fontdiff":    
        config["command"] = "fontdiff"
        config["test_font_files"] = args.fontfiles.split(",")
        for font in config["test_font_files"]: 
            if not os.path.exists(font):
                print("{} file doesnot exist".format(font))
                sys.exit(1)

    elif args.subparser_name == "fonttest":
        config["command"] = "fonttest"
        config["test_font_file"] = args.fontfile
        config["git_url"] = args.giturl
        config["local_ref_dir"] = args.local

        if not config["git_url"] and not config["local_ref_dir"]:
            print("please use -l or -g option")
            sys.exit(1)

        if (config["local_ref_dir"] and not os.path.exists(args.local)) or not os.path.exists(args.fontfile):
            print("invalid file passed")
            sys.exit(1)

    elif args.subparser_name == "generate_reference_image":
        config["command"] = "generate_reference_image"
        config["test_font_file"] = args.fontfile
        if not os.path.exists(args.fontfile):
            print("invalid file {} passed".format(args.fontfile))
            sys.exit(1)

    else:
        print("invalid sub-command specified")
        sys.exit(0)

    obj = Engine(config)
    