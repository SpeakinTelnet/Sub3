from functools import wraps
from typing import Dict


def _build_rpc(func):
    @wraps(func)
    def wrapper(**kwargs):
        params = func(**kwargs)
        if not kwargs:
            params.remove({})
        return dict(jsonrpc="2.0", id="1", method="eth_subscribe", params=params)

    return wrapper


class RPCMaker:

    @_build_rpc
    def new_pending_transaction(**kwargs) -> list[str, Dict]:
        """JSON-RPC for the pending transaction as they are added in the mempool
            
            :param kwargs: This RPC Don't usually take additional args
        """
        return ["newPendingTransactions", kwargs]

    @_build_rpc
    def new_heads(**kwargs) -> list[str, Dict]:
        """JSON-RPC for the new blocks as they are mined
            
            :param kwargs: Nethermind has the possibility for ``{"includeTransactions":"true"}``,
                            Geth doesn't accept any args
        """
        return ["newHeads", kwargs]

    @_build_rpc
    def logs(**kwargs) -> list[str, Dict]:
        """JSON-RPC for the logs in the new imported blocks according to the filters
                        
            Possible kwargs:
                - address: either an address or an array of addresses. 
                  Only logs that are created from these addresses are returned (optional)
                
                - topics: only logs which match the specified topics (optional)

        .. code-block:: python


            >>> RPCMaker.logs(
                    address="0x8320fe7702b96808f7bbc0d4a888ed1468216cfd",
                    topics=["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"]
                    )

            {'jsonrpc': '2.0',
            'id': '1',
            'method': 'eth_subscribe',
            'params': ['logs',
             {'address': '0x8320fe7702b96808f7bbc0d4a888ed1468216cfd',
              'topics': ['0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902']}]}
        
        """
        return ["logs", kwargs]

    @_build_rpc
    def syncing(**kwargs) -> list[str, Dict]:
        """JSON-RPC for the syncing status of the connected node
            
            :param kwargs: This RPC Don't usually take additional args
        """
        return ["syncing", kwargs]

    @staticmethod
    def unsubscribe(confirmation_id) -> list[str, Dict]:
        """
        JSON-RPC for unsubscribing to an ongoing JSON-RPC call. The client
        should normally close the websocket properly but it is still available
        in case someone would have the need for it
            
        :param confirmation_id: This is the identification as written in the field ``result`` of the subscription confirmation.
            

        .. code-block:: python

                {"jsonrpc":"2.0","id":"1","result":"0x57c86f70cf91507bdb29953e121cb174"}
                
                >>> RPCMaker.unsubscribe("0x57c86f70cf91507bdb29953e121cb174")
            
                {'jsonrpc': '2.0',
                'id': 1,
                'method': 'eth_unsubscribe',
                'params': ['0x57c86f70cf91507bdb29953e121cb174']}
        """
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_unsubscribe",
            "params": [confirmation_id],
        }
