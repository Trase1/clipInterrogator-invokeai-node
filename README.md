CLIP Interrogator Node

An InvokeAI node for generating prompt from the given image. This InvokeAI node takes Unet and image, and outputs a
a prompt, that describes an image, using a https://github.com/pharmapsychotic/clip-interrogator
It automatically detects which of the OpenCLIP pretrained CLIP models to use by the given Unet.
If you have low VRAM, you could switch to Lowvram to reduce the amount of VRAM needed(at the cost of some speed and quality).
The default settings use about 6.3GB of VRAM and the low VRAM settings use about 2.7GB.

## Before use:

In invoke.bat choose 8 to open developer console, virtual environment will be activated.
Install clip-interrogator with PIP
```
# install clip-interrogator
pip install clip-interrogator==0.5.4

# or for very latest WIP with BLIP2 support
#pip install clip-interrogator==0.6.0
```