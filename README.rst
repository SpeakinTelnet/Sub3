====
Sub3
====

A Python aiohttp wrapper client to subscribe to the Ethereum JSON-RPC PubSub endpoints.


Installation
------------

.. readme-install-start

Sub3 can be installed using ``pip`` as follows:

.. code-block:: console

   $ pip install sub3

.. readme-install-end

Usage
-----

Refer to the `full documentation <https://Sub3.readthedocs.io>`_
for the in-depth usage.

.. readme-usage-start

Prerequisite
************

- The URL to a node that has a WebSocket port opened. This can be either from a 
  provider like `infura <https://infura.io>`_ or through a self-hosted Geth/Nethermind node.

Create a basic subscription
***************************

The basic subscription will just print the data as received. It can be tested
by doing the following:

.. code-block:: python

        >>> from sub3 import RPCMaker, Sub3
        
        #RPCMaker is for easy formatting of JSON-RPC calls
        >>> rpc = RPCMaker.new_heads()

        >>> sub = Sub3("ws://localhost:8546", rpc)
        >>> sub.start()
        #Connection to the node
        connected
        
        #Successful answer from the JSONRPC request 
        {"jsonrpc":"2.0","id":"1","result":"0x1aaa6ce63bae0597ceadd723fd05e6db"}
        
        #Starts receiving data
        {
         "jsonrpc":"2.0",
         "method":"eth_subscription",
         "params":{"subscription":"0x1aaa6ce63bae0597ceadd723fd05e6db",
         "result":{"parentHash":"0x65906581" [...]}
         }


Sub-classing
************

The data processing can easily be customized by sub-classing the ``Sub3`` class
like so:

.. code-block:: python

        from sub3 import Sub3

        class NewClient(Sub3):

            async def on_data(self, data):
                # add your own data processing logic

            async def on_closed(self, error):
                # add your processing of `closed` message

            async def on_error(self, error):
                # add your processing of `error` message

        rpc = RPCMaker.new_heads()

        sub = NewClient("ws://localhost:8546", rpc)

        sub.start()

.. Note:: 
  Take note that the functions are Async. if you don't define them as such the client
  will raise an error.


.. readme-usage-end

Donate 
------

.. readme-donate-start

I made this has a fun side project and it's free for anyone to use.
If you like it and wish to donate here's a few of my crypto wallets. 

.. _tbl-grid:

+----------------------------------------+--------------------------------------+-----------------------------------------+
| Ethereum and L2s (0x29006...)          | Monero (85tBS7YSrM5...)              | Peercoin (PBzj1ZwMDW...)                |
|                                        |                                      |                                         |
+========================================+======================================+=========================================+
| |EthereumQR|                           | |MoneroQR|                           | |PeercoinQR|                            |
+----------------------------------------+--------------------------------------+-----------------------------------------+

.. |EthereumQR| image:: https://raw.githubusercontent.com/SpeakinTelnet/Sub3/master/docs/_qrcodes/ethereum.png
  :width: 300
  :alt: EthereumQR

.. |MoneroQR| image:: https://raw.githubusercontent.com/SpeakinTelnet/Sub3/master/docs/_qrcodes/monero.png
  :width: 300
  :alt: MoneroQR

.. |PeercoinQR| image:: https://raw.githubusercontent.com/SpeakinTelnet/Sub3/master/docs/_qrcodes/peercoin.png
  :width: 300
  :alt: PeerCoinQR

.. readme-donate-end

* Free software: MIT
* Documentation: https://Sub3.readthedocs.io.

⊂(▀¯▀⊂)
