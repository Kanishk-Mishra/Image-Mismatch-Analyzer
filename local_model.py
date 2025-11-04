from PIL import Image, ImageChops

class LocalModel:
    def __init__(self):
        pass

    def compare_images(self, image1: Image.Image, image2: Image.Image) -> str:
        """
        Very basic pixel diff using PIL.
        Extend with your local model logic if needed.
        """

        diff = ImageChops.difference(image1, image2)
        bbox = diff.getbbox()

        if bbox:
            return "The images are different. Pixel differences detected."
        else:
            return "The images are identical. No differences detected."