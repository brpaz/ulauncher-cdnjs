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

logger = logging.getLogger(__name__)

CDN_URL = "https://api.cdnjs.com/libraries/"

class CdnjsExtension(Extension):

    def __init__(self):
        logger.info('init cdnjs Extension')
        super(CdnjsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
      
        try:

            maxResults = int(extension.preferences['max_results'])
            payload = {'search': event.get_argument(
            ), 'fields': 'version,description,repository'.encode('utf-8')}

            headers = {'Content-Type': 'application/json',
                    'User-Agent': 'Ulauncher-cdnjs/1.0'}

            r = requests.get(CDN_URL, params=payload, headers=headers)
            r.raise_for_status()

            libraries = r.json()

            for library in libraries['results'][0:maxResults]:
                repoUrl = library['repository']['url'].replace(
                    'git://', 'https://').replace('git+', '')
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=library['name'] + " (" + library['version'] + ")",
                    description=library['description'],
                    on_enter=CopyToClipboardAction(library['latest']),
                    on_alt_enter=OpenUrlAction(repoUrl)
            ))

        except requests.exceptions.RequestException as err:
            logger.error(err.message)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name="Request error: " + r.status_code,
                description=err.message,
                on_enter=HideWindowAction
            ))
        finally:
            return RenderResultListAction(items)

if __name__ == '__main__':
   CdnjsExtension().run()
