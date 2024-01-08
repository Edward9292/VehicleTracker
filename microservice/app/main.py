import os
import pathlib
import uuid
from .tracking import process_video

from fastapi import (
    FastAPI,
    File,
    UploadFile,
)
from fastapi.responses import (
    FileResponse,
)
import io

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home_view():
    return {"message": "Hello World GET"}

@app.post("/")
def home_detail_view():
    return {"message": "Hello World POST"}

@app.post("/video-echo/", response_class=FileResponse) # HTTP POST
async def video_echo(file: UploadFile = File(...)):
    print("file",file)
    bytes_stream = io.BytesIO(await file.read())
    f_name = pathlib.Path(file.filename)
    f_ext = f_name.suffix # .jpg, .mp4, .png
    destination = UPLOAD_DIR / f"{uuid.uuid1()}{f_ext}"
    ##how to save the file in the server
    with open(str(destination), "wb") as out:
        out.write(bytes_stream.read())
    return destination

@app.post("/video-render/", response_class=FileResponse) # HTTP POST
async def video_render(file: UploadFile = File(...)):
    print("file", file)
    bytes_stream = io.BytesIO(await file.read())
    f_name = pathlib.Path(file.filename)
    f_ext = f_name.suffix
    input_video_path = UPLOAD_DIR / f"{uuid.uuid1()}{f_ext}"
    output_video_path = UPLOAD_DIR / f"{uuid.uuid1()}_processed{f_ext}"

    with open(str(input_video_path), "wb") as out:
        out.write(bytes_stream.read())

    process_video(str(input_video_path), str(output_video_path))

    return output_video_path