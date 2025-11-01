"""
Helper functions para processamento de requests HTTP
"""


def parse_boolean_param(value: str | None, default: bool = True) -> bool:
    """
    Converte string de query parameter para boolean

    Args:
        value: String do query parameter (ex: 'true', 'false', '1', '0')
        default: Valor padrão se value for None

    Returns:
        Boolean correspondente

    Examples:
        >>> parse_boolean_param('true')
        True
        >>> parse_boolean_param('false')
        False
        >>> parse_boolean_param('1')
        True
        >>> parse_boolean_param('0')
        False
        >>> parse_boolean_param(None, default=True)
        True
    """
    if value is None:
        return default

    return value.lower() in ('true', '1', 'yes', 't', 'y')
