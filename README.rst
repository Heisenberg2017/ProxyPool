ProxyPool
=========

基于Python asyncio 实现的异步高性能代理池


Features
--------

================================  ==============================
Proxy pool server                   Yes
Proxy IP checking                   No
Python type checking                WIP
Asynchronous HTTP request           WIP
Benchmarks                          No
Asynchronous Server support         No
Tested CPython versions             3.7
================================  ==============================


Documentation
-------------

...

Usage examples
--------------

安装依赖:

.. code:: shell

    pip3 install -r requirements.txt

打开代理池和API:

.. code:: shell

    python3 run.py

获取代理:

.. code:: python

    import requests

    PROXY_POOL_URL = 'http://localhost:5555/random'

    def get_proxy():
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None


Requirements
------------

* Python 3.7.3+

.. note::

    ...

Benchmarks
----------

...


License
-------

The ProxyPool is offered under MIT license.
