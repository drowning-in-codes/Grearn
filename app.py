import gradio as gr
import time
import requests
import json

from fastapi import HTTPException


def greet(name, intensity):
    return "Hello" * intensity + name + "!"


# demo = gr.Interface(
#     fn=greet,
#     inputs=[gr.components.Textbox(placeholder="input your words"), gr.Textbox(placeholder=""),gr.components.Slider()],
#     outputs=["text",gr.Checkbox(label="选择")],
# )

def update(name):
    return "Hello" + name + "!"


with gr.Blocks(theme=gr.themes.Glass()) as test:
    gr.Markdown("## Hello World")
    with gr.Row():
        textbox = gr.Textbox(placeholder="input your words", label="name")
        slider = gr.components.Slider(label="Greet", interactive=True)
    btn = gr.Button("Run")
    btn.click(fn=update, inputs=textbox, outputs=slider)


# stt_demo = gr.load(
#     "huggingface/facebook/wav2vec2-base-960h",
#     title=None,
#     inputs="mic",
#     description="Let me try to guess what you're saying!",
# )

# def slow_echo(message, history):
#     for i in range(len(message)):
#         time.sleep(0.3)
#         print(history)
#         yield "You typed: " + message[: i + 1]


def req_bot(message, history, temperature=0.7):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"},
        data=json.dumps({
            "model": "mistralai/mistral-7b-instruct",  # Optional
            "messages": [
                {"role": "user", "content": f"${message}"}
            ],
            "temperature": temperature,
        })
    )
    res = response.json()["choices"][0]["message"]["content"].strip('"')
    yield res


with gr.Blocks() as demo:
    gr.Markdown("## Chat with Mistral")
    temperature = gr.components.Slider(label="Temperature", value=0.7, minimum=0.1, maximum=1.0)
    chat_demo = gr.ChatInterface(req_bot, additional_inputs=temperature, ).queue()

# demo = gr.TabbedInterface([test, chat_demo], ["Hello World", "chat"])

if __name__ == '__main__':
    try:
        demo.launch()
    except HTTPException:
        pass
    except AttributeError:
        pass