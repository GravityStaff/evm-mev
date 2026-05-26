import asyncio
import json
import websockets
from web3 import Web3
from evm_mev.config import WSS_URL, RPC_URL
from evm_mev.simulator import check_sandwich_opportunity

w3 = Web3(Web3.HTTPProvider(RPC_URL))

async def handle_tx(tx_hash):
    try:
        # web3.py is slow here, maybe raw jsonrpc later?
        tx = w3.eth.get_transaction(tx_hash)
        if not tx or not tx['to']:
            return
        
        # we only care about router calls
        # TODO: add more routers to config
        if tx['to'].lower() == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d":
            await check_sandwich_opportunity(tx)
    except Exception as e:
        # mostly 'not found' for fast blocks
        pass

async def watch_mempool():
    async with websockets.connect(WSS_URL) as ws:
        sub = {"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}
        await ws.send(json.dumps(sub))
        
        print("monitoring started...")
        while True:
            try:
                msg = await ws.recv()
                res = json.loads(msg)
                tx_hash = res['params']['result']
                asyncio.create_task(handle_tx(tx_hash))
            except Exception as e:
                print(f"loop error: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(watch_mempool())
