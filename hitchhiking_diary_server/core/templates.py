from fastapi.templating import Jinja2Templates

from hitchhiking_diary_server.core.conf import settings

templates = Jinja2Templates(
    directory=settings.BASE_DIR / "hitchhiking_diary_server/templates",
    context_processors=[
        lambda request: {
            'settings': settings
        },
    ]
)
