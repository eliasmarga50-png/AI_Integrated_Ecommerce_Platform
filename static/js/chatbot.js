



/**
 * ============================================================
 * AI_Ecommerce
 * Chatbot Module
 * ------------------------------------------------------------
 * Responsibilities
 * - Conversation management
 * - AI communication
 * - Typing indicator
 * - Message rendering
 * - Error handling
 * ============================================================
 */

"use strict";

const Chatbot = {

    config: {
        endpoint: "/ai/chat/"
    },

    state: {
        loading: false,
        typing: false,
        sessionId: crypto.randomUUID(),
        messages: []
    },

    init() {

        this.cacheDOM();

        if (!this.dom.form) return;

        this.bindEvents();

    },

    cacheDOM() {

        this.dom = {

            form:
                document.querySelector(".chatbot-form"),

            input:
                document.querySelector(".chatbot-input"),

            messages:
                document.querySelector(".chatbot-messages"),

            button:
                document.querySelector(".chatbot-send")

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

        const message =
            this.dom.input.value.trim();

        if (!message) return;

        this.addMessage("user", message);

        this.dom.input.value = "";

        this.toggleTyping(true);

        try {

            const response = await fetch(

                this.config.endpoint,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "X-CSRFToken":
                            this.getCSRFToken()
                         

                    },
                    
                    getCSRFToken() {

    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    )?.value || "";

},

                    body: JSON.stringify({

                        message,

                        session_id:
                            this.state.sessionId

                    })

                }

            );

            if (!response.ok) {

                throw new Error();

            }

            const data = await response.json();

            this.addMessage(

                "assistant",

                data.message

            );

        }

        catch (error) {

            Alerts.error(

                "Unable to contact AI assistant."

            );

        }

        finally {

            this.toggleTyping(false);

        }

    },

    addMessage(role, content) {

        this.state.messages.push({

            role,

            content

        });

        this.renderMessage(

            role,

            content

        );

    },

    renderMessage(role, content) {

        const message =
            document.createElement("div");

        message.className =
            `chat-message ${role}`;

        message.textContent = content;

        this.dom.messages.appendChild(message);

        this.scrollToBottom();

    },

    toggleTyping(show) {

        this.state.typing = show;

        this.dom.button.disabled = show;

        this.dom.button.textContent =
            show

            ? "Thinking..."

            : "Send";

    },

    scrollToBottom() {

        this.dom.messages.scrollTop =
            this.dom.messages.scrollHeight;

    }

};


