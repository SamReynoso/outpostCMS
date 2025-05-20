from src import models


TEMPLATE_CONTEXT = {
        "new": {
            "template": "metadata/canonical.html",
            "action": "/api/new/",
            "enctype": "application/x-www-form-urlencoded",
            "model": models.Canonical,
            "title": "New project",
            "subtitle": "Create a new project by filling out the form below.",
            "description": "This data is needed to create a new project.",
        },
        "upload": {
            "template": "metadata/upload.html",
            "action": "/api/upload/",
            "enctype": "multipart/form-data",
            "model": models.Upload,
            "title": "Upload File",
            "subtitle": "Upload your index.html file",
            "description": "Upload an HTML file to be used as the index page for your project.",
        },
        "canonical": {
            "template": "metadata/canonical.html",
            "action": "/api/canonical/",
            "enctype": "application/x-www-form-urlencoded",
            "model": models.Canonical,
            "title": "Canonical Metadata",
            "subtitle": "Canonical",
            "description": "Update canonical metadata for the project. This data should be updated for each project.",
        },
        "basic": {
            "template": "metadata/basic.html",
            "action": "/api/basic/",
            "enctype": "application/x-www-form-urlencoded",
            "model": models.Basic,
            "title": "Basic Metadata",
            "subtitle": "Basic",
            "description": "Add basic metadata for the project like title, author, and description.",
        },
        "social": {
            "template": "metadata/social.html",
            "action": "/api/social/",
            "enctype": "application/x-www-form-urlencoded",
            "model": models.Social,
            "title": "Social Metadata",
            "subtitle": "Social",
            "description": "Fill out the social metadata form to so that rich preview cards are generated for the project.",
        },
        "advanced": {
            "template": "metadata/advanced.html",
            "action": "/api/advanced/",
            "enctype": "application/x-www-form-urlencoded",
            "model": models.Advanced,
            "title": "Advanced Metadata",
            "subtitle": "Override",
            "description": "By default, the system will generate similar tags and JSON-LD data from the Basic and Social forms. If you want to override the default values to be platform specific, fill out the form below.",
        },
}
