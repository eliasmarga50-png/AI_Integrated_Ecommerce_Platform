


"""
Base payment gateway client.

Contains shared functionality used by all payment providers.
"""

import logging

import requests
from django.conf import settings

from ..exceptions import (
    GatewayConnectionError,
    GatewayTimeoutError,
    GatewayAuthenticationError,
)

from ..utils import generate_idempotency_key


logger = logging.getLogger(__name__)


class BasePaymentGateway:
    """
    Base class for all payment gateway integrations.

    Provider-specific gateways should inherit from this class.
    """

    base_url = None
    api_key = None

    timeout = getattr(
        settings,
        "PAYMENT_GATEWAY_TIMEOUT",
        30,
    )

    def __init__(
        self,
        *,
        base_url=None,
        api_key=None,
    ):
        self.base_url = (
            base_url or self.base_url
        )

        self.api_key = (
            api_key or self.api_key
        )

        self.session = requests.Session()

    # -------------------------------------------------
    # Headers
    # -------------------------------------------------

    def get_headers(self):
        """
        Default authentication headers.

        Providers can override this.
        """

        return {
            "Authorization": (
                f"Bearer {self.api_key}"
                if self.api_key
                else ""
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Idempotency-Key": (
                generate_idempotency_key()
            ),
        }

    # -------------------------------------------------
    # HTTP methods
    # -------------------------------------------------

    def request(
        self,
        *,
        method,
        endpoint,
        data=None,
        headers=None,
    ):
        """
        Perform an HTTP request to a gateway.
        """

        url = (
            f"{self.base_url}{endpoint}"
        )

        request_headers = (
            self.get_headers()
        )

        if headers:
            request_headers.update(
                headers
            )

        try:

            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=request_headers,
                timeout=self.timeout,
            )

        except requests.Timeout:

            logger.exception(
                "Payment gateway timeout"
            )

            raise GatewayTimeoutError()

        except requests.ConnectionError:

            logger.exception(
                "Payment gateway connection failed"
            )

            raise GatewayConnectionError()

        except requests.RequestException:

            logger.exception(
                "Payment gateway request failed"
            )

            raise GatewayConnectionError()


        return self.handle_response(
            response
        )


    # -------------------------------------------------
    # Response handling
    # -------------------------------------------------

    def handle_response(
        self,
        response,
    ):
        """
        Normalize gateway responses.
        """

        if response.status_code in (
            401,
            403,
        ):

            raise GatewayAuthenticationError()


        try:

            response_data = response.json()

        except ValueError:

            response_data = {
                "raw_response":
                    response.text
            }


        if not response.ok:

            logger.error(
                "Gateway error: %s",
                response_data,
            )

            return {
                "success": False,
                "status_code":
                    response.status_code,
                "data":
                    response_data,
            }


        return {
            "success": True,
            "status_code":
                response.status_code,
            "data":
                response_data,
        }


    # -------------------------------------------------
    # Required gateway methods
    # -------------------------------------------------

    def initialize_payment(
        self,
        payment,
    ):
        """
        Start payment.

        Must be implemented by providers.
        """

        raise NotImplementedError(
            "Gateway must implement initialize_payment()."
        )


    def verify_payment(
        self,
        payment,
    ):
        """
        Verify payment.

        Must be implemented by providers.
        """

        raise NotImplementedError(
            "Gateway must implement verify_payment()."
        )


    def refund_payment(
        self,
        payment,
    ):
        """
        Refund payment.

        Must be implemented by providers.
        """

        raise NotImplementedError(
            "Gateway must implement refund_payment()."
        )