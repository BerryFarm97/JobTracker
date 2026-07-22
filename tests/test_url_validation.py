from main import url_validation_handler


def test_valid_https_url():
    url = "https://example.com/jobs/123"

    is_valid, error_message = url_validation_handler(url)

    assert is_valid is True
    assert error_message == ""


def test_rejects_unsupported_scheme():
    url = "ftp://example.com/file"

    is_valid, error_message = url_validation_handler(url)

    assert is_valid is False
    assert error_message == "\nPlease enter a URL with HTTP or HTTPS"


def test_rejects_missing_hostname():
    url = "https://"

    is_valid, error_message = url_validation_handler(url)

    assert is_valid is False
    assert error_message == "\nURL hostname cannot be empty. Check the URL and try again."


def test_handles_url_parse_failure():
    url = "http://[invalid"

    is_valid, error_message = url_validation_handler(url)

    assert is_valid is False
    assert error_message == "\nURL parse failed. Please re-check the URL and try again."