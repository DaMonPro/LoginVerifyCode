
from PIL import Image
import tesseract.tesseract

image = Image.open('code1.png')
vcode = tesseract.tesseract..image_to_string(image)
print(vcode)

