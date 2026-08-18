


/**
 * ============================================================
 * AI_Ecommerce
 * Checkout Module
 * ============================================================
 */

"use strict";

const Checkout = {

    config: {
        endpoint: "/orders/create/"
    },

    state: {
        loading: false,
        submitting: false,
        paymentMethod: null,
        shippingMethod: null,
        coupon: null
    },

    init() {
        this.cacheDOM();
        if (!this.dom.form) return;
        this.bindEvents();
    },

    cacheDOM() {
        this.dom = {
            form: document.querySelector("#checkout-form"),
            payment: document.querySelector("#payment-method"),
            shipping: document.querySelector("#shipping-method"),
            button: document.querySelector("#place-order")
        };
    },

    bindEvents() {
        this.dom.form.addEventListener(
            "submit",
            (event) => this.handleSubmit(event)
        );
    },

    async handleSubmit(event) {
        event.preventDefault();

        //stop double clicking
        if (this.state.submitting) return;

        if (!this.validate()) return;

        this.state.submitting = true;
        this.toggleLoading(true);

        try {
            const payload = this.buildPayload();

            const response = await fetch(
                this.config.endpoint,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.getCSRFToken()
                    },
                    body: JSON.stringify(payload)
                }
            );

            if (!response.ok) {
                throw new Error("Checkout failed.");
            }

            const data = await response.json();
            this.handleSuccess(data);

        } catch (error) {
            // Safe fallback if the Alerts global utility doesn't exist
            if (typeof Alerts !== 'undefined' && Alerts.error) {
                Alerts.error("Unable to complete checkout.");
            } else {
                alert("Unable to complete checkout. Please try again.");
            }
        } finally {
            this.state.submitting = false;
            this.toggleLoading(false);
        }
    },

    validate() {
        // Safe fallback check for Cart
        if (typeof Cart === 'undefined' || !Cart.state.items.length) {
            if (typeof Alerts !== 'undefined' && Alerts.warning) {
                Alerts.warning("Your cart is empty.");
            } else {
                alert("Your cart is empty.");
            }
            return false;
        }

        // Safe fallback check for Validation
        if (typeof Validation === 'undefined') {
            return this.dom.form.checkValidity(); // use native browser check if plugin missing
        }

        return Validation.validateForm(
            this.dom.form,
            {
                full_name: { required: true, minLength: 3 },
                email: { required: true, email: true },
                address: { required: true, minLength: 10 }
            }
        );
    },

    buildPayload() {
        // Create a FormData object to easily grab the validated input fields
        const formData = new FormData(this.dom.form);

        return {
            items: typeof Cart !== 'undefined' ? Cart.state.items : [],
            customer_name: formData.get('full_name'),
            customer_email: formData.get('email'),
            shipping_address: formData.get('address'),
            payment_method: this.dom.payment?.value || '',
            shipping_method: this.dom.shipping?.value || '',
            coupon: this.state.coupon
        };
    },

    handleSuccess(data) {
        if (typeof Alerts !== 'undefined' && Alerts.success) {
            Alerts.success("Order created successfully.");
        }

        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    },

    toggleLoading(show) {
        this.state.loading = show;
        if (!this.dom.button) return;

        this.dom.button.disabled = show;
        this.dom.button.textContent = show ? "Processing..." : "Place Order";
    },

    getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    }
};
