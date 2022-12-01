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
        frame = DisplayFrame(parent=self, session=session)
        frame.grid(row=0, column=0) 
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )


    
    def selectLoginFrame(self):
        frame = LoginFrame(parent=self)
        frame.grid(row=0, column=0)
        frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT )



# ================== Frames =========================


class FillerFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **{"bg":Constants.BACKGROUND, **kwargs})



class DisplayFrame(FillerFrame):
    
    def __init__(self, parent, session: webuntis.Session):
        super().__init__(parent)
        self.session = session
        self._build(session)


    def _build(self, session: webuntis.Session):
        settings_bar = self._create_settings_bar()
        table_frame = self._create_table_frame()
        exit_bar = self._create_exit_bar()

        self._pack_contents(settings_bar, table_frame, exit_bar)


    def _pack_contents(self, settings_bar, table_frame, exit_bar):
        settings_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP )
        table_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        exit_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP)


    def _create_settings_bar(self):
        settings_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=60, relief='groove', highlightthickness=2)
        retry = tk.Button(settings_bar, text="\u27F3", padx=-1, pady=-1, font=("SherifSans", 20), borderwidth=0)
        retry.configure(activeforeground="blue", activebackground=Constants.BACKGROUND, bg=Constants.BACKGROUND)
        retry.place(x=20, y=3)
        return settings_bar


    def _create_exit_bar(self):
        exit_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=80, relief='groove', highlightthickness=2)
        b1 = tk.Button(exit_bar, padx=5, text="LogOut")
        b2 = tk.Button(exit_bar, padx=5, text="Beenden")
        b1.place(relx=0.45, rely=0.5, anchor=tk.E)
        b2.place(relx=0.55, rely=0.5, anchor=tk.W)
        return exit_bar



    # =============== middle frame =================>


    def _create_table_frame(self):
        frame = FillerFrame(self)
        self._create_arrow(frame, '\u2B9C').pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self._create_table(frame).pack(anchor=tk.W, fill=tk.BOTH, expand=True, side=tk.LEFT)
        self._create_arrow(frame, "\u2B9E").pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        return frame


    def _create_table(self, parent):
        table = FillerFrame(parent, bg="blue")
        return table


    def _create_arrow(self, parent, text):
        bg=Constants().BACKGROUND
        arrow_frame = FillerFrame(parent, width=120)

        arrow = tk.Button(arrow_frame, text=text)
        arrow.configure(borderwidth=0, font=("Arial", 30), activeforeground="blue", bg=bg, activebackground=bg)
        arrow.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return arrow_frame


    def _on_button_press(self, event):
        event.widget.configure(bg="red")




class LoginFrame(FillerFrame):
    pass
