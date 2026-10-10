# Polish Voice Chat

This sample records Polish speech in the browser, transcribes it with Azure AI Speech, sends the text and recent conversation history to an Azure OpenAI GPT-4.1-mini deployment, and speaks the Polish response with `en-US-Andrew:DragonHDLatestNeural`.

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
