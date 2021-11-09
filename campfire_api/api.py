from requests import get, post, Session, Response
from typing import Union, Literal, Any
import warnings
from json import JSONDecodeError

from .errors import *
from .post_elements import Element


class CampfireAPI:
    """
    Campfire API wrapper based on @sit Campfire Web: https://github.com/timas130/campfire-web

    If you want to log in to your account, use LoginCampfireAPI.
    """
    _BASE_URL = 'https://camp.33rd.dev/api/'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Stores the parameters for requests."""
        self._args = args
        self._kwargs = kwargs

    def _get_response(self, endpoint: str) -> dict:
        """Accesses the API via the specified path and returns a response."""
        url = self._BASE_URL + endpoint
        resp = get(url, *self._args, **self._kwargs)

        return self._error_handler(resp)

    @staticmethod
    def _error_handler(resp: Response) -> dict:
        """Returns dictionary if request is successful, else raise ValueError."""
        server_errors = {
            'ERROR_UNAUTHORIZED': UnauthorizedError,
            'ERROR_ACCOUNT_IS_BANED': AccountIsBannedError,
            'E_ALREADY_EXIST': EAlreadyExist,
            'ERROR_GONE': GoneError,
            'E_BAD_PAGE_INDEX': EBadPageIndex
        }
        try:
            resp_json = resp.json()
        except JSONDecodeError:
            if resp.status_code == 404:
                raise NotFoundError()
            warnings.warn('Something wrong')
            return {'status_code': resp.status_code, 'content': resp.text}

        if resp.status_code != 200:
            if 'response' in resp_json:
                raise server_errors[resp_json['response']['code']](resp_json['response']['messageError'])
            else:
                print(resp_json)
                raise UnknownError()
        return resp_json

    def _get_img(self, endpoint: str) -> bytes:
        """Returns the image in bytes, else raise a ValueError."""
        url = self._BASE_URL + endpoint
        resp = get(url, *self._args, **self._kwargs)

        if resp.status_code != 200:
            raise NotFoundError('Image not available.')
        return resp.content

    def get_account_info(self, id_or_name: Union[int, str]) -> dict:
        """Returns information about the user by nickname or ID."""
        endpoint = 'account/{id}'.format(id=id_or_name)
        return self._get_response(endpoint)

    def get_account_posts(self, account_id: int, offset: int = 0) -> dict:
        """Returns the user's posts. Use the offset to get the earliest posts."""
        endpoint = 'account/{id}/publications?offset={offset}'.format(id=account_id, offset=offset)
        return self._get_response(endpoint)

    def get_activity_info(self, activity_id: int) -> dict:
        """Returns information about the relay."""
        endpoint = 'activity/{id}'.format(id=activity_id)
        return self._get_response(endpoint)

    def get_activity_posts(self, activity_id: int, offset: int = 0) -> dict:
        """Returns the relay posts. Use the offset to get the earliest posts."""
        endpoint = 'activity/{id}/posts?offset={offset}'.format(id=activity_id, offset=offset)
        return self._get_response(endpoint)

    def get_fandom_info(self, fandom_id: int) -> dict:
        """Returns information about the fandom."""
        endpoint = 'fandom/{id}'.format(id=fandom_id)
        return self._get_response(endpoint)

    def get_fandom_posts(self, fandom_id: int, offset: int = 0) -> dict:
        """Returns the fandom posts. Use the offset to get the earliest posts."""
        endpoint = 'fandom/{id}/posts?offset={offset}'.format(id=fandom_id, offset=offset)
        return self._get_response(endpoint)

    def get_popular_fandoms(self, randomize: bool = False, offset: int = 0) -> dict:
        """Returns a list of popular fandoms. Use randomize to shuffle it."""
        endpoint = 'fandom?card={randomize}&offset={offset}'.format(randomize=randomize, offset=offset)
        if not isinstance(randomize, bool):
            warnings.warn('The randomize parameter must be of the bool type')
        return self._get_response(endpoint)

    def get_image(self, img_id: int) -> bytes:
        """Returns the image by ID."""
        endpoint = 'image/{id}'.format(id=img_id)
        return self._get_img(endpoint)

    def search_posts(self, query: str) -> dict:
        """Searches for posts by the specified query"""
        endpoint = 'post/search?q={query}'.format(query=query)
        return self._get_response(endpoint)

    def get_post_content(self, post_id: int) -> dict:
        """Returns information and content about the post."""
        endpoint = 'post/{id}'.format(id=post_id)
        return self._get_response(endpoint)

    def get_comments(self, pub_id: int, offset: int = 0) -> dict:
        """Returns the publication comments."""
        endpoint = 'post/{id}/comments?offset={offset}'.format(id=pub_id, offset=offset)
        return self._get_response(endpoint)

    def get_donates_sum(self) -> float:
        """Returns the amount of donations for that month."""
        endpoint = 'project/donates'
        raw = self._get_response(endpoint)
        return raw['totalCount'] / 100

    def get_rubric_info(self, rubric_id: int) -> dict:
        """Returns information about the rubric."""
        endpoint = 'rubric/{id}?offset=0'.format(id=rubric_id)
        return self._get_response(endpoint)['rubric']

    def get_rubric_posts(self, rubric_id: int, offset: int = 0) -> dict:
        """Returns the rubric posts. Use the offset to get the earliest posts."""
        endpoint = 'rubric/{id}?offset={offset}'.format(id=rubric_id, offset=offset)
        return self._get_response(endpoint)['posts']

    def get_feed(self, offset: int = 0,
                 feed_type: Literal['subscribed', 'all', 'best', 'good', 'abyss', 'all_subs'] = 'subscribed') -> dict:
        """Returns sit's feed or yours if you are logged into the account."""
        endpoint = 'feed?offset={offset}&type={type}'.format(offset=offset, type=feed_type)
        return self._get_response(endpoint)

    def get_fandom_wiki(self, fandom_id: int, offset: int = 0) -> dict:
        """Returns a list from the root of the fandom wiki. Use the offset to get the earliest articles."""
        endpoint = 'fandom/{id}/wiki?offset={offset}'.format(id=fandom_id, offset=offset)
        return self._get_response(endpoint)

    def get_fandom_wiki_section(self, fandom_id: int, section_id: int, offset: int = 0) -> dict:
        """Returns a list from the section of the fandom wiki. Use the offset to get the earliest articles."""
        endpoint = 'fandom/{id}/wiki/{section_id}?offset={offset}'.format(id=fandom_id, section_id=section_id,
                                                                          offset=offset)
        return self._get_response(endpoint)

    def get_wiki_article(self, article_id: int) -> dict:
        """Returns information and content about the article."""
        endpoint = 'fandom/wiki/{id}'.format(id=article_id)
        return self._get_response(endpoint)

    def custom(self, **data):
        url = self._BASE_URL + 'custom'
        resp = post(url, json=data)
        return self._error_handler(resp)


