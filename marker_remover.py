from PIL import Image
import numpy as np
import pypdfium2 as pdfium


def transform(image):
    # image.show()
    r, g, b = image.split()
    A = np.asarray(r)

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i, j] > 240:
                A[i, j] = 255

    r = Image.fromarray(A).convert('L')
    return r


filepath = input("Input RELATIVE path:")
pdf = pdfium.PdfDocument(filepath)

# first page:
page = pdf.get_page(0)
pil_image = page.render_to(
    pdfium.BitmapConv.pil_image,
)
page.close()
page1 = transform(pil_image)

print(
    "\t------------------------------------------------------Rendering PDF into jpg-----------------------------------------------")
n_pages = len(pdf)  # get the number of pages in the document
image_list = []

# load the rest of the document:
if n_pages > 1:
    for i in range(1, n_pages):
        page = pdf.get_page(i)
        pil_image = page.render_to(
            pdfium.BitmapConv.pil_image,
        )
        page.close()
        image_list.append(transform(pil_image))

print(
    "\n\n\t------------------------------------------------------num of pages found: {} ----------------------------------------------".format(
        len(image_list) + 1))
print(
    "\n\n\t------------------------------------------------------Saving back to pdf---------------------------------------------------")

# create and save a single pdf file:
page1.save(filepath[:-4] + "_CLEAN.pdf", save_all=True, append_images=image_list)
print(
    "\n\n\t------------------------------------------------------Proccess Completed!--------------------------------------------------")
