


/**
 * ============================================================
 * AI_Ecommerce
 * Alerts Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Success notifications
 * - Error notifications
 * - Warning notifications
 * - Info notifications
 * - Auto dismiss
 * - Manual close
 * ============================================================
 */

"use strict";

const Alerts = {

    config: {
        duration: 4000,
        maxAlerts: 5
    },

    init() {

        this.cacheDOM();

        if (!this.dom.container) {
            this.createContainer();
        }

    },

    cacheDOM() {

        this.dom = {
            container: document.querySelector("#alert-container")
        };

    },

    createContainer() {

        const container = document.createElement("div");

        container.id = "alert-container";

        document.body.appendChild(container);

        this.dom.container = container;

    },

    show(message, type = "info") {

        if (!this.dom.container) return;

        this.limitAlerts();

        const alert = document.createElement("div");

        alert.className = `alert alert-${type}`;

        const messageElement =
    document.createElement("span");

messageElement.className =
    "alert-message";

messageElement.textContent =
    message;

const closeButton =
    document.createElement("button");

closeButton.className =
    "alert-close";

closeButton.type = "button";

closeButton.textContent = "×";

alert.appendChild(messageElement);
alert.appendChild(closeButton);

        this.dom.container.appendChild(alert);

        this.attachCloseEvent(alert);

        this.autoDismiss(alert);

    },

    success(message) {
        this.show(message, "success");
    },

    error(message) {
        this.show(message, "error");
    },

    warning(message) {
        this.show(message, "warning");
    },

    info(message) {
        this.show(message, "info");
    },

    attachCloseEvent(alert) {

        const button = alert.querySelector(".alert-close");

        if (!button) return;

        button.addEventListener("click", () => {

            this.remove(alert);

        });

    },

    autoDismiss(alert) {

        setTimeout(() => {

            this.remove(alert);

        }, this.config.duration);

    },

    remove(alert) {

        if (!alert) return;

        alert.classList.add("fade-out");

        setTimeout(() => {

            alert.remove();

        }, 300);

    },

    limitAlerts() {

        const alerts = this.dom.container.children;

        while (alerts.length >= this.config.maxAlerts) {

            alerts[0].remove();

        }

    }

};


