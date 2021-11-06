from typing import Literal, Union


class Element:
    """A base class for all post elements."""

    def __init__(self):
        self._data = dict()

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, *args):
        return self._data.__getitem__(*args)

    def keys(self):
        return self._data.keys()


class Text(Element):
    """Text element."""
    _ALIGN_TYPES = {
        'left': 0,
        'center': 2,
        'right': 1
    }
    _IS_TITLE_CONVERTER = {
        False: 0,
        True: 1
    }

    def __init__(self, content: str, align: Literal['left', 'center', 'right'] = 'left', icon_id: int = 0,
                 is_title: bool = False):
        super().__init__()
        align = self._ALIGN_TYPES[str(align).lower()]
        is_title = self._IS_TITLE_CONVERTER[is_title]
        self._data = {
            "J_PAGE_TYPE": 1,
            "J_TEXT": str(content),
            "J_SIZE": is_title,
            "align": align,
            "icon": int(icon_id)
        }


class Image(Element):
    """
    Element image.
    \nMust be sent with add_draft_image(...)
    """

    def __init__(self):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 2
        }


class ImagesList(Element):
    """
    Element list of images.
    \nNot ready for use.
    """

    def __init__(self):
        super().__init__()
        images_ids = list()
        self._data = {
            "J_PAGE_TYPE": 3,
            "imagesIds": [
                int(),
                int()
            ],
            "imagesCount": len(images_ids),
            "replacePageIndex": -1,
            "imagesMiniSizesW": [
                int(),
                int()
            ],
            "imagesMiniSizesH": [
                int(),
                int()
            ],
            "title": "",
            "removePageIndex": -1,
            "imagesMiniIds": [
                int(),
                int()
            ]
        }
        raise NotImplementedError('This element is not ready, do not use it.')


class Video(Element):
    """
    The element video.
    \nMust be sent with add_draft_image(...)
    """

    def __init__(self, link: str):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 9,
            "videoId": str(link)
        }


class Quote(Element):
    """The quote element."""

    def __init__(self, text: str, author: str = str()):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 5,
            "author": str(author),
            "text": str(text)
        }


class Link(Element):
    """The link element."""

    def __init__(self, name: str, link: str):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 4,
            "name": str(name),
            "link": str(link)
        }


class Spoiler(Element):
    """The spoiler element."""

    def __init__(self, name: str, count: int):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 6,
            "count": int(count),
            "name": str(name)
        }


class Survey(Element):
    """The survey element."""

    def __init__(self, title: str, min_lvl: float = 0, min_karma: float = 0, *polls: str):
        super().__init__()
        min_lvl = float(min_lvl) * 100
        min_karma = float(min_karma) * 100
        self._data = {
            "minLevel": int(min_lvl),
            "J_PAGE_TYPE": 7,
            "pollingId": 0,
            "options": list(map(str, polls)),
            "title": str(title),
            "minKarma": int(min_karma)
        }


class LinkImage(Element):
    """
    The link-picture element.
    \nMust be sent with add_draft_image(...)
    """

    def __init__(self, link: str):
        super().__init__()
        self._data = {
            "J_PAGE_TYPE": 14,
            "link": str(link)
        }


class CampfireElement(Element):
    """Link to the Campfire element."""

    def __init__(self, element_type: str, element_id: int, optional_id: Union[int, None] = None):
        super().__init__()
        if isinstance(optional_id, int):
            optional_id = '_{id}'.format(id=optional_id)
        else:
            optional_id = ''
        self._data = {
            "J_PAGE_TYPE": 12,
            "link": "http://sayzen.ru/r/r.php?a={type}-{id}{optional}".format(type=element_type, id=element_id,
                                                                              optional=optional_id)
        }


class Table(Element):
    """
    Element table.
    \nNot ready for use.
    """

    def __init__(self):
        super().__init__()
        raise NotImplementedError('This element is not ready, do not use it.')
