# Night vision enhancement

IPCV project by Royston, Amruth, Siddharth and Mayur

## To Run

### Prerequisites to Run

 * Ensure the code folder is inside the TNO dataset

 * Install the vl_feat in MATLAB library using [this](https://www.vlfeat.org/install-matlab.html). Run `vl_setup demo` to ensure its installed.


### To run using all images in the dataset

  * Run `execute` in your matlab terminal
    * It contains two parameters `save` and `disp_count`.
    * If `save` is enabled i.e. by setting it to `1`, the re-coloured images gets saved in the directory of the folder in which the IR and VIS images contain.
    * `disp_count` is to tell how many images should be displayed as it contains a lot of images displaying all of them might not be necessary. if `disp_count` is set to `2` , two images are displayed.

  * to run : execute(1, 3); - saves all images in the dataset but displays only 3

### To run using any one image

  * Run `execute_indi(name)`;
    * `name` is the folder name containig the IR and VIS image

  * example: `execute_indi('House');`


### Run using images which is not present in the dataset

  ```
  [rgbnames, dataset] =  get_filenames();
  ir = im2gray(imresize(imread(ir_image_path), [400, 400]));
  vis = im2gray(imresize(imread(vis_image_path), [400, 400]));
  recoloured = enhance(ir, vis, rgbnames);
  imwrite(recolured, to_save_path); %save image
  fig = figure();
  display_images(ir, vis, recoloured, fig);
  ```
