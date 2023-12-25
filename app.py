***REMOVED***


def greet(name, intensity,test):
***REMOVED***


demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.components.Slider()],
    outputs=["text"],
)

***REMOVED***
    demo.launch()
