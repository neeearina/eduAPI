import typing

import fastapi

import oauth2
import session
import shemas

router = fastapi.APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/", response_model=typing.List[shemas.TagOut])
def get_all_tags(limit: int = 10):
    """Получить все теги"""
    with session.Session() as my_session:
        tags = (
            my_session.query(session.Tags).limit(limit).all()
        )
        if not tags:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="no tags",
            )
        return tags


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.TagOut)
def create_tag(tag_info: shemas.TagBase,
               get_current_user: int =
               fastapi.Depends(oauth2.get_current_user)):
    """Создать тег"""
    with session.Session() as my_session:
        new_tag = session.Tags(**tag_info.dict())
        my_session.add(new_tag)
        my_session.commit()
        return (
            my_session.query(session.Tags)
            .filter_by(id=new_tag.id).first()
        )


@router.get("/{tag_id}", response_model=shemas.TagOut)
def get_tag_by_id(tag_id: int):
    """Получить определенный тег"""
    with session.Session() as my_session:
        tag = (my_session.query(session.Tags)
               .filter_by(id=tag_id).first())
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no tag with id: {tag_id}",
            )
        return tag


@router.put("/{tag_id}", response_model=shemas.TagOut)
def put_tag_by_id(tag_id: int, update_tag_info: shemas.TagBase,
                  get_current_user: int =
                  fastapi.Depends(oauth2.get_current_user)):
    """Изменить определенный тег"""
    with session.Session() as my_session:
        tag_query = my_session.query(session.Tags).filter_by(id=tag_id)
        tag = tag_query.first()
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no tag with id: {tag_id}",
            )
        tag_query.update(update_tag_info.dict(), synchronize_session=False)
        my_session.commit()
        return tag_query.first()


@router.delete("/{tag_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_tag_by_id(tag_id: int,
                     get_current_user: int =
                     fastapi.Depends(oauth2.get_current_user)):
    """Удалить определенный тег"""
    with session.Session() as my_session:
        tag_query = my_session.query(session.Tags).filter_by(id=tag_id)
        tag = tag_query.first()
        if not tag:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no tag with id: {tag_id}",
            )
        tag_query.delete(synchronize_session=False)
        my_session.commit()
        return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)
