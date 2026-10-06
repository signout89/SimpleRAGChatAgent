import gradio as gr
from dotenv import load_dotenv

from answer import answer_question

load_dotenv(override=True)

FORCE_LIGHT_MODE = """
() => {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.href = url.href;
    }
}
"""


def format_context(context):
    result = "<h2 style='color: #15803d;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #15803d;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result


def to_text_messages(history):
    """Convert Gradio 6 chat history (content as a list of parts) to plain text messages."""
    return [
        {"role": m["role"], "content": "".join(p["text"] for p in m["content"] if p["type"] == "text")}
        for m in history
    ]


def chat(history):
    messages = to_text_messages(history)
    last_message = messages[-1]["content"]
    prior = messages[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)


def main():
    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(
        primary_hue="green", neutral_hue="gray", font=["Inter", "system-ui", "sans-serif"]
    ).set(
        body_background_fill="white",
        block_background_fill="#f0fdf4",
        block_border_color="#bbf7d0",
        input_background_fill="white",
    )

    with gr.Blocks(title="Insurellm Expert Assistant") as ui:
        gr.Markdown("# 🏢 Insurellm Expert Assistant\nAsk me anything about Insurellm!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 Conversation", height=600, buttons=["copy"]
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about Insurellm...",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="📚 Retrieved Context",
                    value="*Retrieved context will appear here*",
                    container=True,
                    height=600,
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    ui.launch(inbrowser=True, theme=theme, js=FORCE_LIGHT_MODE)


if __name__ == "__main__":
    main()
