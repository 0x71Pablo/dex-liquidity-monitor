import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from web3 import Web3
from web3.providers import WebSocketsProvider

load_dotenv()
WSS_URL = os.getenv("RPC_WSS_URL")

if not WSS_URL:
    print("[ERROR] RPC_WSS_URL missing from environment configuration. Exiting.")
    sys.exit(1)

POOL_ABI = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')

TRACKED_POOLS = {
    "0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852": {"name": "Uniswap V2: USDT-WETH", "decimals0": 6, "decimals1": 18},
    "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc": {"name": "Uniswap V2: USDC-WETH", "decimals0": 6, "decimals1": 18}
}

class LiquidityMonitor:
    def __init__(self, wss_url: str, pools: dict):
        self.wss_url = wss_url
        self.pools = pools
        self.w3 = None

    async def connect_nodes(self):
        self.w3 = Web3(WebSocketsProvider(self.wss_url))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to the RPC network layer.")

    async def fetch_pool_metrics(self, pool_address: str, meta: dict):
        try:
            checksum_address = self.w3.to_checksum_address(pool_address)
            contract = self.w3.eth.contract(address=checksum_address, abi=POOL_ABI)
            reserves = contract.functions.getReserves().call()
            reserve0 = reserves[0] / (10 ** meta["decimals0"])
            reserve1 = reserves[1] / (10 ** meta["decimals1"])
            
            if reserve0 > 0:
                spot_price = reserve1 / reserve0
                print(f"[{meta['name']}] Spot Price: {spot_price:.6f}")
        except Exception as e:
            print(f"[ERROR] {pool_address}: {str(e)}")

    async def run_event_loop(self):
        await self.connect_nodes()
        while True:
            try:
                tasks = [self.fetch_pool_metrics(addr, data) for addr, data in self.pools.items()]
                await asyncio.gather(*tasks)
                await asyncio.sleep(12)
            except Exception as e:
                await asyncio.sleep(5)
                await self.connect_nodes()

if __name__ == "__main__":
    monitor = LiquidityMonitor(WSS_URL, TRACKED_POOLS)
    try:
        asyncio.run(monitor.run_event_loop())
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Engine terminated.")
      
