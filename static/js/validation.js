


/**
 * ============================================================
 * AI_Ecommerce
 * Validation Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Validate common form inputs
 * - Validate complete forms
 * - Display validation errors
 * - Reusable across the application
 * ============================================================
 */

"use strict";

const Validation = {

    patterns: {
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        phone: /^[0-9+\-\s()]{7,20}$/,
        username: /^[a-zA-Z0-9_]{3,30}$/,
        url: /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/.*)?$/,
    },

    init() {
        console.log("Validation module initialized.");
    },

    required(value) {
        return value.trim().length > 0;
    },

    email(value) {
        return this.patterns.email.test(value.trim());
    },

    phone(value) {
        return this.patterns.phone.test(value.trim());
    },

    username(value) {
        return this.patterns.username.test(value.trim());
    },

    url(value) {
        return this.patterns.url.test(value.trim());
    },

    minLength(value, length) {
        return value.trim().length >= length;
    },

    maxLength(value, length) {
        return value.trim().length <= length;
    },

    number(value) {
        return !isNaN(value);
    },

    match(value1, value2) {
        return value1 === value2;
    },

    validateField(field, rules) {

        const value = field.value;

        if (rules.required && !this.required(value)) {
            return "This field is required.";
        }

        if (rules.email && !this.email(value)) {
            return "Enter a valid email address.";
        }

        if (rules.phone && !this.phone(value)) {
            return "Enter a valid phone number.";
        }

        if (rules.username && !this.username(value)) {
            return "Username is invalid.";
        }

        if (rules.url && !this.url(value)) {
            return "Enter a valid URL.";
        }

        if (rules.minLength &&
            !this.minLength(value, rules.minLength)) {

            return `Minimum ${rules.minLength} characters required.`;
        }

        if (rules.maxLength &&
            !this.maxLength(value, rules.maxLength)) {

            return `Maximum ${rules.maxLength} characters allowed.`;
        }

        if (rules.number && !this.number(value)) {
            return "Enter a valid number.";
        }

        return null;
    },

    validateForm(form, schema) {

        let valid = true;

        Object.keys(schema).forEach(name => {

            const field = form.elements[name];

            if (!field) return;

            const error = this.validateField(
                field,
                schema[name]
            );

            if (error) {

                valid = false;

                field.classList.add("is-invalid");

                Alerts.error(error);

            } else {

                field.classList.remove("is-invalid");

            }

        });

        return valid;
    }

};


