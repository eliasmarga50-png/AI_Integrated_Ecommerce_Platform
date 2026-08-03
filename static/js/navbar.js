



/**
 * ============================================================
 * AI_Ecommerce
 * Navbar Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Mobile menu
 * - User dropdown
 * - Sticky navbar
 * - Active navigation links
 * - Accessibility
 * ============================================================
 */

"use strict";

const Navbar = {

    init() {
        this.cacheDOM();
        this.bindEvents();
        this.highlightActiveLink();
    },

    cacheDOM() {
        this.dom = {
            navbar: document.querySelector(".navbar"),
            toggle: document.querySelector(".navbar-toggle"),
            menu: document.querySelector(".navbar-menu"),
            userToggle: document.querySelector(".navbar-user-toggle"),
            userMenu: document.querySelector(".navbar-user-menu"),
            links: document.querySelectorAll(".navbar-menu a")
        };
    },

    bindEvents() {

        if (this.dom.toggle) {
            this.dom.toggle.addEventListener(
                "click",
                () => this.toggleMenu()
            );
        }

        if (this.dom.userToggle) {
            this.dom.userToggle.addEventListener(
                "click",
                (event) => {
                    event.stopPropagation();
                    this.toggleUserMenu();
                }
            );
        }

        document.addEventListener(
            "click",
            (event) => this.handleOutsideClick(event)
        );

        document.addEventListener(
            "keydown",
            (event) => this.handleKeyboard(event)
        );

        window.addEventListener(
            "scroll",
            () => this.handleStickyNavbar()
        );
    },

    toggleMenu() {

        if (!this.dom.menu) return;

        const isOpen = this.dom.menu.classList.toggle("active");

        this.dom.toggle.setAttribute(
            "aria-expanded",
            isOpen
        );
    },

    toggleUserMenu() {

        if (!this.dom.userMenu) return;

        this.dom.userMenu.classList.toggle("active");
    },

    handleOutsideClick(event) {

        if (
            this.dom.userMenu &&
            this.dom.userToggle &&
            !this.dom.userMenu.contains(event.target) &&
            !this.dom.userToggle.contains(event.target)
        ) {
            this.dom.userMenu.classList.remove("active");
        }
    },

    handleKeyboard(event) {

        if (event.key !== "Escape") return;

        this.dom.menu?.classList.remove("active");
        this.dom.userMenu?.classList.remove("active");
    },

    handleStickyNavbar() {

        if (!this.dom.navbar) return;

        this.dom.navbar.classList.toggle(
            "sticky",
            window.scrollY > 40
        );
    },

    highlightActiveLink() {

        const currentPath = window.location.pathname;

        this.dom.links.forEach(link => {

            const href = link.getAttribute("href");

            if (href === currentPath) {
                link.classList.add("active");
            }
        });
    }

};


