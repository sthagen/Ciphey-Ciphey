from typing import Dict, Optional
import math

import logging
from typing import Optional, Dict, Tuple

from ciphey.iface import Config, Decoder, ParamSpec, T, U, registry
from ciphey.basemods.Checkers.ezcheck import EzCheck
from ciphey.basemods.Checkers.quadgrams import Quadgrams


@registry.register
class Route(Decoder[str]):
    def decode(self, ctext: T) -> Optional[U]:
        params = self._params()

        def decode_with(cols: int) -> str:
            if cols <= 1:
                return ctext

            length = len(ctext)
            rows = math.ceil(length / cols)
            full_cols = length % cols

            col_sizes = []
            for c in range(cols):
                if full_cols == 0:
                    col_sizes.append(rows)
                else:
                    if c < full_cols:
                        col_sizes.append(rows)
                    else:
                        col_sizes.append(rows - 1)

            cols_data = []
            idx = 0
            for size in col_sizes:
                cols_data.append(list(ctext[idx : idx + size]))
                idx += size

            result = []
            for r in range(rows):
                for c in range(cols):
                    if r < len(cols_data[c]):
                        result.append(cols_data[c][r])

            return "".join(result)

        # If user supplied columns param, use it
        if "columns" in params and params["columns"] is not None:
            try:
                cols = int(params["columns"])
                return decode_with(cols)
            except Exception:
                pass

        # Brute-force columns and score with Quadgrams
        cfg = self._config()
        quad = cfg(Quadgrams)
        max_cols = int(self._params().get("max_columns", 20))
        max_cols = min(max_cols, max(2, len(ctext)))

        candidates: Dict[int, Tuple[str, float, float, float, float]] = {}
        quad_w = float(self._params().get("quad_weight", 1.0))
        letter_w = float(self._params().get("letter_weight", 0.5))
        word_w = float(self._params().get("word_weight", 0.3))

        common_words = ["THE", "AND", "IS", "IN", "OF", "TO", "YOU", "HELLO"]

        for cols in range(2, max_cols + 1):
            pt = decode_with(cols)
            try:
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

                letters = sum(1 for c in pt if c.isalpha())
                letter_density = letters / max(1, len(pt))

                up = pt.upper()
                hits = sum(up.count(w) for w in common_words)
                word_score = hits / max(1, len(pt) / 4)

                combined = quad_w * quad_score + letter_w * letter_density + word_w * word_score
                candidates[cols] = (pt, combined, quad_score, letter_density, word_score)
            except Exception:
                candidates[cols] = (pt, -9999.0, -9999.0, 0.0, 0.0)

        best_key, best_tuple = max(candidates.items(), key=lambda x: x[1][1])
        best_pt, best_score, qsc, lden, wsc = best_tuple
        logging.info(
            f"Route: selected columns={best_key} combined={best_score:.6f} quad={qsc:.6f} letter={lden:.3f} words={wsc:.3f}"
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
            "columns": ParamSpec(
                desc="Number of columns used for the route/columnar transposition.",
                req=False,
                default=4,
            ),
            "max_columns": ParamSpec(
                desc="Maximum columns to brute-force when no key is supplied.",
                req=False,
                default=12,
            ),
        }

    @staticmethod
    def getTarget() -> str:
        return "route"
