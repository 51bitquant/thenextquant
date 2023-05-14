# -*— coding:utf-8 -*-

"""
websocket接口封装

Author: HuangTao
Date:   2018/06/29
"""

import json
import aiohttp
import asyncio

from quant.utils import logger
from quant.config import config


class Websocket:
    """ websocket接口封装
    """

    def __init__(self, url: str, ping_interval: int = 20, ping_timeout: int = 20):
        """ 初始化
        @param url 建立websocket的地址
        @param ping_timeout 检查websocket连接时间间隔
        @param ping_interval 发送心跳时间间隔
        """
        self.ws = None  # websocket连接对象
        self.url = url
        self._ping_interval = ping_interval
        self._ping_timeout = ping_timeout

    def initialize(self):
        """ 初始化
        """
        # 建立websocket连接
        asyncio.get_event_loop().create_task(self._connect())

    async def _connect(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    logger.info("url:", self.url, caller=self)
                    self.ws = await session.ws_connect(self.url,
                                                       receive_timeout=self._ping_timeout,
                                                       heartbeat=self._ping_interval)
                    await self.connected_callback()
                    async for msg in self.ws:
                        try:
                            data = json.loads(msg.data)
                        except:
                            data = msg.data
                        finally:
                            await self.process(data)

                    await self.disconnected_callback()

                except Exception as error:
                    print(f"error: {error}")
                    pass
                    logger.error("connect to server error! url:", self.url, caller=self)
                finally:
                    if self.ws:
                        await self.ws.close()

    async def connected_callback(self):
        """ 连接建立成功的回调函数
        * NOTE: 子类继承实现
        """
        pass

    async def disconnected_callback(self):
        """ 连接建立成功的回调函数
        * NOTE: 子类继承实现
        """
        pass

    async def process(self, msg):
        """ 处理websocket上接收到的消息 text 类型
        * NOTE: 子类继承实现
        """
        raise NotImplementedError

    async def send(self, data) -> bool:
        """ Send message to Websocket server.

        Args:
            data: Message content, must be dict or string.

        Returns:
            If send successfully, return True, otherwise return False.
        """
        if not self.ws:
            logger.warn("Websocket connection not connected yet!", caller=self)
            return False
        if isinstance(data, dict):
            await self.ws.send_json(data)
        elif isinstance(data, str):
            await self.ws.send_str(data)
        else:
            logger.error("send message failed:", data, caller=self)
            return False
        logger.debug("send message:", data, caller=self)
        return True
