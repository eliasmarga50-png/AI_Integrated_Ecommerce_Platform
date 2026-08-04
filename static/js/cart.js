



/**
 * ============================================================
 * AI_Ecommerce
 * Cart Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Cart state management
 * - Add / Remove products
 * - Update quantity
 * - Calculate totals
 * - Persist guest cart
 * - Synchronize with backend
 * ============================================================
 */

"use strict";

const Cart = {

    config: {
        storageKey: "ai_ecommerce_cart",
        taxRate: 0.15,
        shipping: 0,
        syncDelay: 500
    },

    state: {
        items: [],
        subtotal: 0,
        tax: 0,
        shipping: 0,
        discount: 0,
        total: 0
    },

    syncTimer: null,

    init() {

        this.cacheDOM();

        this.load();

        this.bindEvents();

        this.calculateTotals();

        this.render();

    },

    cacheDOM() {

        this.dom = {
            badge: document.querySelector(".cart-badge"),
            items: document.querySelector(".cart-items"),
            subtotal: document.querySelector(".cart-subtotal"),
            tax: document.querySelector(".cart-tax"),
            shipping: document.querySelector(".cart-shipping"),
            total: document.querySelector(".cart-total")
        };

    },

    bindEvents() {

        document.addEventListener("click", (event) => {

            const addButton = event.target.closest("[data-add-cart]");

            if (addButton) {

                this.add({
                    id: addButton.dataset.productId,
                    name: addButton.dataset.productName,
                    price: parseFloat(addButton.dataset.productPrice),
                    quantity: 1
                });

            }

        });

    },

    add(product) {

        const existing = this.state.items.find(

            item => item.id === product.id

        );

        if (existing) {

            existing.quantity++;

        }

        else {

            this.state.items.push(product);

        }

        this.afterUpdate();

        Alerts.success("Product added to cart.");

    },

    remove(productId) {

        this.state.items = this.state.items.filter(

            item => item.id !== productId

        );

        this.afterUpdate();

        Alerts.info("Product removed.");

    },

    updateQuantity(productId, quantity) {

        const item = this.state.items.find(

            item => item.id === productId

        );

        if (!item) return;

        if (quantity <= 0) {

            this.remove(productId);

            return;

        }

        item.quantity = quantity;

        this.afterUpdate();

    },

    calculateTotals() {

        this.state.subtotal = this.state.items.reduce(

            (sum, item) => sum + item.price * item.quantity,

            0

        );

        this.state.tax =
            this.state.subtotal * this.config.taxRate;

        this.state.shipping =
            this.config.shipping;

        this.state.total =
            this.state.subtotal +
            this.state.tax +
            this.state.shipping -
            this.state.discount;

    },

    afterUpdate() {

        this.calculateTotals();

        this.save();

        this.render();

        this.queueSync();

    },

    render() {

        this.updateBadge();

        this.renderTotals();

    },

    updateBadge() {

        if (!this.dom.badge) return;

        const count = this.state.items.reduce(

            (sum, item) => sum + item.quantity,

            0

        );

        this.dom.badge.textContent = count;

    },

    renderTotals() {

        this.dom.subtotal &&
            (this.dom.subtotal.textContent =
                this.state.subtotal.toFixed(2));

        this.dom.tax &&
            (this.dom.tax.textContent =
                this.state.tax.toFixed(2));

        this.dom.shipping &&
            (this.dom.shipping.textContent =
                this.state.shipping.toFixed(2));

        this.dom.total &&
            (this.dom.total.textContent =
                this.state.total.toFixed(2));

    },

    save() {

        localStorage.setItem(

            this.config.storageKey,

            JSON.stringify(this.state.items)

        );

    },

    load() {

        const saved = localStorage.getItem(

            this.config.storageKey

        );

        if (!saved) return;

        this.state.items = JSON.parse(saved);

    },

    queueSync() {

        clearTimeout(this.syncTimer);

        this.syncTimer = setTimeout(() => {

            this.sync();

        }, this.config.syncDelay);

    },

    async sync() {

        console.log("Synchronizing cart...");

        /*
        Future implementation:

        POST /cart/sync/

        {
            items: [...]
        }

        Django saves the cart.

        */

    }

};


