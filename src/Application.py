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
        pass


    def selectDisplayPanel(self):
        pass

    
    def selectLoginPanel(self):
        pass
