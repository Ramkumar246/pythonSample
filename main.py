from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
from datetime import datetime

app = FastAPI()
# Define the directory where converted images will be saved
SAVE_DIRECTORY = "converted_images"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": "hiiiiiiman"}

# Ensure the save directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

@app.post("/convert-image/")
async def convert_image(file: UploadFile = File(...), format: str = "jpeg"):
    # Load the image file
    image = Image.open(io.BytesIO(await file.read()))

    # Convert image mode if necessary (JPEG does not support alpha channel)
    if format.lower() == "jpeg" and image.mode == "RGBA":
        image = image.convert("RGB")
    elif format.lower() == "jpeg" and image.mode != "RGB":
        image = image.convert("RGB")

    # Clear the save directory before saving the new image
    clear_save_directory()

    # Create a filename for the converted image
    original_filename, file_extension = os.path.splitext(file.filename)
    save_path = os.path.join(SAVE_DIRECTORY, original_filename + "." + format.lower())

    # Save the converted image to the file system
    image.save(save_path, format=format.upper())

    # Return the path to the saved file
    return JSONResponse(content={"file_path": save_path})

def clear_save_directory():
    # Remove all files in the save directory
    for filename in os.listdir(SAVE_DIRECTORY):
        file_path = os.path.join(SAVE_DIRECTORY, filename)
        os.remove(file_path)