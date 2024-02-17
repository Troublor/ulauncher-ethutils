from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
import subprocess
import os
from pathlib import Path

DIR = Path(os.path.dirname(os.path.realpath(__file__)))


class EthUtilsExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event: KeywordQueryEvent, extension: EthUtilsExtension):
        addr = event.get_argument()
        if not addr:
            return DoNothingAction()
        addr = addr.strip()
        if len(addr) == 0:
            return DoNothingAction()

        checksum = to_checksum(addr)
        plain = to_plain(addr)

        checksum_item = ExtensionResultItem(
            icon='images/checksum_address.png',
            name=checksum,
            description='Checksum address',
            on_enter=CopyToClipboardAction(checksum),
            on_alt_enter=CopyToClipboardAction(checksum),
        )
        plain_item = ExtensionResultItem(
            icon='images/plain_address.png',
            name=plain,
            description='Plain address',
            on_enter=CopyToClipboardAction(plain),
            on_alt_enter=CopyToClipboardAction(plain),
        )

        if addr == checksum:
            items = [plain_item, checksum_item]
        else:
            items = [checksum_item, plain_item]

        return RenderResultListAction(items)


def to_checksum(address: str) -> str:
    # call the external executable
    try:
        output = subprocess.check_output(
            [
                str(DIR / 'bin' / 'ethutils'),
                'address',
                '--convert', 'checksum',
                '--tolerate',
                address,
            ],
            stderr=subprocess.STDOUT
        )
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8').strip()


def to_plain(address: str) -> str:
    # call the external executable
    try:
        output = subprocess.check_output(
            [
                str(DIR / 'bin' / 'ethutils'),
                'address',
                '--convert', 'plain',
                '--tolerate',
                address,
            ],
            stderr=subprocess.STDOUT
        )
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8').strip()


if __name__ == '__main__':
    EthUtilsExtension().run()
