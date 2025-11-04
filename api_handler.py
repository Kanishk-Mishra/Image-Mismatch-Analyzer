import requests
from io import BytesIO
import base64
from PIL import Image

class MistralAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "pixtral-large-2411"

    def encode_image(self, image: Image.Image) -> str:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def compare_images(self, image1: Image.Image, image2: Image.Image) -> str:
        img1_b64 = self.encode_image(image1)
        img2_b64 = self.encode_image(image2)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if image1.width >= 224 and image2.height >= 224:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""You are a car cluster screen validator. Your task is to assess whether the graphics shown on the screen contain any visual mistakes.

                                You are provided with:
                                1. An actual (to-be-checked) image.
                                2. A reference (expected) image.                            

                                ---

                                ### What to flag as significant:
                                - Misalignments of functional elements (icons, text, telltales, etc.).                                
                                - Missing elements, texts, symbols, or icons (even if the overall images appear the same). This is a very critical bug.
                                - Font differnces (style, size, color, etc.).
                                - Textual differences (Use OCR to extract text and match).
                                - Shape, size, or contrasting color (e.g., red vs. green) inconsistencies in key visuals.
                                - Incomplete, overlapping, or cropped elements.

                                ### What to ignore as insignificant:
                                - Minor brightness or color tone differences (e.g., cyan vs. turquoise).
                                - Decorative background variations like misaligned dots or patterns.

                                ---

                                Based on your analysis:
                                - Briefly summarize the visual difference in one or two lines.
                                - Provide one of the following **verdicts** in the **next line only**:

                                - 'Verdict: Same images'
                                - 'Verdict: Similar images with insignificant differences'
                                - 'Verdict: Similar images with slight/major misalignment of element(s)'
                                - 'Verdict: Similar images but with one or few elements missing'
                                - 'Verdict: Similar images but with significant differences'
                                - 'Verdict: Dissimilar/Uncomparable images'
                                - 'Verdict: Inconclusive/Low-confidence findings; human discernment required'

                                Avoid any formatting in your output."""
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/png;base64,{img1_b64}"
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/png;base64,{img2_b64}"
                            },                            
                        ]
                    }
                ]
            }
        else:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""You are a car cluster screen validator. Your task is to assess whether the graphics shown on the screen contain any visual mistakes.

                                You are provided with:
                                1. An actual (to-be-checked) image.
                                2. A reference (expected) image.                   

                                ### What to flag as significant:                            
                                - Incomplete, overlapping, or cropped central element, treat it as a critical bug. This is a common and serious case.
                                - Color, shape, and size inconsistencies in key visuals. A color difference is considered a major bug (although very close shades of the same color are tolerable).
                                - Completely missing central element, text, symbol, or icon.
                                - Font differnces (style, size, weight, etc.) - again a critical bug.
                                - Textual differences (Use OCR to extract text and match).
                                - Color, shape and size inconsistencies in key visuals.
                                - Major Misalignment of the central element (icon, text, telltale, etc.).

                                ### What to ignore as insignificant:
                                - Decorative background variations like misaligned dots or different patterns.                            

                                💡 Tip:  These images were originally very small but were enlarged and enhanced before being sent to you. Examples include the ‘STOP’ icon image, battery icon image, etc.
                                Usually, these images are the same, with only insignificant misalignment differences. 
                                However, sometimes additional pixels from nearby elements — not present in the reference image — get captured in the frame of the actual image. 
                                After enlargement, they may appear large and significant, but since they are meaningless fragments, they should be ignored and only central element should be focused on.
                                
                                ---

                                Based on your analysis:
                                - Briefly summarize the visual difference in one or two lines.
                                - Provide one of the following **verdicts** in the **next line only**:

                                - 'Verdict: Same images'
                                - 'Verdict: Similar images with insignificant differences'
                                - 'Verdict: Similar images with major misalignment of element(s)'
                                - 'Verdict: Similar images but with significant differences'
                                - 'Verdict: Incomplete/Cropped central element'
                                - 'Verdict: Central element has different color'
                                - 'Verdict: Central text is different'
                                - 'Verdict: Central text's font is different'
                                - 'Verdict: Central element's shape is different'
                                - 'Verdict: Dissimilar/Uncomparable images'
                                - 'Verdict: Inconclusive/Low-confidence findings; human discernment required'

                                Avoid any formatting in your output."""
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/png;base64,{img1_b64}"
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/png;base64,{img2_b64}"
                            },
                        ]
                    }
                ]
            }
        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            response = f"Uanble to generate the review due to a server side error [Error: {response.status_code} {response.text}]. Kindly check this case manually."
            return response
            # raise Exception(f"API Error: {response.status_code} {response.text}")
            