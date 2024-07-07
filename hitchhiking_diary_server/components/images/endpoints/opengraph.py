import io
from uuid import UUID

import staticmaps
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response
from staticmaps import Color

from hitchhiking_diary_server.core import settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Trip

OG_WIDTH = 1200
OG_HEIGHT = 630

router = APIRouter()


def create_map_with_points(coordinates, output_size=(OG_WIDTH, OG_HEIGHT)):
    # Create a new static map context
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)

    # Add points to the map
    for coord in coordinates:
        point = staticmaps.create_latlng(coord[0], coord[1])
        marker = staticmaps.Marker(point, color=Color(34, 139, 34), size=8)
        context.add_object(marker)

    # Render the map to an image
    image = context.render_cairo(output_size[0], output_size[1])

    # Save the image to an in-memory buffer
    buf = io.BytesIO()
    image.write_to_png(buf)
    buf.seek(0)

    return buf


@router.get("/opengraph/{trip_id}", response_class=Response)
async def opengraph_image(trip_id: UUID, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip does not exist!")

    img = Image.new("RGB", (OG_WIDTH, OG_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Generate a high-resolution map using py-staticmaps
    map_img_buf = create_map_with_points([(float(item.latitude), float(item.longitude)) for item in trip.records])
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
    logo.thumbnail((200, 181), Image.Resampling.LANCZOS)
    img.paste(logo, (10, 10), logo.convert("RGBA"))

    # Text
    trueno = ImageFont.truetype(settings.BASE_DIR / "static/fonts/Trueno.otf", 15)
    trueno_bold = ImageFont.truetype(settings.BASE_DIR / "static/fonts/TruenoBold.otf", 40)
    draw = ImageDraw.Draw(img)
    draw.text((220, 10), trip.title, fill="black", font=trueno_bold)
    draw.text((220, 55), trip.user.username, fill="black", font=trueno)

    # Convert back to RGB
    img = img.convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG", quality=100, optimize=True, dpi=(300, 300))
    buffer.seek(0)

    return Response(buffer.getvalue(), media_type="image/png")
