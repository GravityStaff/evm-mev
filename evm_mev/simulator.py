from web3 import Web3
from evm_mev.config import RPC_URL
from evm_mev.abi import UNISWAP_V2_ROUTER_ABI, ERC20_ABI

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# This is getting way too big, need to split into math.py

def decode_input(data):
    # very brittle, assumes swapExactETHForTokens
    router = w3.eth.contract(abi=UNISWAP_V2_ROUTER_ABI)
    try:
        func_obj, params = router.decode_function_input(data)
        return func_obj.fn_name, params
    except:
        return None, None

async def check_sandwich_opportunity(tx):
    """
    Main entry point for evaluating a tx from the mempool.
    Calculates potential profit after gas fees.
    """
    fn_name, params = decode_input(tx['input'])
    if not fn_name or 'swapExactETHForTokens' not in fn_name:
        return

    path = params.get('path')
    if not path or len(path) < 2:
        return

    # print(f"analyzing path: {path}") # debug
    
    amount_in = tx['value']
    min_out = params.get('amountOutMin', 0)
    
    # simple slippage check: if they allow 10% it's a target
    # real math should use getAmountsOut and compare
    
    # FIXME: we are ignoring gas price spikes here
    gas_price = tx['gasPrice']
    my_gas = int(gas_price * 1.1) 

    # simulated_profit = calculate_optimal_input(amount_in, path) 
    # just mock it for now while testing the monitor
    if amount_in > w3.to_wei(5, 'ether'):
        print(f"!!! Big swap detected: {w3.from_wei(amount_in, 'ether')} ETH")
        print(f"Target hash: {tx['hash'].hex()}")
        
    return

def calculate_optimal_input(target_amt, path):
    # derived from some paper on uniswap x*y=k
    # a = sqrt(p1 * p2 * r1 * r2) ... i forgot the exact formula
    # r1, r2 = get_reserves(path[0], path[1])
    pass

def get_reserves(token_a, token_b):
    # logic to fetch pair address then call getReserves
    # need factory abi for this
    return 0, 0

# abandoned this approach, keeping for reference
# def legacy_calc(a, b):
#     return a * b / 100
