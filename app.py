import subprocess

import gradio as gr
import requests
import json
import yaml
import os
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
            "Authorization": f"Bearer {orkey}",
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
    with open('./configure.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    orkey = result["OpenRouterKey"]
    try:
        demo.launch()
    except HTTPException:
        pass
    except AttributeError:
        pass
