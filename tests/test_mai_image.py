import unittest

from mai_image import generation_url


class MaiImageTests(unittest.TestCase):
    def test_generation_url_accepts_resource_endpoint(self) -> None:
        self.assertEqual(
            generation_url("https://example.services.ai.azure.com"),
            "https://example.services.ai.azure.com/mai/v1/images/generations",
        )

    def test_generation_url_does_not_duplicate_api_path(self) -> None:
        self.assertEqual(
            generation_url(
                "https://example.services.ai.azure.com/mai/v1/images/generations/"
            ),
            "https://example.services.ai.azure.com/mai/v1/images/generations",
        )


if __name__ == "__main__":
    unittest.main()
