import azure.functions as func
import logging
from PIL import Image
import io import BytesIO

app = func.FunctionApp()

#@app.blob_output(arg_name="outputblob", path="thumbnails/", connection="")
@app.blob_output(arg_name="outputblob", path="thumbnails/{name}_thumbnail.png", connection="")  # the suffix of path defines the file type and must match the input
@app.blob_trigger(arg_name="myblob", path="uploads/{name}", connection="")
def createThumbnail(myblob: func.InputStream, outputblob: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")

    # Create the thumbnail image using Pillow
    try:
        # Set the thumbnail size in pixels
        size = (128, 128)   

        # Instantiate a PIL.Image object from the input stream
        thumbnail = Image.open(BytesIO(myblob.read())) 

        # Create the thumbnail by resizing according to the size tuple
        thumbnail.thumbnail(size)
        logging.info(f"Created")
                
        # Save the thumbnail as a BytesIO object
        thumbnail_bytes = BytesIO()
        thumbnail.save(thumbnail_bytes, format='PNG') # format should match input file type
        thumbnail_bytes.seek(0)
        logging.info(f"Converted")

        # Upload the thumbnail to the output container by setting the outputblob
        outputblob.set(thumbnail_bytes.read())
        logging.info(f"Python blob trigger function created thumbnail for blob: {myblob.name}")

    except:
        logging.info(f"Thumbnail failed to create.")
