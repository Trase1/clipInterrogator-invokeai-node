from invokeai.app.invocations.baseinvocation import BaseInvocation, invocation, InputField, InvocationContext, invocation_output
from invokeai.app.invocations.primitives import ImageField, StringOutput, StringInvocation, BooleanInvocation
from invokeai.app.invocations.model import UNetField
from invokeai.backend.model_management import BaseModelType
from PIL import Image
import torch

try:
    from clip_interrogator import Config, Interrogator
except ImportError:
    print("clip-interrogator is not installed, please install it with 'pip install clip-interrogator'")
    exit(1)



@invocation("CLIPInterrogator", title="CLIP Interrogator", tags=["CLIP", "prompt", "interrogation"], version="0.1.0")
class clipInterrogatorInvocation(BaseInvocation):
    '''Generates prompt from given picture with CLIP interrogator'''
    unet: UNetField = InputField(default=None, description="UNet submodel")
    image:ImageField = InputField(description="The input image")
    lowVram: bool = InputField(default=False, description="Use low_vram setting")
   
    def invoke(self, context: InvocationContext) -> StringOutput :
        clipModelName: str = ''
        device: str = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if not torch.cuda.is_available():
            print("CUDA is not available, using CPU. Warning: this will be very slow!")
        if self.unet.unet.base_model == BaseModelType.StableDiffusion1:
            clipModelName = 'ViT-L-14/openai'
        elif self.unet.unet.base_model == BaseModelType.StableDiffusion2:
            clipModelName = 'ViT-H-14/laion2b_s32b_b79k'
        elif self.unet.unet.base_model == BaseModelType.StableDiffusionXL:
            clipModelName = 'ViT-bigG-14/laion2b_s39b_b160k'
        else : 
            raise Exception("Error: not compatible StableDiffusion(?) version")
        config = Config(device=device, clip_model_name=clipModelName)    
        if self.lowVram == True : config.apply_low_vram_defaults()
        image = context.services.images.get_pil_image(self.image.image_name).convert('RGB')
        ci = Interrogator(config)
        prompt = ci.interrogate(image)
        print(prompt)
        return StringOutput(value = prompt)