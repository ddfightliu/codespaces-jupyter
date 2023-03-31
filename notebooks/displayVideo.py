from IPython.display import display, HTML


def displayVideo():
    html_str = '''
            <video src=\"{}\" />
        '''
    display(HTML(html_str))
