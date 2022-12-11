import tkinter as tk
from tkinter import ttk
import webuntis
from src import DisplayFrame, Constants, TKUtils



def handle_callback_errors():
    tk.Tk.report_callback_exception = TKUtils.TKErrorHandler.report_callback_exception



class MainFrame(tk.Tk):

    # ================ public ================


    def __init__(self):
        super().__init__()
        handle_callback_errors()
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

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjust_win_size(parent)
        self._build()


    def adjust_win_size(self, root):
        pass # TODO


    def _build(self):
        self.login_panel = self._create_login_panel()
        self.login_panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def _create_login_panel(self):
        panel = TKUtils.FillerFrame(self, width=230, height=350, highlightthickness=1, highlightbackground="white")
        panel.grid_propagate(False)


        panel.columnconfigure(0, weight=1)
        for i, subframe in enumerate([*self._create_login_elements(panel)]):
            panel.rowconfigure(i, weight=1)
            subframe.grid(row=i, column=0, sticky=tk.W)
        return panel

    
    def _create_login_elements(self, parent):
        user = self._createUserEntry(parent)
        password = self._createPasswordEntry(parent)
        school = self._createSchoolEntry(parent)
        server = self._createServerEntry(parent)
        return user, password, school, server

    
    def _createUserEntry(self, parent):
        user = TKUtils.FillerFrame(parent)
        label = tk.Label(user, text="Benutzer:", pady=4, padx=4, bg=Constants.BACKGROUND, font=("Arial", 11))
        self.user_entry = tk.Entry(user)
        self._base_entry_config(self.user_entry)

        self._entry_grid_configure(user, label, self.user_entry)
        return user


    def _createPasswordEntry(self, parent):
        password = TKUtils.FillerFrame(parent)
        label = tk.Label(password, text="Password:", pady=4, padx=4, bg=Constants.BACKGROUND, font=("Arial", 11))
        self.pw_entry = tk.Entry(password, show="*")
        self._base_entry_config(self.pw_entry)

        self._entry_grid_configure(password, label, self.pw_entry)
        return password


    def _createSchoolEntry(self, parent):
        school = TKUtils.FillerFrame(parent)
        label = tk.Label(school, text="Schule:", pady=4, padx=4, bg=Constants.BACKGROUND, font=("Arial", 11))
        self.school_entry = tk.Entry(school)
        self._base_entry_config(self.school_entry)

        self._entry_grid_configure(school, label, self.school_entry)
        return school


    def _createServerEntry(self, parent):
        server = TKUtils.FillerFrame(parent)
        label = tk.Label(server, text="Server:", pady=4, padx=4, bg=Constants.BACKGROUND, font=("Arial", 11))
        self.server_entry = tk.Entry(server)
        self._base_entry_config(self.server_entry)

        self._entry_grid_configure(server, label, self.server_entry)
        return server


    def _base_entry_config(self, entry):
        entry.config(width=25, font=("Arial", 11), borderwidth=6, relief=tk.FLAT)

    
    def _entry_grid_configure(self, grid_parent, label, entry):
        grid_parent.columnconfigure(0, weight=1)
        grid_parent.rowconfigure(0, weight=1)
        grid_parent.rowconfigure(1, weight=1)

        label.grid(row=0, column=0, sticky=tk.W)
        entry.grid(row=1, column=0, sticky=tk.NSEW, padx=4)