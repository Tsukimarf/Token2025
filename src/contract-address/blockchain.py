"""
src/blockchain.py

Real on-chain data for the BLD contract address, queried live from a Solana
RPC endpoint (getSignaturesForAddress / getTokenSupply). This module never
invents transactions: until BLD_CONTRACT_ADDRESS is set (and has actually
been deployed on-chain), it returns status="pre_launch" with an empty list,
exactly like src/price.py does for price data.

Config (env vars, see .env.example):
    BLD_CONTRACT_ADDRESS   Same var used by price.py -- the deployed SPL mint.
    SOLANA_RPC_URL         Defaults to the public mainnet-beta RPC. For
                            production use, point this at a dedicated RPC
                            provider (Helius, QuickNode, Triton, etc.) --
                            the public endpoint is rate-limited and not
                            meant for sustained traffic.

Install dependencies:
    pip install requests
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Optional

import requests

DEFAULT_RPC_URL = "https://api.mainnet-beta.solana.com"


def _rpc_url() -> str:
    return os.getenv("SOLANA_RPC_URL", DEFAULT_RPC_URL)


def _contract_address() -> Optional[str]:
    addr = os.getenv("BLD_CONTRACT_ADDRESS", "").strip()
    return addr or None


def _now_iso() -> datetime:
    return datetime.now(timezone.utc)


def _rpc_call(method: str, params: list) -> dict:
    resp = requests.post(
        _rpc_url(),
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=10,
    )
    resp.raise_for_status()
    body = resp.json()
    if "error" in body:
        raise RuntimeError(body["error"].get("message", str(body["error"])))
    return body["result"]


def get_recent_transactions(limit: int = 20, before: Optional[str] = None) -> dict:
    """Recent transaction signatures touching the BLD contract address,
    straight from getSignaturesForAddress. No transaction is shown unless
    the RPC node actually returned it."""
    address = _contract_address()
    if not address:
        return {
            "status": "pre_launch",
            "address": None,
            "transactions": [],
            "fetched_at": _now_iso(),
            "message": (
                "BLD has no contract address yet (pre-mainnet, see roadmap). "
                "Set BLD_CONTRACT_ADDRESS once the token is deployed to pull real transactions."
            ),
        }

    limit = max(1, min(limit, 100))
    params = [address, {"limit": limit}]
    if before:
        params[1]["before"] = before

    try:
        sigs = _rpc_call("getSignaturesForAddress", params)
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "unavailable",
            "address": address,
            "transactions": [],
            "fetched_at": _now_iso(),
            "message": f"RPC error: {exc}",
        }

    transactions = [
        {
            "signature": s.get("signature"),
            "slot": s.get("slot"),
            "block_time": s.get("blockTime"),
            "status": "failed" if s.get("err") else "success",
            "confirmation_status": s.get("confirmationStatus"),
            "memo": s.get("memo"),
        }
        for s in sigs
    ]

    return {
        "status": "live",
        "address": address,
        "transactions": transactions,
        "fetched_at": _now_iso(),
        "message": None if transactions else "Address has no on-chain transactions yet.",
    }


def get_token_supply() -> dict:
    """Actual on-chain circulating supply for the mint, straight from
    getTokenSupply -- a sanity check against the figures quoted in
    BLD_database.json, not a replacement for them."""
    address = _contract_address()
    if not address:
        return {
            "status": "pre_launch",
            "address": None,
            "amount": None,
            "decimals": None,
            "ui_amount": None,
            "fetched_at": _now_iso(),
            "message": "No contract address set yet.",
        }

    try:
        result = _rpc_call("getTokenSupply", [address])
        value = result.get("value", {})
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "unavailable",
            "address": address,
            "amount": None,
            "decimals": None,
            "ui_amount": None,
            "fetched_at": _now_iso(),
            "message": f"RPC error: {exc}",
        }

    return {
        "status": "live",
        "address": address,
        "amount": value.get("amount"),
        "decimals": value.get("decimals"),
        "ui_amount": value.get("uiAmount"),
        "fetched_at": _now_iso(),
        "message": None,
    }
