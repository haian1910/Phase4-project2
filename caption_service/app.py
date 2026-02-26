from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
import io
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

app = FastAPI()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

class Request(BaseModel):
    image: str

@app.post("/caption")
def caption(req: Request):
    image_bytes = base64.b64decode(req.image)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    inputs = processor(image, return_tensors="pt")
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return {"caption": caption}