from eth_utils import to_checksum_address

def to_eth(wei_val):
    return wei_val / 10**18

def clean_hex(h):
    if isinstance(h, str) and h.startswith('0x'):
        return h.lower()
    return h

def checksum(addr):
    if not addr:
        return addr
    return to_checksum_address(addr)
