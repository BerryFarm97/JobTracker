from main import get_user_int


def test_get_user_int_returns_valid_choice(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda prompt: "2")

    result = get_user_int("Choose an option: ", 3)

    assert result == 2


def test_get_user_int_retries_after_non_integer(monkeypatch):
    responses = iter(["abc", "2"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))
    result = get_user_int("Choose an option: ", 3)

    assert result == 2
