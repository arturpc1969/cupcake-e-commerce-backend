import os
from uuid import uuid4

from ninja import UploadedFile


# --- Auxiliar function to save image ---
def save_uploaded_image(image: UploadedFile) -> str:
    ext = image.name.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join('media', 'products', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return f"products/{filename}"
