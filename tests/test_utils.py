from app.utils import format_currency


def test_format_currency_with_decimal():
    input_value = 1234.56
    result = format_currency(input_value)
    
    assert result == "1234,56"


def test_format_currency_with_integer():
    input_value = 1234
    result = format_currency(input_value)

    assert result == "1234,00"


def test_format_currency_with_zero():
    input_value = 0
    result = format_currency(input_value)
    
    assert result == "0,00"
