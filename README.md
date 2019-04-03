# FontTest
---
#### FontTest is a script to test Truetype fonts rendering using Harfbuzz. It supports following test approaches: 

  - Font version diff 
  - Font reference matching 
  - Font reference generator 

## Dependencies
---
  - Python: Pillow, GitPython
  - System Dependency: Harbuzz 

## Installation
---
Install the dependencies and devDependencies and start the server.
```sh
$ cd fonttest
$ pip3 install --user -r requirement.txt
$ sudo dnf install harfbuzz-devel (for fedora)
```

## Usage
---
- Fontdiff: 
Compare two font version and check diff in glyphs
    ```
    python3  fonttest.py  fontdiff  -t  <test.txt>  -f  <"font-one.ttf, font-two.ttf">  -s <"10,50....,256">
        
        usage: PROG fontdiff [-h] -f FONTFILES -t TESTFILE [-s SIZE] [-L LOG] 
        optional arguments:
          -h, --help            show this help message and exit
          -f FONTFILES, --fontfiles FONTFILES
                                This option will get the font version diff, need to
                                pass two version of fontfiles seperated by ','
                                eg:'/<path>/fontfile1.ttf,/<path>/fontfile2.ttf'
          -t TESTFILE, --testfile TESTFILE
                                Testfile with testcases(test strings)
          -s SIZE, --size SIZE  Different em sizes seperated by ','
                                eg:'10,50,150....256'
          -L LOG, --log LOG     Fonttest execution log file path
    ```

- Fonttest: 
Compare the reference glyph image(locally or clone from your font git repo) with newly generated font glyph image and show diff. 
Note: if want to use git repo to save reference glyph image, make sure your repo has fonttest dir and ref images 
with naming convention as <fontname>_<emsize>
    ```
    python3  fonttest.py  fonttest -t  <test.txt>  -f  <"new-font-file.ttf>  -s  <"10,50....,256">
    
            usage: PROG fonttest [-h] -f FONTFILE [-g GITURL] [-l LOCAL] -t TESTFILE [-s SIZE] [-L LOG]
            optional arguments:
              -h, --help            show this help message and exit
              -f FONTFILE, --fontfile FONTFILE
                                    Pass fontfiles to be tested using glyph compare
              -g GITURL, --giturl GITURL
                                    Git repo url to be cloned for reference glyphs. Note:
                                    make sure your repo has fonttest dir and ref images
                                    with naming convention as <fontname>_<size>
              -l LOCAL, --local LOCAL
                                    Directory path to local reference glyph directory
                                    Note: make sure you have ref images with naming
                                    convention as <fontname>_<size>
              -t TESTFILE, --testfile TESTFILE
                                    Testfile with testcases(test strings)
              -s SIZE, --size SIZE  Different em sizes seperated by ','
                                    eg:'10,50,....,256'
              -L LOG, --log LOG     Fonttest execution log file path
    ```
    
- Generate_reference_image: 
Generate reference glyph image so that it can used by Font reference matching feature or to upload it to your font git repo. 
    ```
    python3 fonttest.py generate_reference_image -t  <test.txt>  -f  <"new-font-file.ttf>  -s  <"10,50....,256">
        usage: PROG generate_reference_image [-h] -f FONTFILE -t TESTFILE [-s SIZE] [-L LOG]
        optional arguments:
          -h, --help            show this help message and exit
          -f FONTFILE, --fontfile FONTFILE
                                Pass fontfiles
          -t TESTFILE, --testfile TESTFILE
                                Testfile with testcases(test strings)
          -s SIZE, --size SIZE  Different em sizes seperated by ','
                                eg:'10,50,....,256'
          -L LOG, --log LOG     Fonttest execution log file path
    ```

## License
---
##### GPL-V3.0

