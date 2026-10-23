"""Canonical annotation vocabulary for the renders ledger (tech#375).

readiness.py's render-unannot gate accepts exactly five states. Ledger rows
are written by hand (and by render commands), so the tokens live here once:
a self-coined label is invisible to the gate and surfaces as an
"unannotated" leak instead of a readable vocabulary error. Three rounds
(R2399 v71, R2411 v25/v26, R2425 v28) were spent re-diagnosing that gap.
"""

TEST_MARK = "\u6d4b\u8bd5\u4ef6\u00b7\u975e\u6210\u54c1"  # test piece
PRODUCT_MARK = "\u6210\u54c1\u00b7\u6279\u6b21"  # production piece (batch)
PRODUCT_SLOT_MARK = "\u6210\u54c1\u00b7\u843d\u4f4d"  # production piece (slot-filled)
SUPERSEDED_MARK = "\u5df2\u88ab\u53d6\u4ee3"  # superseded archive row
DISPOSED_MARK = "\u5f03\u4eb6\u7559\u6863"  # disposed archive row

# Multi-mention rank: the most specific state wins when a cell names several.
LEGAL_MARKS = (
    PRODUCT_SLOT_MARK,
    PRODUCT_MARK,
    SUPERSEDED_MARK,
    DISPOSED_MARK,
    TEST_MARK,
)


def legal_vocabulary():
    """Human-readable list of the legal tokens, for gate messages."""
    return " / ".join(LEGAL_MARKS)


def assert_legal(mark):
    """Raise ValueError unless `mark` is one of the five legal tokens."""
    if mark not in LEGAL_MARKS:
        raise ValueError(
            "illegal renders mark %r (legal: %s)" % (mark, legal_vocabulary())
        )
    return mark