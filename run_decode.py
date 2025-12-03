#!/usr/bin/env python3
import sys
from ciphey.iface import Config
from ciphey.basemods.Decoders.railfence import Railfence
from ciphey.basemods.Decoders.route import Route


def decode_railfence(ctext: str, rails: int = 3):
    cfg = Config().library_default().complete_config()
    cfg.update_param("railfence", "rails", rails)
    dec = Railfence(cfg)
    return dec.decode(ctext)


def decode_route(ctext: str, columns: int = 4):
    cfg = Config().library_default().complete_config()
    cfg.update_param("route", "columns", columns)
    dec = Route(cfg)
    return dec.decode(ctext)


def main(argv):
    if len(argv) < 3:
        print("Usage: python run_decode.py <rail|route> <ciphertext> [param]")
        return 2

    method = argv[1].lower()
    ctext = argv[2]
    param = int(argv[3]) if len(argv) > 3 else None

    if method == "rail":
        rails = param if param is not None else 3
        print(decode_railfence(ctext, rails))
        return 0
    elif method == "route":
        cols = param if param is not None else 4
        print(decode_route(ctext, cols))
        return 0
    else:
        print("Unknown method; use 'rail' or 'route'")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
