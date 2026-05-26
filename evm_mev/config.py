import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Global settings for the bot"""
    RPC_URL = os.getenv("RPC_URL")
    WSS_URL = os.getenv("WSS_URL")
    PK = os.getenv("PRIVATE_KEY")

    # network stuff
    CHAIN_ID = int(os.getenv("CHAIN_ID", "1"))
    GAS_LIMIT = 500000
    MAX_PRIORITY_FEE = 2 * 10**9 # 2 gwei

    # Uniswap V2 Router on most chains
    UNISWAP_V2_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    
    # used for checking liquidity pools
    FACTORY_V2 = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"

    # TODO: add v3 addresses later if I ever get to it
    # v3_factory = "0x1F98431c8aD98523631AE4a59f267346ea31F984"

# old_config_style = True

cfg = Config()
