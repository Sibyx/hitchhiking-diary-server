import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic_xml import BaseXmlModel, element, attr

NSMAP = {
    "": "http://www.w3.org/2005/Atom",
}


class AtomAuthor(BaseXmlModel, tag="author", nsmap=NSMAP):
    name: str = element()
    uri: Optional[str] = element(default=None)  # TODO: Implement author feeds


class AtomContent(BaseXmlModel, tag="content", nsmap=NSMAP):
    type: str = attr()
    value: str


class AtomLinkType(str, Enum):
    ALTERNATE = "alternate"


class AtomLink(BaseXmlModel, tag="link", nsmap=NSMAP):
    rel: Optional[AtomLinkType] = attr(default=None)
    href: str = attr()


class AtomGenerator(BaseXmlModel, tag="generator", nsmap=NSMAP):
    uri: Optional[str] = attr(default=None)
    version: Optional[str] = attr(default=None)
    value: str = attr()


class AtomEntry(BaseXmlModel, nsmap=NSMAP):
    id: UUID = element()
    title: str = element()
    updated: datetime.datetime = element()
    links: List[AtomLink] = element(tag="link", default=list())
    content: AtomContent


class AtomFeed(BaseXmlModel, tag="feed", nsmap=NSMAP):
    id: UUID = element()
    icon: str = element(default=None)
    links: List[AtomLink] = element(tag="link", default=list())
    title: str = element()
    updated: datetime.datetime = element()
    author: AtomAuthor = element()
    entries: List[AtomEntry] = element(tag="entry", default=list())
