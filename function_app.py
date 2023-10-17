import azure.functions as func
import logging
from PIL import Image
import io   #! Should I specify that we are only using Bytes?

app = func.FunctionApp()

#@app.blob_output(arg_name="outputblob", path="thumbnails/", connection="")
@app.blob_output(arg_name="outputblob", path="thumbnails/{name}_thumbnail.png", connection="")  # the suffix of path defines the file type and must match the input
#! The name of the outputblob could be improved by removing the .png from the input file
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
        thumbnail = Image.open(io.BytesIO(myblob.read())) 

        # Create the thumbnail by resizing according to the size tuple
        thumbnail.thumbnail(size)
        logging.info(f"Created")

        #! We could create a section for file conversion here
                
        # Save the thumbnail as a BytesIO object
        thumbnail_bytes = io.BytesIO()
        thumbnail.save(thumbnail_bytes, format='PNG') # format should match input file type #! Could be made safer by using the extension of the input file
        thumbnail_bytes.seek(0)
        logging.info(f"Converted")

        # Upload the thumbnail to the output container by setting the outputblob
        outputblob.set(thumbnail_bytes.read())
        logging.info(f"Python blob trigger function created thumbnail for blob: {myblob.name}")

    except:
        logging.info(f"Thumbnail failed to create.")

''' 
From what filetypes can a PIL.Image object be created?

A PIL.Image object can be created from a variety of file types, including:

JPEG
PNG
BMP
GIF
TIFF
WebP
ICO
PDF
In addition to file types, PIL.Image objects can also be created from in-memory data, such as bytes or byte arrays.

In the context of the code you provided, the PIL.Image object is created from the myblob input stream, which is passed to the Image.open() method as a BytesIO object. 
The BytesIO object is created by calling the read() method on the myblob input stream, which returns the image data as bytes.
'''

''''
Is it necessary to convert the myblob input to a BytesIO object?

Yes, it is necessary to convert the myblob input to a BytesIO object before passing it to the Image.open() method.

The Image.open() method expects a file-like object as input, which means that it needs to be able to read data from the object using the read() method.

In the context of the code you provided, myblob is an input stream that represents the image data. 
To pass this data to the Image.open() method, it needs to be wrapped in a file-like object that provides a read() method.

The io.BytesIO() function creates a BytesIO object that behaves like a file, but is backed by an in-memory buffer instead of a physical file on disk. 
By calling myblob.read() and passing the result to io.BytesIO(), the image data is loaded into memory as a BytesIO object, which can then be passed to the Image.open() method.
'''