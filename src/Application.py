from tkinter import *
from tkinter.ttk import *
import webuntis


class MainFrame(Tk):

    # ================ public ================


    def __init__(self):
        super().__init__()
        self.create_layout()
        self.session = None


    def mainloop(self, session: webuntis.Session=None) -> None:
        try:
            self._before_start(session)
            super().mainloop()
        finally:
            self._logout()


    def _before_start(self, session: webuntis.Session):
        if self._prelogin(session):
            self.selectDisplayPanel()


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



    def create_layout(self):
        self.configure_variables()
        # TODO


    def configure_variables(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 1000
        height = 600
        x = (screen_width-width)/2
        y = (screen_height-height)/2

        self.title('Pausenaufsicht')
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.resizable(True, True)
        # TODO icon


    def selectDisplayPanel(self):
        pass

    
    def selectLoginPanel(self):
        pass
