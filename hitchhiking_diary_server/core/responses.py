import typing

from pydantic_xml import BaseXmlModel
from starlette.background import BackgroundTask
from starlette.responses import Response


class XMLResponse(Response):
    media_type = "text/xml"

    def __init__(
        self,
        content: BaseXmlModel,
        status_code: int = 200,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(
            content.to_xml(
                encoding="UTF-8",
                standalone=True,
                skip_empty=True,
            ),
            status_code,
            headers,
            media_type,
            background,
        )
