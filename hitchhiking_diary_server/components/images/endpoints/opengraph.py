from io import BytesIO
from uuid import UUID

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from hitchhiking_diary_server.core import settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Trip

OG_WIDTH = 1200
OG_HEIGHT = 630

router = APIRouter()


def generate_map_with_osm(markers: list[tuple[float, float]]):
    # Use OSM tiles from Cartopy
    osm_tiles = OSM()

    # Determine the extent based on the markers
    lats, lons = zip(*markers)
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    # Create a figure and axis with the OSM tiles
    fig, ax = plt.subplots(figsize=(12, 6.3), dpi=200, subplot_kw={"projection": osm_tiles.crs})
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

    # Add the OSM tiles to the axis
    ax.add_image(osm_tiles, 10)  # The 10 here is the zoom level

    # Plot markers
    for lat, lon in markers:
        ax.plot(lon, lat, "o", color="red", markersize=10, transform=ccrs.PlateCarree())

    # Remove axis for cleaner look
    ax.set_axis_off()

    # Save map to buffer
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return buf


@router.get("/opengraph/{trip_id}", response_class=Response)
async def opengraph(trip_id: UUID, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip does not exist!")

    img = Image.new("RGB", (OG_WIDTH, OG_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Logo
    logo = Image.open(settings.BASE_DIR / "static/images/logo-rounded.jpg")
    logo.thumbnail((200, 181), Image.Resampling.LANCZOS)
    img.paste(logo, (10, 10))

    # Text
    trueno = ImageFont.truetype(settings.BASE_DIR / "static/fonts/Trueno.otf", 15)
    trueno_bold = ImageFont.truetype(settings.BASE_DIR / "static/fonts/TruenoBold.otf", 40)
    draw.text((220, 10), trip.title, fill="black", font=trueno_bold)
    draw.text((220, 55), trip.user.username, fill="black", font=trueno)

    # Generate a high-resolution map using Cartopy and contextily
    map_img = Image.open(
        generate_map_with_osm([(float(item.latitude), float(item.longitude)) for item in trip.records])
    )
    map_img = ImageEnhance.Brightness(map_img).enhance(0.7)
    img.paste(map_img, (0, 0), map_img)

    buffer = BytesIO(img.tobytes())
    img.save(buffer, format="JPEG", quality=100, optimize=True, dpi=(300, 300))
    buffer.seek(0)

    return Response(buffer.getvalue(), media_type="image/jpg")
