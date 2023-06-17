import asyncio
import queue

import threading
import time
from contextlib import asynccontextmanager
from typing import Callable
from urllib.parse import urlparse
from playwright.async_api import async_playwright


class PlaywrightBrowser:
    _browser = None
    _context = None

    @asynccontextmanager
    async def init_browser_context(self):
        """
        初始化全局浏览器上下文对象
        """
        if self._context:
            yield self._context
        async with async_playwright() as playwright:
            _browser = await playwright.chromium.launch(headless=False, slow_mo=50)
            self._context = await _browser.new_context()
            yield self._context

    async def goto(self, url: str) -> str:

        ctx = self.init_browser_context()
        context = await ctx.__aenter__()

        page = await context.new_page()
        await page.goto(url)
        source = await page.content()
        # await page.close()

        return source

    async def close(self):
        await self._context.close()


_browser_queue = queue.Queue()


async def browser_coroutine():
    browser = PlaywrightBrowser()
    while 1:
        if _browser_queue.empty():
            time.sleep(2)
            # _browser_queue.task_done()
            continue
        else:
            item = _browser_queue.get()

        if item == 'over':
            await browser.close()
        elif len(item) == 2:
            url, callback = item
            content = await browser.goto(url)
            callback(content)
        _browser_queue.task_done()


def run_coroutine_in_thread():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(browser_coroutine())


if 1:
    _browser_thread = threading.Thread(target=run_coroutine_in_thread)
    _browser_thread.start()


class PlaywrightOperate:

    @staticmethod
    def put_task(url: str, callback: Callable):
        _browser_queue.put((url, callback))

    @staticmethod
    def end():
        _browser_queue.put('over')

    @staticmethod
    def wait():
        _browser_queue.join()



