from typing import Dict, Optional

import logging
from typing import Callable, Optional, Dict, Tuple

from ciphey.iface import Config, Decoder, ParamSpec, T, U, registry
from ciphey.basemods.Checkers.ezcheck import EzCheck
from ciphey.basemods.Checkers.quadgrams import Quadgrams


@registry.register
class Railfence(Decoder[str]):
    def decode(self, ctext: T) -> Optional[U]:
        # If a rails parameter is provided, use it. Otherwise brute-force possible rails
        params = self._params()

        def decode_with(n: int) -> str:
            if n <= 1:
                return ctext

            # Determine rail pattern for each character position
            pattern = []
            rail = 0
            direction = 1
            for _ in range(len(ctext)):
                pattern.append(rail)
                rail += direction
                if rail == 0 or rail == n - 1:
                    direction *= -1

            # Count characters per rail
            counts = [0] * n
            for p in pattern:
                counts[p] += 1

            # Fill rails from ciphertext sequentially
            rails_list = []
            idx = 0
            for c in counts:
                rails_list.append(list(ctext[idx : idx + c]))
                idx += c

            # Reconstruct plaintext by reading according to pattern
            result_chars = []
            pointers = [0] * n
            for p in pattern:
                result_chars.append(rails_list[p][pointers[p]])
                pointers[p] += 1

            return "".join(result_chars)

        # If user supplied rails param, use it
        if "rails" in params and params["rails"] is not None:
            try:
                n = int(params["rails"])
                return decode_with(n)
            except Exception:
                pass

        # Brute-force: try rails from 2..max_rails and score with Quadgrams
        cfg = self._config()
        quad = cfg(Quadgrams)
        max_rails = int(self._params().get("max_rails", 20))
        max_rails = min(max_rails, max(2, len(ctext) - 1))

        candidates: Dict[int, Tuple[str, float]] = {}
        # scoring weights
        quad_w = float(self._params().get("quad_weight", 1.0))
        letter_w = float(self._params().get("letter_weight", 0.5))
        word_w = float(self._params().get("word_weight", 0.3))

        common_words = ["THE", "AND", "IS", "IN", "OF", "TO", "YOU", "HELLO"]

        for n in range(2, max_rails + 1):
            pt = decode_with(n)
            try:
                # quadgram score (higher is better)
                txt = pt
                qdict = quad.QUADGRAMS_DICT
                quad_sum = sum(qdict.values())
                quad_score = 0.0
                from math import log10

                floor = log10(0.01 / quad_sum)
                s = ''.join([c for c in txt.upper() if c.isalpha()])
                for i in range(max(0, len(s) - 4 + 1)):
                    gram = s[i : i + 4]
                    if gram in qdict:
                        quad_score += float(qdict[gram]) / quad_sum
                    else:
                        quad_score += floor
                if len(s) > 0:
                    quad_score = quad_score / len(s)

                # letter density
                letters = sum(1 for c in pt if c.isalpha())
                letter_density = letters / max(1, len(pt))

                # simple common-word hits (normalized)
                up = pt.upper()
                hits = sum(up.count(w) for w in common_words)
                word_score = hits / max(1, len(pt) / 4)

                combined = quad_w * quad_score + letter_w * letter_density + word_w * word_score
                candidates[n] = (pt, combined, quad_score, letter_density, word_score)
            except Exception:
                candidates[n] = (pt, -9999.0, -9999.0, 0.0, 0.0)

        # choose best combined-scored candidate
        best_key, best_tuple = max(candidates.items(), key=lambda x: x[1][1])
        best_pt, best_score, qsc, lden, wsc = best_tuple
        logging.info(
            f"Railfence: selected rails={best_key} combined={best_score:.6f} quad={qsc:.6f} letter={lden:.3f} words={wsc:.3f}"
        )
        return best_pt

    @staticmethod
    def priority() -> float:
        return 0.05

    def __init__(self, config: Config):
        super().__init__(config)
        logging.basicConfig()

    @staticmethod
    def getParams() -> Optional[Dict[str, ParamSpec]]:
        return {
            "rails": ParamSpec(
                desc="Number of rails used for the railfence cipher.", req=False, default=3
            ),
            "max_rails": ParamSpec(
                desc="Maximum rails to brute-force when no key is supplied.",
                req=False,
                default=40,
            ),
            "quad_weight": ParamSpec(
                desc="Weight for quadgram score when combining signals.", req=False, default=1.0
            ),
            "letter_weight": ParamSpec(
                desc="Weight for letter-density when combining signals.", req=False, default=0.5
            ),
            "word_weight": ParamSpec(
                desc="Weight for common-word hits when combining signals.", req=False, default=0.3
            ),
        }

    @staticmethod
    def getTarget() -> str:
        return "railfence"
