# OffRender

### 1. Overview

OffRender is a low-level feature-controlled object stimulus renderer under various types of transform, such as translation, rotation, scaling and viewpoint variation. ModelNet10 (Wu et al., 2015), a publicly available 3D object dataset which contains 10 different object classes with aligned orientations, was used to render the stimulus (we used only nine object classes due to an insufficient number of CAD files). Each CAD file is converted to an image at a given horizontal viewpoint using the object render. After capturing the object, the renderer generates a phase-scrambled background image. Using a sample natural image, it scrambles the phase of the given natural image in the Fourier domain and returns it to the original space. These phase-scrambled backgrounds are often used in human fMRI studies to exclude the effects of the background in visual processing (Stigliani et al., 2015). For the object images and phase-scrambled backgrounds, the overall pixel intensity is normalized in each case to have an identical intensity distribution.

![OffRender_Method.png](https://github.com/Jeonghwan-Cheon/OffRender/blob/main/source/OffRender_Method.png)

### 2. Installation
- Download all files and folders. ("Clone or download" -> "Download ZIP")
- Download ModelNet10 from below link and unzip files in the same directory
- Princeton ModelNet: [https://modelnet.cs.princeton.edu/]
- There are five python codes which render .off file and process image. You should modify only ```main.py```.

| Code | Task |
|:----:|:-----|
|```main.py```| Set the type of transformation (translation, rotation, scaling, viewpoint) and type of dataset to render (object dataset, viewpoint dataset, SVM dataset) |
|```batch_generator.py```| As the type of transformation and dataset to render determined in ```main.py```, it automately generates sub-tasks which directly related to core rendering part.|
|```render.py```| It handles single CAD file (.off) and generates a 227×227 image at given conditions (e.g. horizontal and vertical viewpoint). |
|```image_processing.py```| It offers various functions that are related to image processing. First, there are some functions that used to normalize a image that makes overall pixel intensity has identical distribution. Second, there is a function which generates scrambled image set. Third, there are various functions that can linearly transform the given image (i.e. translation, rotation, scaling) |
|```background_generator.py```| If offers fucntions that generate and merge phase-scrambled background which is often used in human fMRI studies to exclude the effects of the background in visual processing (Stigliani et al., 2015). |


### 3. Instructions
- You can modify ```main()``` in ```main.py``` to set the type of transformation and dataset. The following is a example of implementation, which used to generate viewpoint-variant object images.
```
def main():
    var_type = "viewpoint"
    dir_list = os.listdir(route)
    render_selectivity_var_set(var_type, dir_list)
    render_invariance_test_set(var_type, dir_list, 1)
    render_invariance_test_set(var_type, dir_list, 2)
    render_invariance_unit_set(var_type, dir_list)
    render_SVM_var_set(var_type, dir_list)
```
- Detailed explanation for each type of dataset (object dataset, viewpoint dataset, SVM dataset) can be found in 'Materials and methods' part of our publication. [![DOI:10.3389/fncom.2022.1030707](http://img.shields.io/badge/DOI-10.3389/fncom.2022.1030707-C12E32.svg)](https://doi.org/10.3389/fncom.2022.1030707)

### 4. Output

- Rendered images are stored in ```./Image``` directory, and each type of dataset saved as sub-directories. For example, dataset ```invariance_test``` with transformation type ```viewpoint``` is saved as ```./Image/invariance_test/viewpoint/```.
- Followings are example images of object dataset. In the object dataset, brightness and contrast of the images are precisely controlled to be equal across object classes. Also, the intra-class similarity of the images in each object category was calibrated at a statistically comparable level.

![OffRender_Object_Dataset.png](https://github.com/Jeonghwan-Cheon/OffRender/blob/main/source/OffRender_Object_Dataset.png)

- Followings are example images of viewpoint dataset. In the viewpoint dataset, brightness and contrast of the images are precisely controlled to be equal across transformation results. Also, the intra-class similarity of the images in each different transformation was calibrated at a statistically comparable level.

![OffRender_Viewpoint_Dataset.png](https://github.com/Jeonghwan-Cheon/OffRender/blob/main/source/OffRender_Viewpoint_Dataset.png)

- (1) Object dataset, (2) Viewpoint dataset, (3) SVM dataset with viewpoint transformation, which generated using ```OffRender``` and also used in our study can be downloaded in following open repository. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7276304.svg)](https://doi.org/10.5281/zenodo.7276304)

### 5. Dataset for "Invariance of object detection in untrained deep neural networks"
- ```OffRender``` was developed to generate dataset used in our study which investigates invariance of object detection in untrained deep neural network.
```bibtex
@ARTICLE{10.3389/fncom.2022.1030707,
  AUTHOR={Cheon, Jeonghwan and Baek, Seungdae and Paik, Se-Bum},
  TITLE={Invariance of object detection in untrained deep neural networks},
  JOURNAL={Frontiers in Computational Neuroscience},
  VOLUME={16},
  YEAR={2022},
  URL={https://www.frontiersin.org/articles/10.3389/fncom.2022.1030707},
  DOI={10.3389/fncom.2022.1030707},
  ISSN={1662-5188}
}
```
