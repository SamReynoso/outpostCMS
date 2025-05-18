from pydantic import BaseModel, Field, HttpUrl


class OutpostModel(BaseModel):

    def from_form(self, *args, **_) -> "OutpostModel":
        """
        Convert form data to model instance.
        """
        return self.model_validate(args[0])

    def as_schema(self) -> dict:
        return self.model_json_schema()

    def as_json(self: BaseModel) -> str:
        return self.model_dump_json()


class Canonical(OutpostModel):
    group: str = Field(..., title="Group Name")
    project: str = Field(..., title="Project Name")
    canonical: str = Field(..., title="Canonical URL")

    @property
    def id(self) -> str:
        return f"{self.group}/{self.project}"


class Basic(OutpostModel):
    title: str = Field(..., title="Title")
    author: str = Field(..., title="Author")
    description: str = Field(..., title="Description")
    date: str = Field(..., title="Date")
    last_update: str = Field(..., title="Last Update")


class Social(OutpostModel):
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    image: HttpUrl = Field(..., title="Image URL")
    twitter_card: str = Field(..., title="Twitter Card Type")
    twitter_site: str = Field(..., title="Twitter Site Handle")
    twitter_creator: str = Field(..., title="Twitter Creator Handle")
    og_type: str = Field(..., title="Open Graph Type")
    og_url: HttpUrl = Field(..., title="Open Graph URL")
    og_image: HttpUrl = Field(..., title="Open Graph Image URL")


class Advanced(OutpostModel):
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    image: HttpUrl = Field(..., title="Image URL")
    twitter_card: str = Field(..., title="Twitter Card Type")
    twitter_site: str = Field(..., title="Twitter Site Handle")
    twitter_creator: str = Field(..., title="Twitter Creator Handle")
    og_type: str = Field(..., title="Open Graph Type")
    og_url: HttpUrl = Field(..., title="Open Graph URL")
    og_image: HttpUrl = Field(..., title="Open Graph Image URL")


class Upload(OutpostModel):
    index_html_file: str = Field(..., title="Index HTML File")
