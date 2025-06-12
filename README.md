# LinkedIn Uploader Middleware

## How It Works
- Accepts a base64-encoded image and uploads it to LinkedIn via a pre-signed URL
- Optional: Also posts image + text as a feed post (if using full_uploader.py)

## Endpoints
- `/upload-only`: Accepts `base64_image`, `upload_url`, and `content_type`
- `/linkedin/upload`: Accepts `base64_image`, `content`, `access_token`, `person_urn`

## Deployment
1. Clone this repo or copy manually
2. `pip install -r requirements.txt`
3. Run with `python upload_only.py`
4. Or deploy to Render, Railway, etc.

## Example Payload (for `/upload-only`)
```json
{
  "base64_image": "<base64 string>",
  "upload_url": "https://media-upload-url-from-linkedin",
  "content_type": "image/png"
}
