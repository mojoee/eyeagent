from PIL import Image
import pytesseract
from pyzbar.pyzbar import decode
from src.get_book_info import call_google_api


def read_image(src):
    """
    Reads an image from the specified source file.

    Parameters:
    src (str): The path to the image file.

    Returns:
    Image: An Image object representing the loaded image.
    """
    try:
        img = Image.open(src)
        return img
    except IOError:
        print(f"Error opening the image file at {src}")
        return None


def barcode_decode(img_path):
    return decode(read_image(img_path))


def process_image_to_info(filepath):
    results = barcode_decode(filepath)
    print(results)
    for result in results:
        ISBN = result.data.decode('utf-8')
        print(f"ISBN: {ISBN}")
        book_info = call_google_api(ISBN)
    print(10*"*")
    print(f"All book info {book_info}")
    return book_info