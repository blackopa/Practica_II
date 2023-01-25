
# Requires Python 3.6 or higher due to f-strings

# Import libraries
import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
#import cv2

if platform.system() == "Windows":
	# We may need to do some additional downloading and setup...
	# Windows needs a PyTesseract Download
	# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

	pytesseract.pytesseract.tesseract_cmd = (
		r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	)

	# Windows also needs poppler_exe
	path_to_poppler_exe = Path(r"C:\.....")
	
	# Put our output files in a sane place...
	out_directory = Path(r"D:\OneDrive - Ministerio de Educación\Escritorio\Practica\LecturaPdf").expanduser()
else:
	out_directory = Path("~").expanduser()	

# Path of the Input pdf
PDF_file = Path(r"informeFinal5393.pdf")

# Store all the pages of the PDF in a variable
image_file_list = []

text_file = out_directory / Path("out_text.txt")

def mark_region(image_path):
    
    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])


    return image, line_items_coordinates
def imagen_a_texto():
	# load the original image
	image = cv2.imread('Original_Image.jpg')

	# get co-ordinates to crop the image
	c = line_items_coordinates[1]

	# cropping image img = image[y0:y1, x0:x1]
	img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

	plt.figure(figsize=(10,10))
	plt.imshow(img)

	# convert the image to black and white for better OCR
	ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

	# pytesseract image to string to get results
	text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
	return(text)

def main():
	''' Main execution point of the program'''
	with TemporaryDirectory() as tempdir:
		# Create a temporary directory to hold our temporary images.

		"""
		Part #1 : Converting PDF to images
		"""

		if platform.system() == "Windows":
			pdf_pages = convert_from_path(
				PDF_file, 300, poppler_path=path_to_poppler_exe,first_page=43,last_page=45,timeout=360
			)
		else:
			pdf_pages = convert_from_path(PDF_file, 300,first_page=43,last_page=45,timeout=360)
		# Read in the PDF file at 500 DPI

		# Iterate through all the pages stored above
		for page_enumeration, page in enumerate(pdf_pages, start=1):
			# enumerate() "counts" the pages for us.

			# Create a file name to store the image
			filename = f"{tempdir}\page_{page_enumeration:03}.jpg"

			# Declaring filename for each page of PDF as JPG
			# For each page, filename will be:
			# PDF page 1 -> page_001.jpg
			# PDF page 2 -> page_002.jpg
			# PDF page 3 -> page_003.jpg
			# ....
			# PDF page n -> page_00n.jpg

			# Save the image of the page in system
			page.save(filename, "JPEG")
			image_file_list.append(filename)

		"""
		Part #2 - Recognizing text from the images using OCR
		"""

		with open(text_file, "a") as output_file:
			# Open the file in append mode so that
			# All contents of all images are added to the same file

			# Iterate from 1 to total number of pages
			for image_file in image_file_list:

				# Set filename to recognize text from
				# Again, these files will be:
				# page_1.jpg
				# page_2.jpg
				# ....
				# page_n.jpg

				# Recognize the text as string in image using pytesserct
				text = str(((pytesseract.image_to_string(Image.open(image_file)))))

				# The recognized text is stored in variable text
				# Any string processing may be applied on text
				# Here, basic formatting has been done:
				# In many PDFs, at line ending, if a word can't
				# be written fully, a 'hyphen' is added.
				# The rest of the word is written in the next line
				# Eg: This is a sample text this word here GeeksF-
				# orGeeks is half on first line, remaining on next.
				# To remove this, we replace every '-\n' to ''.
				text = text.replace("-\n", "")

				# Finally, write the processed text to the file.
				output_file.write(text)

			# At the end of the with .. output_file block
			# the file is closed after writing all the text.
		# At the end of the with .. tempdir block, the
		# TemporaryDirectory() we're using gets removed!	
	#mark_region(image_path)
	# End of main function!
	
if __name__ == "__main__":
	# We only want to run this if it's directly executed!
	main()
