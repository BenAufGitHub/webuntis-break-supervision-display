import tkinter as tk
from datetime import datetime
from src import Constants
from tkinter.messagebox import showerror
import traceback, sys
import pyperclip


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



class WidthControlledScrollContainer(ScrollContainer):
    def __init__(self, parent, grid_item_width: int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.item_width = grid_item_width

    
    '''
    Configures canvas.frame to adjust to canvas-height and -width accordingly.
    '''
    def onCanvasConfigure(self, event): 
        super().onCanvasConfigure(event)
        grid_width = len(self.frame.winfo_children()) * self.item_width
        self.canvas.itemconfigure(self._frame_id, width=max(grid_width, self.canvas.winfo_width()))


class FillerFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **{"bg":Constants.BACKGROUND, **kwargs})


'''
Illustation of current day, e.g. "Sa, den 09.11."
'''
class DayLabel(tk.Label):

    
    def __init__(self, parent, dayObject: datetime, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.month = dayObject.month
        self.day = dayObject.day
        self.weekday = dayObject.weekday()
        self.set_text(self.month, self.day, self.weekday)


    def set_text(self, month, day, weekday):
        week_day_abbr = self.match(weekday)
        self.config(text=f'{week_day_abbr}, den {day}.{month}.')


    '''
    With the respective German abbreviations.
    '''
    def match(self, weekday):
        abbrs = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        return abbrs[weekday]

    

class TKErrorHandler:


    def report_callback_exception(caller, exc, val, tb):
        instructions = '''Vorgehen bei weiteren Problemen:\n1. Das Traceback per Mail an "bmette.api@gmail.com"\noder\n2. Issue an 
"https://github.com/BenAufGitHub/webuntis-break-supervision-display/issues" schreiben.'''
        msg = f'Fehler:\n{val}\n\n{instructions}\n\nTraceback:\nvom Typ {exc},\nTraceback wurde automatisch kopiert.'
        TKErrorHandler._copy(exc, val, tb)
        showerror("Fehler", message=msg)


    def _copy(exc, val, tb):
        msg = TKErrorHandler._prepare_clipboard_msg(exc, val, tb)
        if sys.stderr: sys.stderr.write(msg)
        pyperclip.copy(msg)


    def _prepare_clipboard_msg(exc, val, tb):
        lines = traceback.format_tb(tb)
        tb_result = lines.pop(0)
        for line in lines:
            tb_result += "\n"+line
        return f'{exc}\n{val}\nTraceback (webuntis-bs):\n{tb_result}'