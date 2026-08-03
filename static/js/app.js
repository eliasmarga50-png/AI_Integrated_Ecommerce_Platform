


/**
 * ============================================================
 * AI_Ecommerce
 * Main Application Bootstrap
 * ------------------------------------------------------------
 * Responsibilities
 * - Wait for the DOM to be ready
 * - Cache commonly used DOM elements
 * - Detect the current page
 * - Initialize feature modules
 * - Register global event listeners
 * - Handle unexpected JavaScript errors
 * ============================================================
 */

"use strict";

/**
 * Main application namespace.
 * Keeping everything inside one object prevents polluting
 * the global scope and makes the code easier to maintain.
 */
const App = {
    /**
     * Global configuration.
     * Centralizing configuration avoids hardcoding values
     * throughout the application.
     */
    config: {
        debug: true,
        version: "1.0.0",
    },

    /**
     * Cache frequently used DOM elements.
     * Query once, reuse many times.
     */
    cacheDOM() {
        this.dom = {
            body: document.body,
            navbar: document.querySelector(".navbar"),
            alerts: document.querySelector(".alerts"),
        };
    },

    /**
     * Detect useful information about the current page.
     * This allows modules to initialize only when needed.
     */
    detectPage() {
        this.page = {
            path: window.location.pathname,
            isHome: window.location.pathname === "/",
            isDashboard: window.location.pathname.startsWith("/dashboard"),
            isCheckout: window.location.pathname.startsWith("/checkout"),
        };
    },

    /**
     * Initialize all feature modules.
     * Each module is responsible for checking whether it
     * should activate on the current page.
     */
    initializeModules() {
        if (window.Navbar?.init) Navbar.init();
        if (window.Alerts?.init) Alerts.init();
        if (window.Validation?.init) Validation.init();
        if (window.Search?.init) Search.init();
        if (window.Cart?.init) Cart.init();
        if (window.Checkout?.init) Checkout.init();
        if (window.Dashboard?.init) Dashboard.init();
        if (window.Chatbot?.init) Chatbot.init();
    },

    /**
     * Register application-wide event listeners.
     */
    registerEvents() {
        window.addEventListener("error", (event) => {
            if (this.config.debug) {
                console.error("Application Error:", event.error);
            }
        });

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                console.log("Application paused.");
            } else {
                console.log("Application resumed.");
            }
        });
    },

    /**
     * Main application entry point.
     */
    init() {
        console.log(`AI_Ecommerce v${this.config.version} starting...`);

        this.cacheDOM();
        this.detectPage();
        this.registerEvents();
        this.initializeModules();

        console.log("Application initialized successfully.");
    },
};

/**
 * Wait until the DOM is fully loaded before initializing.
 * This ensures every HTML element is available.
 */
document.addEventListener("DOMContentLoaded", () => {
    App.init();
});


