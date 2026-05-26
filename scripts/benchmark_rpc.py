import time
import asyncio
import httpx
from evm_mev.config import RPC_URLS

async def check_latency(name, url):
    # measuring both ping and a basic state read
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            # use gasPrice because some cheap RPCs throttle blockNumber calls differently
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_gasPrice",
                "params": [],
                "id": 1
            }
            resp = await client.post(url, json=payload, timeout=7.0)
            
            if resp.status_code == 200:
                delta = (time.perf_counter() - start) * 1000
                return name, delta
            
            if resp.status_code == 429:
                return name, "ratelimited"
                
    except Exception:
        return name, "failed"
    return name, "error"

async def main():
    if not RPC_URLS:
        print("no urls in config.py, check your .env")
        return

    print(f"starting bench on {len(RPC_URLS)} endpoints...")
    tasks = [check_latency(n, u) for n, u in RPC_URLS.items()]
    results = await asyncio.gather(*tasks)
    
    # sort by speed
    valid = [r for r in results if isinstance(r[1], float)]
    errors = [r for r in results if not isinstance(r[1], float)]
    
    for name, lat in sorted(valid, key=lambda x: x[1]):
        print(f"[+] {name:<15} | {lat:>8.2f}ms")
        
    for name, err in errors:
        print(f"[!] {name:<15} | {err}")

if __name__ == "__main__":
    asyncio.run(main())
