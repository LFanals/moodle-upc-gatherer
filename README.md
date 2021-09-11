# moodle-up-gatherer

This repository contains a simple script that is able to download all the files present in a Moodle course of Universitat Politècnica de Catalunya (UPC). In case some files are already downloaded in the indicated folder, only new files are downloaded. This program comes from the following needs:
* To download all the course material once it has finished. I like to keep all the contents of a course for future needs, and it's tedious to download the resources one by one. 
* To keep a local file system up to date with the Moodle courses. Sometimes the university servers stopped working. In other cases I found myself downloading documents and losing some time on this task. 
* To keep all the documents/versions that have been uploaded to each of the courses.

ATENEA, the virtual learning environment of Universitat Politècnica de Catalunya (UPC), works with adAS as the authentication manager. This supposes an increase in difficulty to use some softwares that perform similar and more advanced tasks than this program. I couldn't manage to make any of them work.

moodle-upc-gathered is based on Selenium, which makes it very easy to navigate through webpages, and can be programmed to replicate mouse clicks and keyboard strokes. The program exploits the fact that resources uploaded to an ATENEA Moodle course are labelled by an unique identifier, which is currently over 3 million. Thus, it's only necessary to check the identifier to determine if there are new files. 

Over time, I've came across a few files which have a variable identifier. To avoid saving these files every time the program is executed, the `diff` command is used to determine if the contents of the file already exist within a file of the folder or not.



## Dependencies
Google Chrome is required to run this script without problems. In Arch Linux:
``` 
$ cd ~/Downloads
$ git clone https://aur.archlinux.org/google-chrome.git
$ cd google-chrome/
$ makepkg -s
``` 

``` 
$ cd ~/Downloads
$ git clone https://aur.archlinux.org/chromedriver.git
$ cd chromedriver/
$ makepkg -s
``` 


Make sure you have python installed. In Arch Linux:
``` 
$ sudo pacman -S python
``` 

And then install the required packages:
``` 
$ pip install selenium tqdm os glob time
``` 


## Usage
First, edit `moodle-upc-gatherer.py` with your Moodle username and password:
```python
username = ""
password = ""
```

Then, type the course links from which you want to gather the documents, the respective directories where files should be saved, and a directory in which files will be downloaded. The program already contains my directories, in case you need an example.
```python
courseLinks = []
dirMain = []
dirTemporal = ''
```

Finally, just run the program.
``` 
$ python moodle-upc-gatherer.py
``` 

You can run the program periodically to have your file directories always up to date and not to miss any file.


## TODO
* Gather external resources (contents pointed to by a link). 
* Improve the folder gathering. 
* Improve code readability. 
* Make the program more robust. 
