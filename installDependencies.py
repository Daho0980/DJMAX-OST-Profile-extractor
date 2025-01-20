from os import system


for lib in ("Pillow", "pdf2image"):
    try:                        __import__(lib),
    except ModuleNotFoundError: system(f"pip install {lib}")