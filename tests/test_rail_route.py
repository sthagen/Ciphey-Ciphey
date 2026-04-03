from ciphey.iface import Config
from ciphey.basemods.Decoders.railfence import Railfence
from ciphey.basemods.Decoders.route import Route


def test_railfence_classic():
    # Classic example: rails=3
    cfg = Config().library_default().complete_config()
    dec = Railfence(cfg)
    ciphertext = "WECRLTEERDSOEEFEAOCAIVDEN"
    plaintext = "WEAREDISCOVEREDFLEEATONCE"
    assert dec.decode(ciphertext) == plaintext


def test_route_simple():
    cfg = Config().library_default().complete_config()
    dec = Route(cfg)
    # plaintext HELLOWORLD with columns=4 -> ciphertext HOLEWDLOLR
    ciphertext = "HOLEWDLOLR"
    plaintext = "HELLOWORLD"
    assert dec.decode(ciphertext) == plaintext
