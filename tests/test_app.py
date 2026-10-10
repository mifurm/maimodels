import base64
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app, openai_base_url


class VoiceChatApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_home_page_is_available(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Polski asystent głosowy", response.text)

    def test_openai_base_url_accepts_resource_endpoint(self) -> None:
        with patch.dict(
            os.environ,
            {"AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com"},
        ):
            self.assertEqual(
                openai_base_url(),
                "https://example.openai.azure.com/openai/v1/",
            )

    def test_openai_base_url_does_not_duplicate_api_path(self) -> None:
        with patch.dict(
            os.environ,
            {
                "AZURE_OPENAI_ENDPOINT": (
                    "https://example.services.ai.azure.com/openai/v1"
                )
            },
        ):
            self.assertEqual(
                openai_base_url(),
                "https://example.services.ai.azure.com/openai/v1/",
            )

    @patch("app.synthesize_reply", return_value=b"audio")
    @patch("app.generate_reply", return_value="Odpowiedź")
    @patch("app.transcribe_wav", return_value="Pytanie")
    def test_voice_chat_returns_transcript_reply_and_audio(
        self,
        _transcribe,
        _generate,
        _synthesize,
    ) -> None:
        response = self.client.post(
            "/api/chat",
            files={
                "audio": (
                    "recording.wav",
                    b"RIFF\x00\x00\x00\x00WAVE",
                    "audio/wav",
                )
            },
            data={"history": "[]"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "transcript": "Pytanie",
                "reply": "Odpowiedź",
                "audio": base64.b64encode(b"audio").decode("ascii"),
            },
        )

    def test_voice_chat_rejects_non_wav_audio(self) -> None:
        response = self.client.post(
            "/api/chat",
            files={"audio": ("recording.webm", b"not-a-wav", "audio/webm")},
            data={"history": "[]"},
        )

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json()["detail"], "Audio must be a WAV file.")


if __name__ == "__main__":
    unittest.main()
