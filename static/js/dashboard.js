



/**
 * ============================================================
 * AI_Ecommerce
 * Dashboard Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Dashboard initialization
 * - Widget loading
 * - Statistics refresh
 * - Dashboard auto refresh
 * - Role detection
 * ============================================================
 */

"use strict";

const Dashboard = {

    config: {
        refreshInterval: 60000, // 60 seconds
        endpoint: "/dashboard/api/"
    },

    state: {
        role: null,
        loading: false,
        widgets: {}
    },

    refreshTimer: null,

    init() {

        this.cacheDOM();

        if (!this.dom.dashboard) return;

        this.detectRole();

        this.bindEvents();

        this.loadDashboard();

        this.startAutoRefresh();

    },

    cacheDOM() {

        this.dom = {

            dashboard: document.querySelector(".dashboard"),

            refreshButton:
                document.querySelector(".dashboard-refresh"),

            statCards:
                document.querySelectorAll(".stat-card"),

            notificationArea:
                document.querySelector(".dashboard-notifications")

        };

    },

    detectRole() {

        this.state.role =
            this.dom.dashboard.dataset.role || "customer";

    },

    bindEvents() {

        this.dom.refreshButton?.addEventListener(

            "click",

            () => this.refresh()

        );

    },

    async loadDashboard() {

        this.state.loading = true;

        try {

            const response = await fetch(

                `${this.config.endpoint}${this.state.role}/`

            );

            if (!response.ok) {

                throw new Error("Dashboard loading failed.");

            }

            const data = await response.json();

            this.render(data);

        }

        catch (error) {

            Alerts.error(

                "Unable to load dashboard."

            );

        }

        finally {

            this.state.loading = false;

        }

    },

    render(data) {

        this.renderStatistics(data.statistics);

        this.renderNotifications(data.notifications);

    },

    renderStatistics(statistics) {

        this.dom.statCards.forEach(card => {

            const key = card.dataset.stat;

            if (statistics[key] !== undefined) {

                card.querySelector(".stat-value").textContent =
                    statistics[key];

            }

        });

    },

    renderNotifications(notifications) {

        if (!this.dom.notificationArea) return;

        this.dom.notificationArea.innerHTML = "";

        notifications.forEach(notification => {

            const item = document.createElement("div");

            item.className = "dashboard-notification";

            item.textContent = notification.message;

            this.dom.notificationArea.appendChild(item);

        });

    },

    refresh() {

        this.loadDashboard();

        Alerts.info(

            "Dashboard refreshed."

        );

    },

    startAutoRefresh() {

        this.refreshTimer = setInterval(

            () => this.loadDashboard(),

            this.config.refreshInterval

        );

    },

    stopAutoRefresh() {

        clearInterval(this.refreshTimer);

    }

};


