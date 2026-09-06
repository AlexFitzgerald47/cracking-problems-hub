from ric_cipher import build_key, transform


def test_archer_example_rows():
    key = build_key("SWITZERLAND")
    assert key.top == "SWITZERLANDBC"
    assert key.bottom == "FGHJKMOPQUVXY"


def test_cipher_is_involution():
    message = "BY TRAIN TO YOU NOW"
    cipher = transform(message, "SWITZERLAND")
    assert transform(cipher, "SWITZERLAND") == message


def test_keyword_dedup_and_spaces():
    key = build_key("PERSIAN GULF")
    assert key.keyword == "PERSIANGULF"
    assert len(key.top) == len(key.bottom) == 13
    assert set(key.top + key.bottom) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
