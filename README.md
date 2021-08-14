# YearbookCV
This repository contains the development code for the YearbookCV package

## Package installation:
1. Open the command prompt
2. Run `pip install git+https://github.com/VanshKachhwal/YearbookCV` in the cmd prompt

## Various Functions:
* **To Remove Background:**

  Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path` ; specify where you want the images with background removed to get stored - `output_path` ; the background color to set in form of color_channels eg. - `(255,255,255)`, `model` type 0 or 1 - 0 is general,  1 is landscape (faster) ; `threshold` (between 0 and 1) to define the degree of accurate background cuts (more the threshold more will be the time taken) and then execute the following code -
  ```python
  from YearbookCV.BackgroundModule import remove_background
  remove_background(r'input_path', r'output_path', color_channels, model, threshold)
  ##default :- color_channels - (255,255,255),  model - 0, threshold - 0.1
  ```

* **To Crop Images:**
  You can choose from 3 different versions:
  1. Pass the path of a single image file - `img_file_src` ;specify the `size` of the image as int (length of collage square edge); specify the `output_path` [If None passed will return image as cv2 file]; specify `make_circle`, True od False to make individual images circle ;  `remove_background` specify to remove background or not [Default is False] and then execute the following code-
  ```python
  from YearbookCV.Cartoon import CropBody
  CropBody(r'input_path', r'size', r'output_path', r'makeCircle',r'removeBackground')
  ```

  2. Pass the path of a single image file - `img_file_src` ;specify the `size` of the image as int (length of collage square edge); specify the `output_path` [If None passed will return image as cv2 file]; specify `make_circle`, True od False to make individual images circle and then execute the following code-
  ```python
  from YearbookCV.Cartoon import CropFace
  CropFace(r'input_path', r'size', r'output_path', r'makeCircle')
  ```

  3.  Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path`; specify the `output_path` ; specify the `type` of the collage as 0,1 for body crop or face crop [Default is 0]; specify `make_circle`, True od False to make individual images circle [Default is True] ;  `remove_background` specify to remove background or not [Default is False] and then execute the following code -
  ```python
  from YearbookCV.Cartoon import CropAll
  CropAll(r'input_path', r'output_path', r'type', r'makeCircle',r'removeBackground')
  ```


* **To Auto-Align Images:**

  Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path` ; specify where you want the images with background removed to get stored - `output_path` ; `min_face_detection_confidence` ; `min_pose_detection_confidence` and then execute the following code -
  ```python
  from YearbookCV.AutoAlignerModule import auto_align
  auto_align(r'input_path', r'output_path', min_face_detection_confidence, min_pose_detection_confidence)
  ##default :- min_face_detection_confidence - 0.5, min_pose_detection_confidence - 0,5
  ```
* **To Create Collage:**
  You can choose from 3 different collages

  1. Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path` ; specify the final collage `file_name` with the required extension ; `width` ; `height` and then execute the following code -
  ```python
  from YearbookCV.CollageModule import make_collage
  make_collage(r'input_path', 'file_name', width, height)
  ```

  2. Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path` ; specify the final collage `file_name` with the required extension ; specify the `output_path`; specify a template image `template_file` which is a black an white image where white color are parts where circles should be made(Eg: A black background with IIT in white written willl make a collage that resembles this text) and then execute the following code - -
  ```python
  from YearbookCV.CircleCollage import MakeCircleCollage
  MakeCircleCollage(r'input_path', r'template_file',r'output_path',r'file_name'):
  ```

  3. Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path`; specify the `output_path` ; specify the `size` of the collage as int (length of collage square edge); specify `make_circle`, True od False to make individual images circle ; specify `array` as numpy array with 0,1 where to display image or not [Default takes and 8x8 array of ones];  `remove_background` specify to remove background or not [Default is False];   specify the final collage `file_name` with the required extension and then execute the following code -
  ```python
  from YearbookCV.SimpleCollage import SimpleCollage
  SimpleCollage(r'input_path',r'output_path', r'size', r'array', r'removeBackground',r'filename')
  ```

* **To Apply Cartoon Filter:**
  You can choose from 2 different filters
  Copy the path where the photos are present (Only photos must be present in the respective folder) - `input_path` ; specify the `output_path` and then execute the following code -
  ```python
  from YearbookCV.Cartoon import CartoonFilter
  CartoonFilter(r'input_path', r'output_path')
  ```
  or 
  ```python
  from YearbookCV.Cartoon import BlurredCartoonFilter
  BlurredCartoonFilter(r'input_path', r'output_path')
  ```


* **Mosaic Creator**
  This function named  ```createMosaic```  is used to create mosaic of a given target image using multiple images.

  It takes in arguments in the following order:</br>
  target_image, input_images_folder , grid_size, output_filename

  The grid size is a tuple and contains number of rows and columns respectively in the given mosaic.</br>
  For example : grid size of (25,40) means 25 images along the height and 40 images along the breadth of the mosaic. So, the resulting mosaic will comprise of 25*40 images.

  In order to implemenet this function just use the following code:
  ```
  yearbookCV.createMosaic(target_image, input_images_folder , grid_size, output_filename)
  ```
  *Note that the output image is generated in jpeg format.*
