from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models import Resource, ResourceCreate, ResourceUpdate

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.post("/", response_model=Resource)
async def create_resource(resource: ResourceCreate, session: SessionDep):
    db_resource = Resource.model_validate(resource)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)

    return db_resource


@router.get("/", response_model=list[Resource])
async def read_resources(session: SessionDep):
    return session.exec(select(Resource)).all()


@router.get("/{resource_id}", response_model=Resource)
async def read_resource(resource_id: int, session: SessionDep):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.patch("/{resource_id}", response_model=Resource)
async def update_resource(resource_id: int, updated: ResourceUpdate, session: SessionDep):
    db_resource = session.get(Resource, resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail="User not found")

    resource_data = updated.model_dump(exclude_unset=True)
    db_resource.sqlmodel_update(resource_data)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@router.delete("/{resource_id}", response_model=Resource)
async def delete_resource(resource_id: int, session: SessionDep):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    session.delete(resource)
    session.commit()
    return resource
