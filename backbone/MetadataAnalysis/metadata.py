from PIL import Image, ExifTags


def getMetadata(path) : 
    """
    example path : /path/to/file.jpg
    """
    img = Image.open(path)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    return exif

