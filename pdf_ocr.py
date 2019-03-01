from wand.image import Image
from PIL import Image as PI
import pyocr.builders
import io

path = "C:\\Users\\KYJ\\aa.pdf"
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0] // 0 is eng

req_image = []
final_text = []

image_pdf = Image(filename=path, resolution=300)
image_jpeg = image_pdf.convert('jpeg')


for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))

for img in req_image:
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    final_text.append(txt)
