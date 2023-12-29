import cv2
import sys
import pyautogui
import pytesseract


def read_white_text_on_image(image_path): 

	# Grayscale, Gaussian blur, Otsu's threshold
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (3,3), 0)
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	# Morph open to remove noise and invert image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
	invert = 255 - opening

	# Perform text extraction
	data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

	return data


def table_blinds():
	"""
	Doesn't matter if other things are in the screenshot, as long as the numbers of the blinds ar ein the
	string that is enough.
	(R)!!!!
	So if the blinds are 0.20/0.40, as long as this is in the end result then it is fine.
	"""

	# VIDEO coordinates
	blinds = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/table_blinds.png", region=(895, 1029, 120, 36))

	# real app coordinates
	blinds = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/table_blinds.png", region=(895, 1029, 120, 36))

	# blinds.show()
	blinds = blinds.resize((160, 40))
	blinds.save(f"{sys.path[0]}/photo_dump/table_blindss.png")
	blinds = f"{sys.path[0]}/photo_dump/table_blindss.png"

	return read_white_text_on_image(blinds)


print(table_blinds())
