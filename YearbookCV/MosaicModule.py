import os, random
from PIL import Image
import numpy as np


class MosaicMaker():

    def __init__(self):
        pass

    def getImages(self, images_directory):
        files = os.listdir(images_directory)
        images = []
        for file in files:
            filePath = os.path.abspath(os.path.join(images_directory, file))
            try:
                fp = open(filePath, "rb")
                im = Image.open(fp)
                images.append(im)
                im.load()
                fp.close()
            except:
                print("Invalid image: %s" % (filePath,))
        return (images)

    def getAverageRGB(self, image):
        im = np.array(image)
        w, h, d = im.shape
        return (tuple(np.average(im.reshape(w * h, d), axis=0)))
    
    def splitImage(self, image, size):
        W, H = image.size[0], image.size[1]
        m, n = size
        w, h = int(W / n), int(H / m)
        imgs = []
        for j in range(m):
            for i in range(n):
                imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
        return (imgs)

    def getBestMatchIndex(self, input_avg, avgs):
        avg = input_avg
        index = 0
        min_index = 0
        min_dist = float("inf")
        for val in avgs:
            dist = ((val[0] - avg[0]) * (val[0] - avg[0]) +
                    (val[1] - avg[1]) * (val[1] - avg[1]) +
                    (val[2] - avg[2]) * (val[2] - avg[2]))
            if dist < min_dist:
                min_dist = dist
                min_index = index
            index += 1
        return (min_index)

    def createImageGrid(self, images, dims):
        m, n = dims
        width = max([img.size[0] for img in images])
        height = max([img.size[1] for img in images])
        grid_img = Image.new('RGB', (n * width, m * height))
        for index in range(len(images)):
            row = int(index / n)
            col = index - n * row
            grid_img.paste(images[index], (col * width, row * height))
        return (grid_img)
    
    def createPhotomosaic(self, target_image, input_images, grid_size, reuse_images=True):
        target_images = self.splitImage(target_image, grid_size)

        output_images = []
        count = 0
        batch_size = int(len(target_images) / 10)
        avgs = []
        for img in input_images:
            try:
                avgs.append(self.getAverageRGB(img))
            except ValueError:
                continue

        for img in target_images:
            avg = self.getAverageRGB(img)
            match_index = self.getBestMatchIndex(avg, avgs)
            output_images.append(input_images[match_index])
            #For logging the processing of images uncomment the code below:
            # if count > 0 and batch_size > 10 and count % batch_size == 0:
            #     print('processed %d of %d...' % (count, len(target_images)))
            # count += 1
            # remove selected image from input if flag set
            if not reuse_images:
                input_images.remove(match_index)

        mosaic_image = self.createImageGrid(output_images, grid_size)
        return (mosaic_image)

def make_mosaic(target_image, input_file, grid_size, output_filename = "mosaic.jpeg", reuse_images=True):
    """

    :param target_image: image file to fit mosaic
    :param input_file: file containing images
    :param grid_size: tuple of size of grid of photos
    :param output_filename: filename of the output file
    :param reuse_images: (reuse_images = True => reuse images) (reuse_images = False => don't reuse images)
    
    """
    mm = MosaicMaker()
    images = mm.getImages(input_file)
    target_image = Image.open(target_image)

    if images == []:
        raise Exception("There are no image files in the directory!")

    random.shuffle(images)

    resize_input = True

    if not reuse_images:
        if grid_size[0] * grid_size[1] > len(images):
            raise Exception('grid size less than number of images')
    
    if resize_input:
        # for given grid size, compute max dims w,h of tiles
        dims = (int(target_image.size[0] / grid_size[1]),
                int(target_image.size[1] / grid_size[0]))
        # resize
        for img in images:
            img.thumbnail(dims)

    
    mosaic_image = mm.createPhotomosaic(target_image,images, grid_size, reuse_images)
    mosaic_image.save(output_filename, 'jpeg')