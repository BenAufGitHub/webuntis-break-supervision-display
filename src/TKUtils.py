import tkinter as tk


'''
This class solves a very bugging problem:
You cannot put a scrollbar on a frame.
You can put it on a canvas, but a canvas can't resize its components dynamically.
Note that the class is only the container, children should be added to 'self.frame'.
References:
https://pythonguides.com/python-tkinter-scrollbar/  ('Python Tkinter Scrollbar Canvas')
https://stackoverflow.com/a/57745179/16288659
'''
class ScrollContainer(tk.Frame):


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient='horizontal', width=16)

        self.scrollbar.config(command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._frame_id = self.canvas.create_window(
                                0,  0,
                                anchor='nw',
                                window=self.frame)
        self.frame.bind('<Configure>', self.onFrameConfigure)
        self.canvas.bind('<Configure>', self.onCanvasConfigure)


    '''
    Enables scrolling through the frames grid
    '''
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.frame.bbox('all'))


    '''
    Configures canvas.frame to adjust to canvas-height accordingly.
    '''
    def onCanvasConfigure(self, event): 
        self.canvas.itemconfigure(self._frame_id, height=self.canvas.winfo_height())


    def get_frame(self) -> tk.Frame:
        return self.frame
