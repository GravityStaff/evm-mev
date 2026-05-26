import pytest
from evm_mev.utils import parse_swap_data

def test_parse_v2_swap():
    # swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] path, address to, uint256 deadline)
    # this is a truncated dummy hex for testing logic
    hex_data = "0x38ed17390000000000000000000000000000000000000000000000000de0b6b3a7640000" 
    
    res = parse_swap_data(hex_data)
    assert res['amountIn'] == 10**18

def test_empty_calldata():
    assert parse_swap_data("") is None
    assert parse_swap_data("0x") is None

def test_malformed_selector():
    # random 4 bytes that aren't a swap
    res = parse_swap_data("0xdeadbeef1234")
    assert res is None

def test_path_extraction():
    # TODO: need a real mainnet blob here to verify path decoding
    pass
