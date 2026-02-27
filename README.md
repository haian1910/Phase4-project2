# Image Captioning & Image Inpainting Docker Services

This project provides two Docker images:

1. Image Captioning Service – Generate caption from an image  
2. Image Inpainting Service – Inpaint a selected region of an image using a caption  

---

# 1. Image Captioning Service

## Endpoint

POST /caption

## Input (JSON)

```json
{
  "image": "base64_encoded_image"
}
```

## Output (JSON)

```json
{
  "caption": "A man wearing a red shirt standing outside."
}
```


## Pull Docker Image

```bash
docker pull haiancol/caption:latest
```

## Run Container

```bash
docker run -p 8000:8000 haiancol/caption:latest
```

Service will be available at:

http://localhost:8000/caption

---

# 2. Image Inpainting Service

## Endpoint

POST /inpaint

## Input (JSON)

```json
{
  "image": "base64_encoded_image",
  "caption": "a beautiful landscape with mountains",
  "tl": [x1, y1],
  "br": [x2, y2]
}
```

- image (string): Base64 encoded image.
- caption (string): Text prompt used to guide inpainting.
- tl (array[int, int]): Top-left coordinate of inpainting region.
- br (array[int, int]): Bottom-right coordinate of inpainting region.

## Output (JSON)

```json
{
  "image": "base64_encoded_inpainted_image"
}
```

- image (string): Base64 encoded inpainted image.

## Pull Docker Image

```bash
docker pull haiancol/inpaint:latest
```

## Run Container

```bash
docker run -p 8001:8000 haiancol/inpaint:latest
```

Service will be available at:

http://localhost:8001/inpaint

---

# Example Request

## Caption

```bash
curl -X POST http://localhost:8000/caption \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_string_here"}'
```

## Inpaint

```bash
curl -X POST http://localhost:8001/inpaint \
  -H "Content-Type: application/json" \
  -d '{
        "image": "base64_string_here",
        "caption": "a blue sky",
        "tl": [0, 0],
        "br": [200, 200]
      }'
```