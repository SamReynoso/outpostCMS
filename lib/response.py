from fastapi.templating import Jinja2Templates
from fastapi import Request
from lib.locached import Cache


class EntryResponse:
    _templates = Jinja2Templates(directory="templates")

    def __init__(self, request: Request, template_name: str):
        self.request = request
        self.template_name = template_name
        self.entry = Cache.project
        self.context = {
            "request": request,
            "title": "Outpost CMS",
            "description": "Outpost CMS is a simple, fast, and easy-to-use content management system.",
            "keywords": "Outpost CMS, content management system, fastapi, python",
            "entry": self.entry,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.context[key] = value
        self.context["entry"] = Cache.project


    def as_response(self):
        return self._templates.TemplateResponse(self.template_name, self.context)
