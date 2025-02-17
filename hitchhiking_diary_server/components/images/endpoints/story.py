import io
from typing import List
from uuid import UUID
from datetime import datetime

import staticmaps
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from hitchhiking_diary_server.components.images.staticmaps import CustomImageMarker
from hitchhiking_diary_server.core import settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Trip, TripRecordType, TripRecord

INSTAGRAM_STORY_WIDTH = 1080
INSTAGRAM_STORY_HEIGHT = 1920

router = APIRouter()


def create_map_with_points(records: List[TripRecord], output_size=(INSTAGRAM_STORY_WIDTH, INSTAGRAM_STORY_HEIGHT)):
    # Create a new static map context
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)

    # Add points to the map
    for record in records:
        point = staticmaps.create_latlng(record.latitude, record.longitude)
        marker = CustomImageMarker(
            point,
            file=f"{settings.BASE_DIR}/static/images/marker-{record.type.value}.png",
            size=(64, 64),
        )
        context.add_object(marker)

    # Render the map to an image
    image = context.render_cairo(output_size[0], output_size[1])

    # Save the image to an in-memory buffer
    buf = io.BytesIO()
    image.write_to_png(buf)
    buf.seek(0)

    return buf


@router.get("/story/{trip_id}", response_class=Response)
async def story_image(
    trip_id: UUID,
    db: Session = Depends(get_db),
    day: str = Query(None, description="Optional date filter in Y-m-d format"),
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip does not exist!")

    # If the day parameter is provided, process it here
    if day:
        try:
            day = datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format! Use Y-m-d.")

        records = [
            record for record in trip.records if record.happened_at.strftime("%Y-%m-%d") == day.strftime("%Y-%m-%d")
        ]
        day_num = (day.date() - trip.records[-1].happened_at.date()).days + 1
    else:
        day_num = None
        records = trip.records

    stats = {record_type: 0 for record_type in TripRecordType}

    for record in records:
        stats[record.type] += 1

    img = Image.new("RGB", (INSTAGRAM_STORY_WIDTH, INSTAGRAM_STORY_HEIGHT), color=(255, 255, 255))

    # Generate a high-resolution map using py-staticmaps
    map_img_buf = create_map_with_points(records)
    map_img = Image.open(map_img_buf)

    # Adjust the opacity of the map image
    map_img = map_img.convert("RGBA")
    alpha = map_img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.7)
    map_img.putalpha(alpha)

    # Paste the map onto the base image
    img = img.convert("RGBA")
    img.paste(map_img, (0, 0), map_img)

    # Logo
    logo = Image.open(settings.BASE_DIR / "static/images/logo-rounded.jpg")
    logo.thumbnail((200, 200), Image.Resampling.LANCZOS)  # Adjust size as needed
    img.paste(logo, (10, 110), logo.convert("RGBA"))

    # Text
    futura = ImageFont.truetype(settings.BASE_DIR / "static/fonts/Futura.ttf", 50)
    futura_small = ImageFont.truetype(settings.BASE_DIR / "static/fonts/Futura.ttf", 30)
    futura_big = ImageFont.truetype(settings.BASE_DIR / "static/fonts/Futura.ttf", 100)

    draw = ImageDraw.Draw(img)

    if day_num:
        draw.text((220, 100), trip.title, fill="black", font=futura_big)
        draw.text((220, 220), f"Day #{day_num} ({day.date()})", fill="black", font=futura)
    else:
        draw.text((220, 150), trip.title, fill="black", font=futura_big)
    draw.text((15, 290), "hitchhikingdiary.app", fill="black", font=futura_small)
    draw.text((15, 400), f"Total records: {len(trip.records)}", fill="black", font=futura)
    draw.text((15, 450), f"Pickups: {stats[TripRecordType.pickup]}", fill="black", font=futura)

    # Convert back to RGB
    img = img.convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG", quality=100, optimize=True, dpi=(300, 300))
    buffer.seek(0)

    return Response(buffer.getvalue(), media_type="image/png")
