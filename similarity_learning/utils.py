__all__ = ['fix_notebook_widgets']

def fix_notebook_widgets():
    """Taken from https://github.com/microsoft/vscode-jupyter/issues/13163"""
    from IPython.display import clear_output, DisplayHandle
    def update_patch(self, obj):
        clear_output(wait=True)
        self.display(obj)
    DisplayHandle.update = update_patch
