import os


def makeFolder(filename):
    cwd = os.getcwd()
    path = cwd + "\\" + filename
    if not os.path.exists(path):
        os.mkdir(path)


def collect_image_files(input_path):
    IMAGE_FILES = []
    for filename in os.listdir(input_path):
        IMAGE_FILES.append(filename)

    return IMAGE_FILES

    
        