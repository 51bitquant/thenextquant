# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="thenextquant",
    version="0.0.6",
    packages=["quant",
              "quant.utils",
              "quant.platform",
              ],
    description="Quant Trader Framework",
    url="https://github.com/51bitquant/thenextquant",
    author="huangtao, 51bitquant",
    author_email="stephen0823@aliyun.com",
    license="MIT",
    keywords=["thenextquant", "quant", "aioquant", "51bitquant"],
    install_requires=[
        "aiohttp== 3.8.4",
        "aioamqp==0.10.0",
    ],
)
