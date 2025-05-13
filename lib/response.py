from fastapi.templating import Jinja2Templates


class PFResponse:
    _templates = Jinja2Templates(directory="templates")

    def __init__(self, request, template):
        self.template = template
        self.context = {"request": request}

    def update(self, **kwargs):
        self.context.update(kwargs)

    @property
    def title(self):
        return self.context.get("title")

    def __call__(self):

        if not self.title:
            raise ValueError("PFResponse: Missing required field 'title'")
        return self._templates.TemplateResponse(self.template, self.context)
