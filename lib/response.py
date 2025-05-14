from fastapi.templating import Jinja2Templates
from fastapi import Request


class MetaTemplateResponse:
    _templates = Jinja2Templates(directory="templates")

    def __init__(self, request, template):
        self.template = template
        self.context = {"request": request}

    def update(self, **kwargs):
        self.context.update(kwargs)

    @property
    def title(self):
        return self.context.get("title")


class PFResponse(MetaTemplateResponse):
    def __call__(self):
        if not self.title:
            print("[ERROR] PFResponse: Missing required field 'title'")
            raise ValueError("PFResponse: Missing required field 'title'")
        try:
            return self._templates.TemplateResponse(self.template, self.context)
        except Exception as e:
            print(f"[ERROR] PFResponse: Error rendering template {self.template}: {e}")
            raise e


class MetadataResponse(MetaTemplateResponse):
    def __init__(self, request, template):
        super().__init__(request, template)

    @property
    def form_action(self):
        return self.context.get("form_action")

    @property
    def form_header(self):
        return self.context.get("form_header")
    
    @property
    def form_description(self):
        return self.context.get("form_description")

    @property
    def entry(self):
        return self.context.get("entry")

    def __call__(self):
        if not all([self.title, self.form_action, self.form_header]):
            print("[ERROR] MetadataResponse: Missing required fields")
            raise ValueError("MeatDataResponse: Missing required fields")
        if not self.entry:
            print("[ERROR] MetadataResponse: Missing required field 'entry'")
            raise ValueError("MeatDataResponse: Missing required field 'entry'")
        try:
            return self._templates.TemplateResponse(self.template, self.context)
        except Exception as e:
            print(f"[ERROR] MetadataResponse: Error rendering template {self.template}: {e}")
            raise e


