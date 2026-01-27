import shutil
from fastapi import APIRouter, UploadFile
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("", summary="Загрузить изображение отеля")
def upload_image(image: UploadFile):
    image_path = f"src/static/images/{image.filename}"

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=image.file, fdst=new_file)

    resize_image.delay(image_path)

    return {"status": "OK", "detail": "Изображение успешно загружено"}