class LoginCampfireAPI(CampfireAPI):
    """
    Campfire API wrapper based on @sit Campfire Web: https://github.com/timas130/campfire-web

    Use this class to log in to the account.
    """

    def __init__(self, email: str, password: str, *args: Any, **kwargs: Any) -> None:
        """Logging in to the account on init."""
        super().__init__(*args, **kwargs)
        self._session = Session()
        self.user = self.login(email, password)

    def login(self, email: str, password: str) -> dict:
        """Logging in to the account."""
        endpoint = 'auth/login'
        payload = {'email': email, 'password': password, 'redir': False}
        self.user = self._post_request(endpoint, **payload)
        return self.user

    def _get_response(self, endpoint: str) -> dict:
        """Accesses the API via the specified path and returns a response."""
        url = self._BASE_URL + endpoint
        resp = self._session.get(url, *self._args, **self._kwargs)
        return self._error_handler(resp)

    def _post_request(self, endpoint: str, **data: Any) -> dict:
        """Accesses the API via the specified path & data and returns a response."""
        url = self._BASE_URL + endpoint
        resp = self._session.post(url, *self._args, **self._kwargs, json=data)
        return self._error_handler(resp)

    def custom(self, **data):
        return self._post_request('custom', **data)

    def get_my_profile(self) -> dict:
        """Returns information about your account."""
        endpoint = 'user'
        return self._get_response(endpoint)

    def get_my_quest(self) -> dict:
        """Returns your daily quest."""
        endpoint = 'user/quest'
        return self._get_response(endpoint)

    def pub_comment(self, pub_id: int, content: str, reply_id: int = 0) -> dict:
        """Publishes a comment under the specified publication."""
        endpoint = 'pub/{id}/comment?redir=false'.format(id=pub_id)
        return self._post_request(endpoint, content=content, reply=reply_id)

    def send_karma(self, pub_id: int, is_positive: bool) -> dict:
        """Sends karma to the specified publication."""
        endpoint = 'pub/{id}/karma?positive={is_positive}'.format(id=pub_id, is_positive=is_positive)
        return self._get_response(endpoint)

    def member_activity(self, activity_id: int, is_member: bool) -> dict:
        """Changes your participation status in the relay. Use reject_activity if it is your turn.
           \nTrue - You are participating
           \nFalse - Do not participate
        """
        endpoint = 'activity/{id}/member?member={is_member}'.format(id=activity_id, is_member=is_member)
        return self._get_response(endpoint)

    def reject_activity(self, activity_id: int) -> dict:
        """Reject the participation in the relay."""
        endpoint = 'activity/{id}/reject'.format(id=activity_id)
        return self._get_response(endpoint)

    def sub_fandom(self, fandom_id: int, sub_type: Literal['all', 'nothing', 'important'] = 'all',
                   notif_important: bool = True) -> dict:
        """
        Subscribes to fandom.
        Type - Type of subscription.

        important -
        \nTrue to notify about important posts,
        \nFalse to not notify about important posts.
        \nThe default is true, but only if type != 1.
        """
        sub_types = {
            'all': 0,
            'nothing': 1,
            'important': -1
        }
        try:
            sub_type = sub_types[str(sub_type).lower()]
        except KeyError:
            raise KeyError('Invalid subscription type.')
        endpoint = 'fandom/{id}/sub?type={type}&important={important}'.format(id=fandom_id, type=sub_type,
                                                                              important=notif_important)
        return self._get_response(endpoint)

    def get_my_drafts(self, offset: int = 0) -> dict:
        """Returns a list of drafts."""
        endpoint = 'drafts?offset={offset}'.format(offset=offset)
        return self._get_response(endpoint)

    def get_draft_content(self, draft_id: int) -> dict:
        """Returns the content of the draft."""
        endpoint = 'drafts/{id}'.format(id=draft_id)
        return self._get_response(endpoint)

    def create_draft(self, fandom_id: int, lang_id: int = 2, *elements: Element) -> dict:
        """Creates a draft with the specified elements."""
        endpoint = 'drafts/0/page?action=put'
        data = {
            "fandomId": int(fandom_id),
            "languageId": int(lang_id),
            "pages": list(map(dict, elements))
        }
        for item in elements:
            if item.has_image:
                data.update(item.images)
        return self._post_request(endpoint, **data)

    def add_draft_elements(self, draft_id: int, *elements: Element) -> dict:
        """Adds an elements to the draft."""
        endpoint = 'drafts/{id}/page?action=put'.format(id=draft_id)
        draft = self.get_draft_content(draft_id)
        data = {
            "fandomId": int(draft['fandomId']),
            "languageId": int(draft['languageId']),
            "pages": list(map(dict, elements))
        }
        for item in elements:
            if item.has_image:
                data.update(item.images)
        return self._post_request(endpoint, **data)

    def move_draft_element(self, draft_id: int, element_index: int, target_index: int) -> dict:
        """Moves the specified element in the draft."""
        endpoint = 'drafts/{id}/page?action=move'.format(id=draft_id)
        data = {"pageIndex": int(element_index), "targetIndex": int(target_index)}
        return self._post_request(endpoint, **data)

    def change_draft_element(self, draft_id: int, element_index: int, element: Element) -> dict:
        """Changes the specified element in the draft."""
        endpoint = 'drafts/{id}/page?action=change'.format(id=draft_id)
        data = {"pageIndex": int(element_index), "page": dict(element)}
        if element.has_image:
            data.update(element.images)
        return self._post_request(endpoint, **data)

    def remove_draft_elements(self, draft_id: int, *element_indexes: int) -> dict:
        """Removes the specified element in the draft."""
        endpoint = 'drafts/{id}/page?action=remove'.format(id=draft_id)
        data = {"pageIndexes": list(map(int, element_indexes))}
        return self._post_request(endpoint, **data)

    def pub_post(self, draft_id: int) -> dict:
        """Publishes a post in the fandom."""
        endpoint = 'drafts/{id}/publish'.format(id=draft_id)
        return self._get_response(endpoint)
