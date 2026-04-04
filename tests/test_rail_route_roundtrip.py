from ciphey.iface import Config
from ciphey.basemods.Decoders.railfence import Railfence
from ciphey.basemods.Decoders.route import Route


def railfence_encode(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(''.join(row) for row in fence)


def route_encode(text, cols):
    # fill rows left-to-right then read columns top-to-bottom
    rows = (len(text) + cols - 1) // cols
    grid = [[''] * cols for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    return ''.join(grid[r][c] for c in range(cols) for r in range(rows) if grid[r][c])


def test_railfence_roundtrip():
    cfg = Config().library_default().complete_config()
    dec = Railfence(cfg)
    inputs = [
        "HELLOWORLD",
        "THEQUICKBROWNFOX",
        "ENCRYPTIONTEST",
        "RAILFENCECIPHER",
        "PYTHONISFUN",
    ]
    for pt in inputs:
        ct = railfence_encode(pt, 3)
        # no explicit key -> brute-force should find best
        assert dec.decode(ct) == pt


def test_route_roundtrip():
    cfg = Config().library_default().complete_config()
    dec = Route(cfg)
    inputs = [
        "HELLOWORLD",
        "THEQUICKBROWNFOX",
        "ENCRYPTIONTEST",
        "RAILFENCECIPHER",
        "PYTHONISFUN",
    ]
    for pt in inputs:
        ct = route_encode(pt, 4)
        assert dec.decode(ct) == pt
