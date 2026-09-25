# Literature review

Three papers shaped the design of this project. The original write-ups
are in [`literature/`](literature/) as Word documents.

## 1. Fusion of infrared and visible images for night-vision context enhancement
*Z. Zhou, M. Dong, X. Xie, Z. Gao — Applied Optics, 2016*

Infrared sensors see thermal radiation that is invisible to the eye in the
dark or behind occlusions. Low-light visible (CCD) images show the details and
background that people find easiest to interpret. Fusing the two produces a
scene that is more complete than either image alone. Most pixel-level methods
are **multi-scale**: they decompose both images, combine the coefficients and
reconstruct. The authors set two goals for good night-vision context
enhancement:

1. Enhance the detail of poorly lit regions in the visible image as much as
   possible.
2. Transfer all important IR information (hot targets) into the visible
   image while keeping the visible background natural to look at.

**What we took from it:** a multi-scale (wavelet) fusion with separate rules
for coarse and fine coefficients, plus a contrast-enhancement step before
fusion (goal 1).

## 2. Making of night vision: object detection under low illumination
*Y. Xiao, A. Jiang — IEEE Access, 2020*

The paper studies how illumination affects object detection. It compares
detection with and without illumination enhancement, the effect of an
illumination-balanced dataset, and how parameters are initialised. The
authors propose a Night Vision Detector (NVD) with a purpose-built feature
pyramid and a context-fusion network. It is trained on the real low-light
ExDARK dataset, with COCO as the normal-light counterpart. Compared with the
RFB-Net baseline it improves COCO-style detection by 0.5–2.8 %.

**What we took from it:** evidence that enhancing low-light imagery before
analysis measurably helps downstream tasks. That motivated evaluating our
output with objective metrics rather than by eye alone.

## 3. Night vision devices (review)
*P. Tamilchelvan*

Background on how night vision works. Night vision devices have three main
parts: an objective lens, an image-intensifier tube (a photocathode, a
micro-channel amplifier and a phosphor screen) and an eyepiece. Other
technologies include thermal imagers, SWIR imagers and sensitive
visible/NIR CCD, CMOS and EMCCD cameras. Building a device from off-the-shelf
parts looks simple, but getting good image quality requires understanding how
each module affects the final image.

**What we took from it:** the `*_II` images in the TNO data come from an
image intensifier, and the `*_IR` images come from a thermal (LWIR) camera.
Knowing how the two sensors behave explains why their information is
complementary.

## Dataset papers

* A. Toet, "The TNO Multiband Image Data Collection", *Data in Brief* 15
  (2017) 249–251. Dataset: [doi:10.6084/m9.figshare.1008029](https://doi.org/10.6084/m9.figshare.1008029)
* A. Toet, M. A. Hogervorst, A. R. Pinkus, "The TRICLOBS Dynamic Multi-Band
  Image Data Set for the Development and Evaluation of Image Fusion Methods",
  *PLoS ONE* 11(12): e0165016 (2016).
  [doi:10.1371/journal.pone.0165016](https://doi.org/10.1371/journal.pone.0165016).
  Dataset: [doi:10.6084/m9.figshare.3206887](https://doi.org/10.6084/m9.figshare.3206887)
* E. Reinhard, M. Ashikhmin, B. Gooch, P. Shirley, "Color Transfer between
  Images", *IEEE Computer Graphics and Applications* 21(5), 2001.
