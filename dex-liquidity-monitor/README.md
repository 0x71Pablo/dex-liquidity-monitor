# Multi-DEX Liquidity & Price Monitoring Engine

An enterprise-grade, asynchronous Python execution layer engine built to continuously monitor real-time liquidity distributions and mathematical spot price deviations across Decentralized Exchanges (DEXs).

## Core Technical Features
- **Asynchronous Architecture:** Leverages `asyncio` coupled with `WebSocketsProvider` to process network states concurrently without blocking core processing threads.
- **Dynamic State Evaluation:** Directly interrogates EVM on-chain smart contract data matrices using optimized JSON-ABIs to retrieve true operational reserve balances.
- **Failover Resiliency:** Contains built-in network connection diagnostics and automated loop recovery logic.

## Installation & Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
