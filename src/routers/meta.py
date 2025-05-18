from fastapi import Request, APIRouter
from lib.response import EntryResponse
from templates.metadata.forms import TEMPLATE_CONTEXT


class ViewDispatchError(Exception):
    """Custom exception for view dispatch errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def view_dispatch(template_id: str):
    """Dispatches a view based on the template ID."""
    context = TEMPLATE_CONTEXT.get(template_id, None)
    if not context:
        raise ViewDispatchError(
                f"Template ID '{template_id}' not found in TEMPLATE_CONTEXT."
                )
    async def _dispatch(request: Request):
        resp = EntryResponse(request, context["template"])
        resp.update(**context)
        return resp.as_response()
    return _dispatch


meta_router = APIRouter()


meta_router.add_api_route("/new/", view_dispatch("new"), methods=["GET"])
meta_router.add_api_route("/canonical/", view_dispatch("canonical"), methods=["GET"])
meta_router.add_api_route("/basic/", view_dispatch("basic"), methods=["GET"])
meta_router.add_api_route("/social/", view_dispatch("social"), methods=["GET"])
meta_router.add_api_route("/advanced/", view_dispatch("advanced"), methods=["GET"])
meta_router.add_api_route("/upload/", view_dispatch("upload"), methods=["GET"])
