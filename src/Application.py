import tkinter as tk
from tkinter import ttk
import webuntis


class Constants:
    WIDTH=1000
    HEIGHT=600
    RESIZABLE=True
    BACKGROUND="#93B5E1"


class MainFrame(tk.Tk):

    # ================ public ================


    def __init__(self):
        super().__init__()
        self.configure_variables()
        self.session = None


    def mainloop(self, session: webuntis.Session=None) -> None:
        try:
            self._before_start(session)
            super().mainloop()
        finally:
            self._logout()


    def _before_start(self, session: webuntis.Session) -> None:
        if self._prelogin(session):
            return self.selectDisplayFrame(session)
        self.selectLoginPanel()


    # ============ session handling ===============
    

    def _prelogin(self, session) -> bool:
        try:
            if not session: return False
            self.session = session.login()
            return True
        except webuntis.errors.AuthError | webuntis.errors.BadCredentialsError:
            return False


    def _logout(self):
        if not self.session: return
        self.session.logout(suppress_errors=True)



    # ========== front-end elements ================


    def configure_variables(self):
        self.resizable(Constants.RESIZABLE, Constants.RESIZABLE)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width-Constants.WIDTH)/2
        y = (screen_height-Constants.HEIGHT)/2

        self.title('Pausenaufsicht')
        self.geometry(f'{Constants.WIDTH}x{Constants.HEIGHT}+{int(x)}+{int(y)}')
        # TODO icon


    def selectDisplayFrame(self, session: webuntis.Session):
        frame = DisplayFrame(parent=self)
        frame.grid(row=0, column=0) 
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )


    
    def selectLoginFrame(self):
        frame = LoginFrame(parent=self)
        frame.grid(row=0, column=0)
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )



# ================== Frames =========================


class FillerFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Constants.BACKGROUND)



class DisplayFrame(FillerFrame):
    pass



class LoginFrame(FillerFrame):
    pass
