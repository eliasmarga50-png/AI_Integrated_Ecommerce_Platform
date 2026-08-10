


class OrderError(Exception):
    """
    Base exception for order-related business errors.
    """


class EmptyCartError(OrderError):
    """
    Raised when attempting to create an order from an empty cart.
    """


class ProductUnavailableError(OrderError):
    """
    Raised when a product cannot currently be purchased.
    """


class InsufficientStockError(OrderError):
    """
    Raised when requested quantity exceeds available stock.
    """


