# evm-mev

Personal playground for messing with MEV. I got tired of manually checking ethscan for pending txs while debugging some arb logic, so I built this. It connects to a node via websockets, filters the mempool, and tries to guess if a swap is worth sandwiching.

It's not a production bot. Don't expect to make money with it as is.

## setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## usage

Create a `.env` with your node URL:
```
RPC_WS_URL=wss://eth-mainnet.g.alchemy.com/v2/your-key
```

Run the observer:
```bash
python -m evm_mev.monitor
```

I added a simulator script too, but it's pretty raw. It uses eth_call to check potential profit without landing anything on chain.

## license
MIT
 