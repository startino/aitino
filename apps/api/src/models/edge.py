from typing import Optional, Union, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class Marker(BaseModel):
    type: str
    color: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    markerUnits: Optional[str] = None
    orient: Optional[str] = None
    strokeWidth: Optional[float] = None

class PathOptions(BaseModel):
    offset: Optional[float] = None
    borderRadius: Optional[float] = None
    curvature: Optional[float] = None

class Edge(BaseModel, Generic[T]):
    id: str
    type: Optional[str] = None
    source: str
    target: str
    sourceHandle: Optional[Union[str, None]] = None
    targetHandle: Optional[Union[str, None]] = None
    animated: Optional[bool] = None
    hidden: Optional[bool] = None
    deletable: Optional[bool] = None
    selectable: Optional[bool] = None
    data: Optional[T] = None
    selected: Optional[bool] = None
    markerStart: Optional[Union[str, Marker]] = None
    markerEnd: Optional[Union[str, Marker]] = None
    zIndex: Optional[int] = None
    ariaLabel: Optional[str] = None
    interactionWidth: Optional[float] = None
    label: Optional[str] = None
    labelStyle: Optional[str] = None
    style: Optional[str] = None
    class_: Optional[str] = Field(alias="class", default=None)
    pathOptions: Optional[PathOptions] = None

    class Config:
        populate_by_name = True