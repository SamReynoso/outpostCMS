from fastapi.templating import Jinja2Templates
from fastapi import Request
from lib.locached import Cache
from src.models import Entry


class EntryResponse:
    _templates = Jinja2Templates(directory="templates")

    def __init__(self, request: Request, template_name: str, canon_id: str | None = None):
        self.request = request
        self.template_name = template_name

        if canon_id is None:
            if Cache.canon is None:
                entry = Entry.new()
            else:
                canon = Cache.canon
                metadata = Cache.metadata
                entry = Entry(
                    canon=canon,
                    basic=metadata[0],
                    social=metadata[1],
                    advanced=metadata[2],
                )
        else:
            canon = Cache.canon_by_id(canon_id)
            metadata = Cache.metadata_by_id(canon_id)
            entry = Entry(
                canon=canon,
                basic=metadata[0],
                social=metadata[1],
                advanced=metadata[2],
            )
        self.context = {
            "request": request,
            "title": "Outpost CMS",
            "description": "Outpost CMS is a simple, fast, and easy-to-use content management system.",
            "keywords": "Outpost CMS, content management system, fastapi, python",
            "entry": entry,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.context[key] = value


    def as_response(self):
        return self._templates.TemplateResponse(self.template_name, self.context)
