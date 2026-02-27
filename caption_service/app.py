from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
import io
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration, BitsAndBytesConfig

app = FastAPI()

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-6.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-6.7b",
    quantization_config=quantization_config,
    device_map="auto",
)
model.eval()

class Request(BaseModel):
    image: str

@app.post("/caption")
def caption(req: Request):
    image_bytes = base64.b64decode(req.image)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return {"caption": caption}