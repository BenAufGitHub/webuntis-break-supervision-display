import tkinter as tk
from tkinter import ttk
import webuntis
from src import DisplayFrame, Constants, TKUtils


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
        self.selectLoginFrame()


    # ============ session handling ===============
    

    def _prelogin(self, session) -> bool:
        try:
            if not session: return False
            self.session = session.login()
            return True
        except webuntis.errors.BadCredentialsError:
            # TODO ModalWindow (Bad Login Data)=> Redirection to Login
            return False
        except webuntis.errors.AuthError:
            # TODO ModalWindow (Auth failed)=> Redirection to Login
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
        self.iconphoto(False, tk.PhotoImage(file='./src/appIcon.png'))
        self.geometry(f'{Constants.WIDTH}x{Constants.HEIGHT}+{int(x)}+{int(y)}')


    def selectDisplayFrame(self, session: webuntis.Session):
        frame = DisplayFrame.DisplayFrame(parent=self, session=session)
        frame.grid(row=0, column=0) 
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )


    def selectLoginFrame(self):
        frame = LoginFrame(parent=self)
        frame.grid(row=0, column=0)
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )



# ================== Frames =========================


class LoginFrame(TKUtils.FillerFrame):
    pass
