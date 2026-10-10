# Microsoft Foundry model samples

This repository contains a Polish voice-chat application, standalone Azure AI
Speech examples, and MAI-Image-2.6 marketing-image samples.

The voice-chat application records Polish speech in the browser, transcribes it
with Azure AI Speech, sends the text and recent conversation history to an Azure
OpenAI GPT-4.1-mini deployment, and speaks the Polish response with
`en-US-Andrew:DragonHDLatestNeural`.

## Configure

1. Create or select an Azure AI Speech resource.
2. Deploy `gpt-4.1-mini` in Azure AI Foundry.
3. Set the following values in `.env`:

   ```dotenv
   AZURE_SPEECH_ENDPOINT=https://YOUR-SPEECH-RESOURCE.cognitiveservices.azure.com/
   AZURE_SPEECH_KEY=YOUR_SPEECH_KEY
   AZURE_OPENAI_ENDPOINT=https://YOUR-OPENAI-RESOURCE.openai.azure.com
   AZURE_OPENAI_API_KEY=YOUR_OPENAI_KEY
   AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
   ```

The deployment value must be the deployment name you chose in Azure AI Foundry, which can differ from the model name.
`AZURE_OPENAI_ENDPOINT` accepts either the resource root URL or a Foundry URL that already ends in `/openai/v1`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open <http://127.0.0.1:8000>, allow microphone access, select **Zacznij mówić**, speak in Polish, and select **Zatrzymaj i wyślij**.

The browser sends 16 kHz mono WAV audio to the server. Keys remain server-side and are never sent to browser JavaScript.

## Standalone Speech SDK samples

The repository also contains two command-line samples that use the Azure AI
Speech SDK directly. Both read `AZURE_SPEECH_ENDPOINT` and `AZURE_SPEECH_KEY`
from the `.env` file configured above and use the computer's default audio
devices.

### Speech to text (`s2t.py`)

[`s2t.py`](./s2t.py) listens continuously to the default microphone and
recognizes Polish speech (`pl-PL`). Partial results are printed as
`Recognizing`, and completed results are printed as `Recognized`.

Run the sample:

```bash
python s2t.py
```

Speak after `Say something...` appears. Press Enter to stop recognition.

### Text to speech (`mai2.py`)

[`mai2.py`](./mai2.py) synthesizes the fixed text
`Cześć, witaj w Azure AI Foundry!` with the
`en-US-Andrew:DragonHDLatestNeural` voice and plays the audio through the
default speaker. It prints whether synthesis completed or was canceled,
including Azure Speech error details when available.

Run the sample:

```bash
python mai2.py
```

To synthesize different content, change the `text` value in `mai2.py`. You can
also change `speech_synthesis_language` and `speech_synthesis_voice_name` to
use another supported language and voice.

## MAI-Image-2.6 marketing samples

[`mai_image.py`](./mai_image.py) demonstrates MAI-Image-2.6's commercial image
quality, text rendering, portraits, and flexible output sizes. It includes a
landscape product-launch hero, a square skincare social post, a vertical travel
poster, a premium fictional technology credit card, and eleven banana-card
concepts ranging from elegant and minimal to rock, cyber, and pop treatments.

The available sample names are:

| Sample | Size | Concept |
| --- | --- | --- |
| `product-launch` | 1536x1024 | Luxury wireless-speaker campaign |
| `skincare-social` | 1024x1024 | Square skincare advertisement |
| `city-poster` | 1024x1536 | Vertical travel poster |
| `tech-credit-card` | 1536x1024 | Fictional technology credit card |
| `banana-credit-card` | 1536x1024 | Original tropical banana card |
| `banana-card-elegant` | 1536x1024 | Gold linework and ivory enamel |
| `banana-card-rock` | 1536x1024 | Distressed concert-poster treatment |
| `banana-card-modern` | 1536x1024 | Geometric color-block design |
| `banana-card-minimal` | 1536x1024 | Monochrome debossed banana |
| `banana-card-art-deco` | 1536x1024 | Gold, lacquer, and geometric ornament |
| `banana-card-cyber` | 1536x1024 | Holographic futuristic banana |
| `banana-card-watercolor` | 1536x1024 | Hand-painted watercolor treatment |
| `banana-card-tropical` | 1536x1024 | Tropical leaves and sunset colors |
| `banana-card-luxury` | 1536x1024 | Gold-like metal, onyx, and leather |
| `banana-card-pop` | 1536x1024 | Bold contemporary pop graphics |

Deploy `MAI-Image-2.6` or `MAI-Image-2.6-Flash` in Microsoft Foundry, then add
its resource details to `.env`:

```dotenv
AZURE_MAI_IMAGE_ENDPOINT=https://YOUR-RESOURCE.services.ai.azure.com
AZURE_MAI_IMAGE_API_KEY=YOUR_MAI_IMAGE_KEY
AZURE_MAI_IMAGE_DEPLOYMENT=YOUR_MAI_IMAGE_2_6_DEPLOYMENT
```

The deployment value is the deployment name you selected in Foundry, not
necessarily the model name. `AZURE_MAI_IMAGE_ENDPOINT` accepts either the
resource root shown above or the full endpoint ending in
`/mai/v1/images/generations`.

Generate all 15 samples:

```bash
python mai_image.py
```

PNG files are written to `generated/mai-image-2.6/`. To generate just one
concept or choose another output directory:

```bash
python mai_image.py --sample product-launch
python mai_image.py --sample skincare-social --output-dir generated/campaign
```

Generate all 11 banana-card concepts, including the original:

```bash
python mai_image.py --sample banana-collection
```

Show every available command-line option and sample name:

```bash
python mai_image.py --help
```

Use `--web-grounding` when a prompt needs current real-world context. The
included fictional campaigns do not require it, so it is disabled by default.
MAI-Image-2.6 is currently in preview; review generated assets before publishing
and disclose AI-generated content where appropriate.

### Direct REST API sample

[`mai-image-sample.py`](./mai-image-sample.py) contains a cURL example that
generates a 1024x1024 red-fox image and decodes the base64 response into
`generated_image.png`. Despite its `.py` extension, this file is a shell
script and requires `curl`, `jq`, and `base64`.

Export the API key expected by the script:

```bash
export AZURE_API_KEY=YOUR_MAI_IMAGE_KEY
```

Update the endpoint and `model` deployment name inside
`mai-image-sample.py` for your Foundry resource, then run:

```bash
bash mai-image-sample.py
```
