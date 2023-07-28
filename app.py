import gradio as gr
import os
from typing import Iterator

DEFAULT_SYSTEM_PROMPT = (
    os.getenv("DEFAULT_SYSTEM_PROMPT")
    if os.getenv("DEFAULT_SYSTEM_PROMPT") is not None
    else ""
)

css = """
    /* Submit button */
    .submit-btn {
         --hover-shadows: 16px 16px 33px #121212,
                           -16px -16px 33px #303030;
         --accent: fuchsia;
         font-weight: bold;
         letter-spacing: 0.1em;
         border: none;
         border-radius: 1.5em;
         background-color: #212121;
         color: white;
         padding: 1em 2em;
         transition: box-shadow ease-in-out 0.3s,
                     background-color ease-in-out 0.1s,
                     letter-spacing ease-in-out 0.1s,
                     transform ease-in-out 0.1s;
         box-shadow: 13px 13px 10px #1c1c1c,
                     -13px -13px 10px #262626;
    }
    
    .submit-btn:hover {
        box-shadow: var(--hover-shadows);
    }
    
    .submit-btn:active {
         box-shadow: var(--hover-shadows),
                      var(--accent) 0px 0px 30px 5px;
         background-color: var(--accent);
         transform: scale(0.95);
         border-radius: 3.0em
    }

    """


def clear_and_save_text_box(message: str) -> tuple[str, str]:
    return "", message


def process_example(example: str) -> tuple[str, str]:
    return "", example


def display_input(
    message: str, history: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    history.append((message, ""))
    return history


with gr.Blocks(css=css) as app:
    with gr.Group():
        chatbot = gr.Chatbot(label="llamav2-bot")
        with gr.Row():
            chatIn = gr.Textbox(
                scale=6,
                container=False,
                show_label=False,
                placeholder="How can I help you ?",
                elem_classes="textbox-primary"
            )
            submit = gr.Button(
                "submit",
                variant="primary",
                scale=1,
                min_width=0,
                size="sm",
                elem_classes="submit-btn"
            )

        with gr.Row():
            retry_button = gr.Button("🔄  Retry", variant="secondary")
            undo_button = gr.Button("↩️ Undo", variant="secondary")
            clear_button = gr.Button("🗑️  Clear", variant="secondary")

        saved_inputs = gr.State()

        with gr.Accordion(label="Options++", open=False):
            system_prompt = gr.Textbox(
                label="System prompt", value=DEFAULT_SYSTEM_PROMPT, lines=6
            )

        # gr.Examples(
        #     examples=[
        #         "Hello there! How are you doing?",
        #         "Can you explain briefly to me what is the Python programming language?",
        #         "Explain the plot of Cinderella in a sentence.",
        #         "How many hours does it take a man to eat a Helicopter?",
        #         "Write a 100-word article on 'Benefits of Open-Source in AI research'",
        #     ],
        #     inputs=chatIn,
        #     outputs=[chatIn, chatbot],
        #     fn=process_example,
        #     cache_examples=True,
        # )

        chatIn.submit(
            fn=clear_and_save_text_box,
            inputs=chatIn,
            outputs=[chatIn, saved_inputs],
            api_name=False,
            queue=False
        ).then(
            fn=display_input,
            inputs=[saved_inputs, chatbot],
            outputs=chatbot,
            api_name=False,
            queue=False
        )
        # ).then(
        #
        #     inputs=[saved_inputs, chatbot, system_prompt],
        #     api_name=False,
        #     queue=False
        # ).success(
        #
        # )

if __name__ == "__main__":
    app.queue(max_size=28).launch()
