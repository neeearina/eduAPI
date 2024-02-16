import typing

import fastapi

import session
import shemas

router = fastapi.APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/", response_model=typing.List[shemas.Tag])
def get_all_tags(limit: int = 10):
    """Получить все теги, которые есть"""

    with session.Session as my_session:
        return (
            my_session.query(session.Tags).limit(limit).all()
        )


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.Tag)
def create_tag(tag_info: shemas.TagBase):
    """Создать новый тег"""
    with session.Session() as my_session:
        new_tag = session.Tags(**tag_info.dict())
        my_session.add(new_tag)
        my_session.commit()
        return (
            my_session.query(session.Tags)
            .filter_by(id=new_tag.id.first())
        )
