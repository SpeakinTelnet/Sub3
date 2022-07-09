from sub3 import RPCMaker


def test_new_heads():
    assert RPCMaker.new_heads() == {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "eth_subscribe",
        "params": ["newHeads"],
    }


def test_logs():
    rpc = RPCMaker.logs(
        address="0x8320fe7702b96808f7bbc0d4a888ed1468216cfd",
        topics=["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"],
    )
    assert rpc == {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "eth_subscribe",
        "params": [
            "logs",
            {
                "address": "0x8320fe7702b96808f7bbc0d4a888ed1468216cfd",
                "topics": [
                    "0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"  # noqa: E501
                ],
            },
        ],
    }


def test_pending_transactions():
    assert RPCMaker.new_pending_transaction() == {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "eth_subscribe",
        "params": ["newPendingTransactions"],
    }


def test_syncing():
    assert RPCMaker.syncing() == {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "eth_subscribe",
        "params": ["syncing"],
    }


def test_unsubscribe():
    rpc = RPCMaker.unsubscribe("0x57c86f70cf91507bdb29953e121cb174")
    assert rpc == {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_unsubscribe",
        "params": ["0x57c86f70cf91507bdb29953e121cb174"],
    }
