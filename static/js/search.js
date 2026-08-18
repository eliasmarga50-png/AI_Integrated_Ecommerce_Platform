


/**
 * ============================================================
 * AI_Ecommerce
 * Search Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Live search
 * - Debounced requests
 * - Client-side caching
 * - Abort previous requests
 * - Keyboard accessibility
 * ============================================================
 */

"use strict";

const Search = {

    config: {
        debounceDelay: 300,
        minimumCharacters: 2,
        maxCacheSize: 100
    },

    cache: new Map(),

    controller: null,

    debounceTimer: null,

    init() {

        this.cacheDOM();

        if (!this.dom.input) return;

        this.bindEvents();

    },

    cacheDOM() {

        this.dom = {
            input: document.querySelector(".search-input"),
            results: document.querySelector(".search-results"),
            loading: document.querySelector(".search-loading"),
            clear: document.querySelector(".search-clear")
        };

    },

    bindEvents() {

        this.dom.input.addEventListener(
            "input",
            (event) => this.handleInput(event)
        );

        this.dom.clear?.addEventListener(
            "click",
            () => this.clear()
        );

    },

    handleInput(event) {

        const query = event.target.value.trim();

        clearTimeout(this.debounceTimer);

        if (query.length < this.config.minimumCharacters) {

            this.clearResults();

            return;

        }

        this.debounceTimer = setTimeout(() => {

            this.search(query);

        }, this.config.debounceDelay);

    },

    async search(query) {

        if (this.cache.has(query)) {

            this.renderResults(
                this.cache.get(query)
            );

            return;

        }

        if (this.controller) {

            this.controller.abort();

        }

        this.controller = new AbortController();

        this.showLoading(true);

        try {

            const response = await fetch(

                `/ai/search/?q=${encodeURIComponent(query)}`,

                {
                    signal: this.controller.signal,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }

            );

            if (!response.ok) {

                throw new Error("Search failed.");

            }

            const data = await response.json();

            this.addToCache(query, data);

            this.renderResults(data);

        }

        catch (error) {

            if (error.name !== "AbortError") {

                Alerts.error(
                    "Unable to perform search."
                );

            }

        }

        finally {

            this.showLoading(false);

        }

    },

    addToCache(query, data) {

        if (this.cache.size >= this.config.maxCacheSize) {

            const firstKey =
                this.cache.keys().next().value;

            this.cache.delete(firstKey);

        }

        this.cache.set(query, data);

    },

    renderResults(data) {

        if (!this.dom.results) return;

        this.dom.results.innerHTML = "";

        if (!data.results.length) {

            this.dom.results.innerHTML = `
                <div class="search-empty">
                    No products found.
                </div>
            `;

            return;

        }

        data.results.forEach(product => {

            const item = document.createElement("div");

            item.className = "search-result";

            item.innerHTML = `
                <a href="${product.url}">
                    ${product.name}
                </a>
            `;

            this.dom.results.appendChild(item);

        });

    },

    showLoading(show) {

        if (!this.dom.loading) return;

        this.dom.loading.hidden = !show;

    },

    clearResults() {

        if (!this.dom.results) return;

        this.dom.results.innerHTML = "";

    },

    clear() {

        this.dom.input.value = "";

        this.clearResults();

    }

};



