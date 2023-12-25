import gradio as gr


def greet(name, intensity,test):
    return "Hello" * intensity + name + "!"


demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.components.Slider()],
    outputs=["text"],
)

if __name__ == '__main__':
    demo.launch()
