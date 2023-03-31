from IPython.display import display, HTML


def displayVideo(path):
    html_str = "<video src=\""+path+"\" ></video>"

    print(html_str)
    display(HTML(html_str))
