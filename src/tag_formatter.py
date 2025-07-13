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
    <meta name="twitter:title" content="{basic.title}">
    <meta property="og:title" content="{basic.title}">

    <meta name="author" content="{basic.author}">

    <meta name="description" content="{basic.description}">
    <meta name="twitter:description" content="{basic.description}">
    <meta property="og:description" content="{basic.description}">

    <meta property="og:image" content="{social.image}">
    <meta name="twitter:image" content="{social.image}">

    <link rel="canonical" href="{canon.canonical}">
    <meta property="og:url" content="{canon.canonical}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@SamGReynoso">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{social.site_name}">
    <meta property="og:locale" content="en_US">

    <meta name="date" content="{basic.date}">
    <meta name="modified" content="{basic.modified}">
    """

