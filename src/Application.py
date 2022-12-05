import tkinter as tk
from tkinter import ttk
import webuntis
import src.UntisBreaks as UntisBreaks
import src.TKUtils as TKUtils
import idlelib.tooltip


class Constants:
    WIDTH=1000
    HEIGHT=600
    RESIZABLE=True
    BACKGROUND="#93B5E1"
    C_PERIOD="lightblue"
    ITEM_WIDTH=200



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
        self.data = None
        self.currentBreak = None
        self._build()


    def reload_tables(self):
        self._change_table(None, _fEmpty=True, _fMessage="aktualisiert Inhalte...")
        self.update()
        self.fetch_break_info()
        self._change_table(self.currentBreak)


    # TODO try-catch connection -> send back to login frame + Error-Popup
    def fetch_break_info(self):
        self.data = UntisBreaks.get_todays_supervisions(self.session)
        self.currentBreak = UntisBreaks.next_break_time(self.data.keys())

    
    def is_displayable(self):
        return self.currentBreak


    def _build(self):
        self.fetch_break_info()
        settings_bar = self._create_settings_bar()
        self.table_frame = self._create_table_frame()
        exit_bar = self._create_exit_bar()

        self._pack_contents(settings_bar, self.table_frame, exit_bar)


    def _pack_contents(self, settings_bar, table_frame, exit_bar):
        settings_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP )
        exit_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.BOTTOM)
        table_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)


    def _create_settings_bar(self):
        settings_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=60, relief='groove', highlightthickness=2)
        retry = tk.Button(settings_bar, text="\u27F3", padx=-1, pady=-1, font=("SherifSans", 20), borderwidth=0)
        retry.configure(activeforeground="blue", activebackground=Constants.BACKGROUND, bg=Constants.BACKGROUND)
        retry.configure(command=self.reload_tables)
        retry.place(x=20, y=3)
        return settings_bar


    def _create_exit_bar(self):
        exit_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=80, relief='groove', highlightthickness=2)
        b1 = tk.Button(exit_bar, padx=5, text="Log Out")
        b2 = tk.Button(exit_bar, padx=5, text="Beenden")
        b1.place(relx=0.45, rely=0.5, anchor=tk.E)
        b2.place(relx=0.55, rely=0.5, anchor=tk.W)
        return exit_bar



    # =============== middle frame =================>


    def _create_table_frame(self, forceEmpty=(False, None)):
        frame = FillerFrame(self)
        self._create_arrow(frame, '\u2B9C', -1).pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        if not forceEmpty[0] and self.is_displayable():
            self._create_table(frame).pack(anchor=tk.W, fill=tk.BOTH, expand=True, side=tk.LEFT)
        else:
            self._create_empty_table(frame, forceEmpty[1]).pack(anchor=tk.W, fill=tk.BOTH, expand=True, side=tk.LEFT)
        self._create_arrow(frame, "\u2B9E", 1).pack(anchor=tk.W, fill=tk.Y, side=tk.RIGHT)
        return frame


    def _create_arrow(self, parent, text, offset):
        arrow_frame = FillerFrame(parent, width=120)

        arrow = tk.Button(arrow_frame, text=text)
        arrow.configure(borderwidth=0, font=("Arial", 30))
        self._toggle_button(arrow, offset)
        arrow.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return arrow_frame


    '''
    whether a previous/next pause exists decides whether arrow should be activated or not
    @param arrow: arrow-button to toggle
    @param offset: how many breaks too look back or forward to. Since the arrows only change break position by one, this value should be 1 or -1.
    '''
    def _toggle_button(self, arrow, offset):
        bg=Constants().BACKGROUND
        if self.currentBreak:
            rel_break = UntisBreaks.get_relative_break(self.currentBreak, self.data.keys(), offset)
        # deactivate if necessary
        if not (self.currentBreak and rel_break):
            arrow["state"] = "disabled"
            return arrow.configure(activeforeground=bg, bg=bg, activebackground=bg, foreground="gray")
        # activate
        arrow["state"] = "normal"
        arrow.configure(activeforeground="blue", bg=bg, activebackground=bg, foreground="black")
        arrow.config(command=lambda:self._change_table(rel_break))

    
    def _change_table(self, selected_break_time, _fEmpty=False, _fMessage=None):
        self.currentBreak = selected_break_time
        self.table_frame.destroy()
        self.table_frame = self._create_table_frame(forceEmpty=(_fEmpty, _fMessage))
        self.table_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    
    def _create_empty_table(self, parent, message):
        msg = message if message else "Hier ist nichts zu sehen :/"
        empty = tk.Frame(parent, bg=Constants().BACKGROUND)
        empty.pack_propagate(False)
        label = tk.Label(empty, text=msg, bg=Constants().BACKGROUND)
        label.configure(font="Helvetica 10 italic")
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return empty


    # ==== inner Table ====>


    def _create_table(self, parent):
        table = FillerFrame(parent, bg="blue")
        self._addTime(table)
        container = TKUtils.WidthControlledScrollContainer(table, Constants().ITEM_WIDTH)
        container.pack(fill=tk.BOTH, expand=True)
        self._add_periods_to_grid(container.get_frame())
        return table


    def _add_periods_to_grid(self, frame: tk.Frame):
        frame.rowconfigure(0, weight=1)
        for i, period in enumerate(self.data[self.currentBreak]):
            frame.columnconfigure(i, weight=1)

            pFrame = tk.Frame(frame, bg=self.getPeriodBG(period), width=Constants.ITEM_WIDTH, padx=40)
            pFrame.config(highlightbackground="gray", highlightthickness=1)
            self.config_tooltip(period, pFrame)
            pFrame.pack_propagate(False)
            pFrame.columnconfigure(0, weight=1)
            pFrame.rowconfigure(0, weight=1)
            pFrame.rowconfigure(1, weight=1)

            self._add_teachers(pFrame, period)
            self._add_rooms(pFrame, period)
            pFrame.grid(row=0, column=i, sticky=tk.NSEW)


    def config_tooltip(self, period, widget):
        if period.code == 'cancelled':
            idlelib.tooltip.Hovertip(widget,'Abgesagte Stunde')
        if period.code == 'irregular':
            idlelib.tooltip.Hovertip(widget,'Irreguläre Stunde')


    def _add_teachers(self, parent, period):
        # gray border frame to fill space
        borderFrame = tk.Frame(parent, bg="gray", width=Constants().ITEM_WIDTH)
        borderFrame.pack_propagate(False)
        borderFrame.grid(row=0, column=0, sticky=tk.NSEW)

        # then frame with pad-bottom=1   => showing gray border
        tFrame = tk.Frame(borderFrame, bg=self.getPeriodBG(period))
        tFrame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, anchor=tk.NW, pady=(0,1), padx=(0,0))
        teachers_text = self._str_teachers(period)
        tLabel = tk.Label(tFrame, text=teachers_text[:-2], font=("Arial", 10))
        tLabel.config(fg=self.getPeriodFG(period), bg=self.getPeriodBG(period))
        tLabel.bind('<Configure>', lambda e: tLabel.config(wraplength=tLabel.winfo_width()))
        tLabel.pack( side=tk.BOTTOM, pady=(10,20))


    def getPeriodBG(self, period):
        if period.code=='cancelled':
            return '#ff4d4d'
        if period.code=='irregular':
            return '#fc00fc'
        return Constants().C_PERIOD

    def getPeriodFG(self, period):
        if period.code=='cancelled':
            return "white"
        return "black"


    '''
        For unknown reasons, an index error is thrown if the list is empty.
        Printing the period show a teacher as id=0, but no such teachers exists,
        therefore I can only reckon this is the webuntis way of saying there is no teacher.
    '''
    def _str_teachers(self, period):
        teachers_text = ""
        try:
            for t in period.teachers:
                teachers_text += t.full_name + "\n" + "\n"
        except IndexError:
            pass
        for t in period.original_teachers:
            teachers_text += f"({t.full_name})\n\n"
        return teachers_text if teachers_text else "----"


    def _add_rooms(self, parent, period):
        rFrame = tk.Frame(parent, bg=self.getPeriodBG(period))
        rFrame.pack_propagate(False)
        rFrame.grid(row=1, column=0, sticky=tk.NSEW)
        room_text = ""
        for r in period.rooms:
            room_text += r.long_name + "\n" +"\n"
        for r in period.original_rooms:
            room_text += f"({r.long_name})\n\n"
        room_text = room_text if room_text else "----"
        rLabel = tk.Label(rFrame, text=room_text[:-2], font=("Arial", 10))
        rLabel.config(bg=self.getPeriodBG(period), fg=self.getPeriodFG(period))
        rLabel.pack(side=tk.TOP, pady=(20,10))


    def _addTime(self, parent):
        upperside = FillerFrame(parent, height=70)
        tk.Label(upperside, text=self._getTime(), padx=5, pady=5, bg=Constants.BACKGROUND, font=("Courier", 18)).pack(anchor=tk.W)
        upperside.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP)


    def _getTime(self):
        date=self.currentBreak
        minute = date.minute if date.minute > 9 else f"0{date.minute}"
        return f"Start: {date.hour}:{minute}"






class LoginFrame(FillerFrame):
    pass
