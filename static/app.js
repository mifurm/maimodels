const recordButton = document.querySelector("#record-button");
const recordLabel = document.querySelector("#record-label");
const statusElement = document.querySelector("#status");
const conversationElement = document.querySelector("#conversation");
const answerAudio = document.querySelector("#answer-audio");

const history = [];
let recording = null;

function setStatus(message, isError = false) {
  statusElement.textContent = message;
  statusElement.classList.toggle("error", isError);
}

function addMessage(role, text) {
  conversationElement.querySelector(".empty-state")?.remove();
  const message = document.createElement("article");
  message.className = `message ${role}`;

  const label = document.createElement("strong");
  label.textContent = role === "user" ? "Ty" : "Asystent";
  const content = document.createElement("p");
  content.textContent = text;

  message.append(label, content);
  conversationElement.append(message);
  message.scrollIntoView({ behavior: "smooth", block: "end" });
}

function mergeBuffers(chunks) {
  const length = chunks.reduce((total, chunk) => total + chunk.length, 0);
  const merged = new Float32Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }
  return merged;
}

function downsample(samples, inputRate, outputRate) {
  if (inputRate === outputRate) {
    return samples;
  }

  const ratio = inputRate / outputRate;
  const output = new Float32Array(Math.round(samples.length / ratio));
  for (let index = 0; index < output.length; index += 1) {
    const start = Math.round(index * ratio);
    const end = Math.min(Math.round((index + 1) * ratio), samples.length);
    let total = 0;
    for (let inputIndex = start; inputIndex < end; inputIndex += 1) {
      total += samples[inputIndex];
    }
    output[index] = total / Math.max(1, end - start);
  }
  return output;
}

function encodeWav(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  function writeText(offset, text) {
    for (let index = 0; index < text.length; index += 1) {
      view.setUint8(offset + index, text.charCodeAt(index));
    }
  }

  writeText(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeText(8, "WAVE");
  writeText(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeText(36, "data");
  view.setUint32(40, samples.length * 2, true);

  let offset = 44;
  for (const sample of samples) {
    const clamped = Math.max(-1, Math.min(1, sample));
    view.setInt16(offset, clamped < 0 ? clamped * 0x8000 : clamped * 0x7fff, true);
    offset += 2;
  }

  return new Blob([buffer], { type: "audio/wav" });
}

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const audioContext = new AudioContext();
  const source = audioContext.createMediaStreamSource(stream);
  const processor = audioContext.createScriptProcessor(4096, 1, 1);
  const silentOutput = audioContext.createGain();
  const chunks = [];

  silentOutput.gain.value = 0;
  processor.onaudioprocess = (event) => {
    chunks.push(new Float32Array(event.inputBuffer.getChannelData(0)));
  };
  source.connect(processor);
  processor.connect(silentOutput);
  silentOutput.connect(audioContext.destination);

  recording = {
    audioContext,
    chunks,
    processor,
    silentOutput,
    source,
    stream,
  };
  recordButton.classList.add("recording");
  recordLabel.textContent = "Zatrzymaj i wyślij";
  setStatus("Słucham...");
}

async function stopRecording() {
  const current = recording;
  recording = null;
  current.processor.disconnect();
  current.source.disconnect();
  current.silentOutput.disconnect();
  current.stream.getTracks().forEach((track) => track.stop());
  await current.audioContext.close();

  recordButton.classList.remove("recording");
  recordLabel.textContent = "Zacznij mówić";
  recordButton.disabled = true;
  setStatus("Rozpoznaję mowę i przygotowuję odpowiedź...");

  const merged = mergeBuffers(current.chunks);
  const samples = downsample(merged, current.audioContext.sampleRate, 16000);
  const wav = encodeWav(samples, 16000);
  const form = new FormData();
  form.append("audio", wav, "recording.wav");
  form.append("history", JSON.stringify(history));

  try {
    const response = await fetch("/api/chat", { method: "POST", body: form });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Nie udało się przetworzyć nagrania.");
    }

    addMessage("user", payload.transcript);
    addMessage("assistant", payload.reply);
    history.push(
      { role: "user", content: payload.transcript },
      { role: "assistant", content: payload.reply },
    );

    answerAudio.src = `data:audio/wav;base64,${payload.audio}`;
    answerAudio.hidden = false;
    await answerAudio.play();
    setStatus("Gotowy");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    recordButton.disabled = false;
  }
}

recordButton.addEventListener("click", async () => {
  try {
    if (recording) {
      await stopRecording();
    } else {
      await startRecording();
    }
  } catch (error) {
    recording = null;
    recordButton.classList.remove("recording");
    recordLabel.textContent = "Zacznij mówić";
    recordButton.disabled = false;
    setStatus(error.message, true);
  }
});
