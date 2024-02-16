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


@router.get("/{tag_id}", response_model=shemas.Tag)
def get_tag_by_id(tag_id: int):
    """Получить тег по id"""
    with session.Session() as my_session:
        tag = (
            my_session.query(session.Tags)
            .filter_by(id=tag_id).first()
        )
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no tag with id: {tag_id}",
            )
        return tag


@router.put("/{tag_id}", response_model=shemas.Tag)
def put_tag_by_id(tag_id: int, update_tag_info: shemas.TagBase):
    """Изменить тег по его id"""
    with session.Session() as my_session:
        tag_query = my_session.query(session.Tags).filter_by(id=tag_id)
        tag = tag_query.first()
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"tag with id: {tag_id} was not found",
            )
        tag_query.update(update_tag_info.dict(), synchronize_session=False)
        my_session.commit()
        return tag_query.first()


@router.delete("/{tag_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_tag_by_id(tag_id: int):
    """Удалить тег по его id"""
    with session.Session() as my_session:
        tag_query = my_session.query(session.Tags).filter_by(id=tag_id)
        tag = tag_query.first()
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"tag with id: {tag_id} was not found",
            )
        tag_query.delete(synchronize_session=False)
        my_session.commit()
        return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)
