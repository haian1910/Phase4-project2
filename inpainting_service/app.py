from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image, ImageDraw
import base64
import io
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

class Request(BaseModel):
    image: str
    caption: str
    tl: List[int]
    br: List[int]

@app.post("/inpaint")
def inpaint(req: Request):
    image_bytes = base64.b64decode(req.image)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(
        [req.tl[0], req.tl[1], req.br[0], req.br[1]],
        fill=255
    )
    prompt = f"{req.caption}, fill the masked region naturally and consistently"

    result = pipe(
        prompt=prompt,
        image=image,
        mask_image=mask
    ).images[0]

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    return {
        "image": encoded
    }