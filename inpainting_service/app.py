from diffusers import AutoPipelineForInpainting
import torch
from PIL import Image, ImageDraw
import base64
import io
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

pipe = AutoPipelineForInpainting.from_pretrained(
    "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

pipe.enable_model_cpu_offload()

class Request(BaseModel):
    image: str
    caption: str
    tl: List[int]
    br: List[int]

@app.post("/inpaint")
def inpaint(req: Request):
    image_bytes = base64.b64decode(req.image)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    original_size = image.size
    image_resized = image.resize((1024, 1024))
    scale_x = 1024 / original_size[0]
    scale_y = 1024 / original_size[1]

    mask = Image.new("L", (1024, 1024), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(
        [
            int(req.tl[0] * scale_x),
            int(req.tl[1] * scale_y),
            int(req.br[0] * scale_x),
            int(req.br[1] * scale_y),
        ],
        fill=255
    )

    prompt = f"{req.caption}, fill the masked region naturally and consistently"

    result = pipe(
        prompt=prompt,
        image=image_resized,
        mask_image=mask,
        width=1024,
        height=1024,
        strength=0.99,
        guidance_scale=8.0,
        num_inference_steps=20,
    ).images[0]

    result = result.resize(original_size, Image.LANCZOS)

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    return {"image": encoded}