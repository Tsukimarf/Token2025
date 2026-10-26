#!/usr/bin/env python3
"""Record REAL deployed addresses into bld_database.json after on-chain deploy.
usage: python3 set_contract_address.py bld_spl_token <BASE58_ADDRESS> [--program <PROGRAM_ID>]
Refuses anything that is not a valid base58 Solana address. Never invents addresses."""
import json, re, sys
B58 = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
PATH = "bld_database.json"

def main(argv):
    if len(argv) < 3: sys.exit(__doc__)
    key, addr = argv[1], argv[2]
    prog = argv[argv.index("--program")+1] if "--program" in argv else None
    d = json.load(open(PATH, encoding="utf-8"))
    c = d["contract_addresses"].get(key)
    if c is None or key.startswith("_"): sys.exit(f"unknown contract key: {key}")
    for v in (addr, prog):
        if v and not B58.fullmatch(v): sys.exit(f"invalid base58 address: {v}")
    c.update(address=addr, status="deployed", explorer=f"https://solscan.io/account/{addr}")
    if prog: c["program"] = prog
    json.dump(d, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"✓ {key} → {addr}")

if __name__ == "__main__": main(sys.argv)
