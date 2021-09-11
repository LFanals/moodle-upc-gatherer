from selenium import webdriver
from tqdm import tqdm # progress bar
import os # to rename files
import glob # to get file name
import time # to wait for downloads to finish

############### USER config #################
# Atenea credentials
username = ""
password = ""
# Working directories
courseLinks = ["https://atenea.upc.edu/course/view.php?id=71639", "https://atenea.upc.edu/course/view.php?id=71638", "https://atenea.upc.edu/course/view.php?id=71729", "https://atenea.upc.edu/course/view.php?id=71685", "https://atenea.upc.edu/course/view.php?id=71645", "https://atenea.upc.edu/course/view.php?id=71715"] # Course links whose resources must be gathered
dirMain = ["/home/lf/MEE/1_MTP", "/home/lf/MEE/1_MTP", "/home/lf/MEE/2_SCPD", "/home/lf/MEE/3_EDIS", "/home/lf/MEE/4_MOSIC", "/home/lf/MEE/5_IBES"] # Directories in which each course contents are to be stored
dirTemporal = "/home/lf/MEE/Scripts/Temporal" # Directory where files will be downloaded and temporarily saved


# Chrome configuration
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": dirTemporal, # Change default directory for downloads
    "download.prompt_for_download": False, # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True # It will not show PDF directly in chrome
})

# Start Chrome
driver = webdriver.Chrome(options=options)

print("moodle-upc-gatherer started")

# Login Atenea
driver.get("https://atenea.upc.edu/login/index.php")
elem = driver.find_element_by_id("loginbtn")
elem.click()
elem = driver.find_element_by_name("adAS_username")
elem.send_keys(username)
elem = driver.find_element_by_name("adAS_password")
elem.send_keys(password)
elem = driver.find_element_by_name("adAS_submit")
elem.click()

print("Login is done")

for j in range(len(courseLinks)):

    # Enter course
    driver.get(courseLinks[j])
    
    # Gather all resources links
    pageSource = driver.page_source
    
    # Split pageSource properly
    Resources = pageSource.split('href="https://atenea.upc.edu/mod/resource/view.php?id=')
    Resourcess = []
    for resource in Resources[1:]: # first string [0] is not useful
        Resourcess.append(resource.split('<span class="accesshide "')[0])
    
    
    # Initialize and fill links, file name and id code vectors
    vecLinks = []
    vecCodes = []
    
    for resource in Resourcess:
        code = resource.split('"')[0]
        vecCodes.append(code)
        vecLinks.append('https://atenea.upc.edu/mod/resource/view.php?id='+code)

    # # #################### FOLDERS #########################
    # # Gather the contents inside folders. The files id seems to change, so a lot of diffs are necessary. It can slow down the computer
    # # Split pageSource properly
    # Folders = pageSource.split('href="https://atenea.upc.edu/mod/folder/view.php?id=')
    # Folderss = [] # contains all folder links
    # for folder in Folders[1:]: 
    #     Folderss.append('https://atenea.upc.edu/mod/folder/view.php?id=' + folder.split('"')[0])

    # print(Folderss)
   
    # for folder in Folderss[0:]:
    #     driver.get(folder)
    #     pageSource = driver.page_source
    #     # Split pageSource properly
    #     Resources = pageSource.split('href="https://atenea.upc.edu/mod/resource/view.php?id=')
    #     for resource in Resources[0:]: 
    #         Resourcess.append(resource.split('<span class="accesshide "')[0])
    #     # Get resources inside the folder 
    #     for resource in Resourcess:
    #         code = resource.split('"')[0]
    #         vecCodes.append(code)
    #         vecLinks.append('https://atenea.upc.edu/mod/resource/view.php?id='+code)





    # Check id codes
    
    vecMainFileNames = glob.glob(dirMain[j]+'/*.*') # get file names in the main folder
    vecMainCodes = []
    for i in range(len(vecMainFileNames)):
        vecMainCodes.append(vecMainFileNames[i].split('/')[-1].split(' ')[0])
    
    
    print("Start gathering at:", courseLinks[j])
    
    for i in tqdm(range(len(vecLinks))): # Display progess bar
        link = vecLinks[i]
        if (not (vecCodes[i] in vecMainCodes)): # Resource has not been downloaded before
            try:
                driver.get(link)
                # In some uncommon cases, files open/download automatically with the default browser configuration, and because we changed this configuration, they no longer are downloaded.
                # The following lines gather the root file and download it.
                pageSource = driver.page_source
                resourcePlugin = ([word for word in pageSource.split() if word.startswith('href="https://atenea.upc.edu/pluginfile.php/')]) # "https://atenea.upc.edu/pluginfile.php/3833466/mod_resource/content/4/lab3.pdf" 
                if resourcePlugin: # a pluginfile has been found
                    linkk = resourcePlugin[0].split('"')[1]
                    try:
                        driver.get(linkk)
                        driver.back() # go back to course main page, so that this same pluginfile is not seen
    
                    except:
                        print("Failed")
                        continue
               
            except:
                print("Failed")
                continue
    
    print("Waiting until downloads are finished")
    
    # Wait until all files are completely downloaded
    isDownloading = 1
    while (isDownloading == 1):
        isDownloading = 0
        vecFileName = glob.glob(dirTemporal+'/*.*') # get file names
        for i in range(len(vecFileName)):
            vecFileName[i] = vecFileName[i].split('/')[-1]
    
        for fileName in vecFileName:
            if fileName.endswith('.crdownload'):
                isDownloading = 1
                time.sleep(0.1)
    

    # Create new files as 'code - name.*' and move them if their content differs (in some unusual cases the code of the same file changes each time, we don't want the same file multiple times in the main folder)
    vecCurrentMainFiles = glob.glob(dirMain[j]+'/*.*') # get file routes of the files in the main folder
    for i in range(len(vecFileName)):
        isNewFile = 1  
        for k in range(len(vecCurrentMainFiles)):
            differences = os.system("diff -s " + dirTemporal+'/'+vecFileName[i].replace(' ', '\ ').replace('(', '\(').replace(')', '\)') + " " + vecCurrentMainFiles[k].replace(' ', '\ ').replace('(', '\(').replace(')', '\)') )
            # differences = os.system("alacritty -e diff -s " + dirTemporal+'/'+vecFileName[i].replace(' ', '\ ').replace('(', '\(').replace(')', '\)') + " " + vecCurrentMainFiles[k].replace(' ', '\ ').replace('(', '\(').replace(')', '\)') ) # To avoid seeing a large log, not an elegant solution though
            if differences == 0:
                isNewFile = 0 

        if isNewFile == 1:
            print(vecFileName[i])
            os.rename(dirTemporal+'/'+vecFileName[i], dirMain[j]+'/'+vecCodes[i]+' - '+vecFileName[i])
        else:
            os.remove(dirTemporal+'/'+vecFileName[i])
     

driver.close()

print("moodle-upc-gatherer has finished")    


