from src.models import Canonical, Basic, Social, Advanced
def head_full(canon: Canonical, metadata: list[dict]) -> str:
    """ Returns the full metadata for a given path """
    if not metadata:
        return ""
    basic = Basic(**metadata[0])
    social = Social(**metadata[1])
    advanced = Advanced(**metadata[2])
    
    return f"""
    <title>{basic.title}</title>
    <meta name="description" content="{basic.description}">
    <meta name="author" content="{basic.author}">
    <meta name="date" content="{basic.date}">
    <meta name="modified" content="{basic.modified}">
    <link rel="canonical" href="{canon.canonical}">
    <meta property="og:title" content="{social.image}">
    <meta property="og:image" content="{social.image}">
    """

