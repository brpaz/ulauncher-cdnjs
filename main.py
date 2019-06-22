"""
Ulauncher CDNjs Extension
Search packages in cdnjs website directly from Ulauncher
"""

import logging
import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

LOGGER = logging.getLogger(__name__)

CDN_URL = "https://api.cdnjs.com/libraries/"


class CdnjsExtension(Extension):
    """ Main Class """

    def __init__(self):
        LOGGER.info('init cdnjs Extension')
        super(CdnjsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """
    Query Event listener
    """

    def on_event(self, event, extension):
        """ Handles Keyword Event """
        items = []

        try:

            query = event.get_argument() or ""

            if len(query) < 3:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name="Keep Typing to search on cdn.js ...",
                        on_enter=HideWindowAction(),
                        highlightable=False,
                    )
                ])

            max_results = int(extension.preferences['max_results'])
            payload = {'search': query,
                       'fields': 'version,description,repository'.encode('utf-8')}

            headers = {'Content-Type': 'application/json',
                       'User-Agent': 'Ulauncher-cdnjs/2.0'}

            req = requests.get(CDN_URL, params=payload, headers=headers)
            req.raise_for_status()

            libraries = req.json()

            for library in libraries['results'][0:max_results]:
                repo_url = library['repository']['url'].replace(
                    'git://', 'https://').replace('git+', '')
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=library['name'] + " (" + library['version'] + ")",
                    description=library['description'],
                    on_enter=CopyToClipboardAction(library['latest']),
                    on_alt_enter=OpenUrlAction(repo_url)
                ))

            return RenderResultListAction(items)

        except requests.exceptions.HTTPError as err:
            LOGGER.error(err)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name="Error requesting CDNjs",
                description="Request error: " + str(req.status_code),
                on_enter=HideWindowAction(),
                highlightable=False,
            ))

            return RenderResultListAction(items)


if __name__ == '__main__':
    CdnjsExtension().run()
