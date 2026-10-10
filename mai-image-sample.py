curl -X POST "https://bankfn.services.ai.azure.com/mai/v1/images/generations" \
-H "Content-Type: application/json" \
-H "api-key: $AZURE_API_KEY" \
-d '{
    "prompt": "A photograph of a red fox in an autumn forest",
    "width": 1024,
    "height": 1024,
    "model": "MAI-Image-2.6"
}' | jq -r '.data[0].b64_json' | base64 --decode > generated_image.png

