from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from hitchhiking_diary_server.components.atom.schemas import (
    AtomFeed,
    AtomLink,
    AtomLinkType,
    AtomAuthor,
    AtomEntry,
    AtomContent,
)
from hitchhiking_diary_server.core import templates
from hitchhiking_diary_server.core.responses import XMLResponse
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Trip

router = APIRouter()


@router.get("/trips/{trip_id}", response_class=XMLResponse)
async def atom_trip_feed(request: Request, trip_id: UUID, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter((Trip.id == trip_id) & (Trip.deleted_at == None)).first()

    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip does not exist!")

    feed = AtomFeed(
        id=trip.id,
        icon=str(request.url_for("static", path="/images/logo.jpg")),
        links=[
            AtomLink(
                rel=AtomLinkType.ALTERNATE,
                href=f'{request.url_for("explore_trip_detail", trip_id=trip.id)}',
            )
        ],
        title=trip.title,
        updated=max(trip.updated_at, trip.records[0].updated_at if trip.records else None),
        author=AtomAuthor(name=trip.user.username),
    )

    for record in trip.records:
        last_updates = [photo.updated_at for photo in record.photos] + [record.updated_at]
        entry = AtomEntry(
            id=record.id,
            title=f"{record.type.title()}: {record.happened_at.strftime('%d.%m.%Y %H:%M %Z')}",
            updated=max(last_updates),
            links=[
                AtomLink(
                    rel=AtomLinkType.ALTERNATE,
                    href=f'{request.url_for("explore_trip_detail", trip_id=trip.id)}#{record.id}',
                )
            ],
            content=AtomContent(
                type="html",
                value=templates.get_template("atom/record.html").render({"record": record, "request": request}),
            ),
        )
        feed.entries.append(entry)

    return XMLResponse(feed, media_type="application/atom+xml")
