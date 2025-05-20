from pydantic import BaseModel, Field
from datetime import datetime


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

    hash: str | None = Field(..., title="Hash")
    public: bool = Field(False, title="Public Access")

    @staticmethod
    def new():
        return Canonical(
            group="",
            project="",
            canonical="",
            hash=None,
            public=False,
        )

    @property
    def id(self) -> str:
        return f"{self.group}/{self.project}"

class Basic(OutpostModel):
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    author: str = Field(..., title="Author")
    date: datetime = Field(..., title="Date")
    modified: datetime = Field(..., title="Last Update")

    @staticmethod
    def new():
        return Basic(
            title="",
            description="",
            author="",
            date=datetime.now(),
            modified=datetime.now(),
        )

class Social(OutpostModel):
    image: str = Field(..., title="Image URL")
    image_alt: str = Field(..., title="Image Alt Text")
    site_name: str = Field(..., title="Site Name")
    site_url: str = Field(..., title="Site URL")
    short_description: str = Field(..., title="Short Description")
    tags: str = Field(..., title="Tags")
    twitter_site: str = Field(..., title="Twitter Site Handle")
    twitter_creator: str = Field(..., title="Twitter Creator Handle")
    twitter_card: str = Field(..., title="Twitter Card Type")
    og_type: str = Field(..., title="Open Graph Type")
    og_section: str = Field(..., title="Open Graph Section")

    @staticmethod
    def new():
        return Social(
                image="",
                image_alt="",
                site_name="",
                site_url="",
                short_description="",
                tags="",
                twitter_site="",
                twitter_creator="",
                twitter_card="summary",
                og_type="website",
                og_section="",
                )




class Advanced(OutpostModel):
    twitter_title: str = Field(..., title="Twitter Title")
    twitter_description: str = Field(..., title="Twitter Description")
    twitter_image: str = Field(..., title="Twitter Image URL")
    twitter_image_alt: str = Field(..., title="Twitter Image Alt Text")
    og_title: str = Field(..., title="Open Graph Title")
    og_description: str = Field(..., title="Open Graph Description")
    og_image: str = Field(..., title="Open Graph Image URL")
    og_image_alt: str = Field(..., title="Open Graph Image Alt Text")
    og_url: str = Field(..., title="Open Graph URL")
    og_site_name: str = Field(..., title="Open Graph Site Name")
    og_locale: str = Field(..., title="Open Graph Locale")
    og_article_author: str = Field(..., title="Open Graph Article Author")
    og_article_section: str = Field(..., title="Open Graph Article Section")
    og_article_tags: str = Field(..., title="Open Graph Article Tags")
    schema_type: str = Field(..., title="Schema Type")
    schema_headline: str = Field(..., title="Schema Headline")
    schema_description: str = Field(..., title="Schema Description")
    schema_date: datetime = Field(..., title="Schema Date Published")
    schema_modified: datetime = Field(..., title="Schema Date Modified")
    schema_author: str = Field(..., title="Schema Author")
    schema_publisher: str = Field(..., title="Schema Publisher")

    @staticmethod
    def new():
        return Advanced(
                twitter_title="",
                twitter_description="",
                twitter_image="",
                twitter_image_alt="",
                og_title="",
                og_description="",
                og_image="",
                og_image_alt="",
                og_url="",
                og_site_name="",
                og_locale="en_US",
                og_article_author="",
                og_article_section="",
                og_article_tags="",
                schema_type="WebPage",
                schema_headline="",
                schema_description="",
                schema_date=datetime.now(),
                schema_modified=datetime.now(),
                schema_author="",
                schema_publisher="",
        )



class Upload(OutpostModel):
    index_html_file: str = Field(..., title="Index HTML File")


class Entry(BaseModel):
    canon: Canonical 
    basic: Basic
    social: Social
    advanced: Advanced

    @staticmethod
    def new():
        return Entry(
            canon=Canonical.new(),
            basic=Basic.new(),
            social=Social.new(),
            advanced=Advanced.new(),
        )

    @property
    def id(self):
        return self.canon.id

    def __str__(self):
        return f"Entry({self.canon}, {self.basic}, {self.social}, {self.advanced})"
