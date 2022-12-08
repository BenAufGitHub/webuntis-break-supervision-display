import idlelib.tooltip
from threading import Thread
import tkinter as tk
from datetime import datetime, timedelta

import webuntis
from src import UntisBreaks, TKUtils, Constants



class DisplayFrame(TKUtils.FillerFrame):
    

    def __init__(self, parent, session: webuntis.Session):
        super().__init__(parent)
        self.session = session
        self.is_today = True
        self.data = None
        self.currentBreak = None
        # For pretending to have a different day, otherwise should be 0.
        self.natural_offset = 0
        self.break_offset_hours = 0
        self._build()


    def finishMainloop(self):
        self.winfo_toplevel().destroy()


    '''
    Errorhandling: Interaction with webuntis
    '''
    def _api_fail_save(self, callback):
        try:
            callback()
        except webuntis.errors.NotLoggedInError as e:
            # TODO ModalWindow (Session Expired/Logged Out) => Login Page
            raise e
        except webuntis.errors.RemoteError as e:
            # TODO ModalWIndow (Server interaction failed) => Login Page
            # Display Details/Send Mail Option
            # use provided data for analysis
            raise e


    def _threaded_fail_save(self, callback):
        try:
            callback()
        except Exception as e:
            TKUtils.TKErrorHandler.report_callback_exception(self, e.__class__.__name__, str(e), e.__traceback__)



    # TODO try-catch connection -> send back to login frame + Error-Popup
    '''
    For the "current" day's table (or whatever the natural_offset suggests).
    '''
    def fetch_break_info(self):
        def do():
            self.data = UntisBreaks.get_offset_supervisions(self.session, self.natural_offset)
            current_time = datetime.now()+timedelta(days=self.natural_offset, hours=self.break_offset_hours)
            self.currentBreak = UntisBreaks.next_break_time(self.data.keys(), current=current_time)
        self._api_fail_save(do)

    
    def fetch_nextday_info(self):
        def do():
        # for Mo-Do => Move 1, else move to Monday
            next_day = self._get_next_day() + self.natural_offset
            self.data = UntisBreaks.get_offset_supervisions(self.session, next_day)
            self.currentBreak = UntisBreaks.next_break_time(self.data.keys())
        self._api_fail_save(do)


    def _get_next_day(self):
        weekday = (datetime.now()+timedelta(days=self.natural_offset)).weekday()
        return 1 if weekday < 4 else 7-weekday


    # ======== building =======>


    def _build(self):
        self.settings_bar = self._create_settings_bar()
        self.table_frame = self._create_table_frame(forceEmpty=(True, "läd Inhalte.."))
        exit_bar = self._create_exit_bar()

        self._pack_contents(self.settings_bar, self.table_frame, exit_bar)
        self.after(10, self.after_init)


    def _pack_contents(self, settings_bar, table_frame, exit_bar):
        settings_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP )
        exit_bar.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.BOTTOM)
        table_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)


    def after_init(self, data_source=None):
        data_source = self._after_init_prep(data_source)
        def do():
            try:
                self._after_init_can_fail(data_source)
            except webuntis.errors.NotLoggedInError:
                pass    # means that user has already logged out
            except RuntimeError as e:
                try:    # if 'winfo_exists' throws an error, then tk closed => do nothing
                    if self.winfo_exists():
                        raise e
                except: pass
        Thread(target=lambda: self._threaded_fail_save(do)).start()


    def _after_init_prep(self, data_source):
        self.toggle_load_buttons(False)
        if hasattr(self, 'day_label') and self.day_label: self.day_label.destroy()
        return data_source if data_source else self.fetch_break_info


    def _after_init_can_fail(self, data_source):
        data_source()
        self._change_table(self.currentBreak)
        self.update_day_label()
        self.toggle_load_buttons(True)


    # ====== settings bar ======>


    def _create_settings_bar(self):
        settings_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=60, relief='groove', highlightthickness=2)
        self.retry = tk.Button(settings_bar, text="\u27F3", padx=-1, pady=-1, font=("SherifSans", 20), borderwidth=0)
        self.retry.configure(activeforeground="blue", activebackground=Constants.BACKGROUND, bg=Constants.BACKGROUND)
        self.retry.configure(command=self.reload_tables)
        self.retry.place(x=20, y=3)

        self.toggle_day = tk.Button(settings_bar, text="Nächstes >>", borderwidth=0)
        self.toggle_day.config(font=("Arial", 13), bg=Constants.BACKGROUND, activeforeground="blue", activebackground=Constants.BACKGROUND)
        self.toggle_day.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        self.toggle_day.config(command=self.toggleDay)
        return settings_bar

    
    def toggleDay(self):
        self.toggle_load_buttons(False)
        self._change_table(None, _fEmpty=True, _fMessage="aktualisiert Inhalte...")
        self.is_today = not self.is_today
        if self.is_today:
            self.toggle_day.config(text="Nächstes >>")
            return self.after_init(data_source=self.fetch_break_info)
        self.toggle_day.config(text="<< Aktuelles")
        self.after_init(data_source=self.fetch_nextday_info)


    def toggle_load_buttons(self, activate):
        if activate:
            self.retry["state"] = 'normal'
            self.toggle_day["state"] = 'normal'
            return
        self.retry["state"] = 'disabled'
        self.toggle_day["state"] = 'disabled'

    
    '''
    Spawns label with day-info on the top right in the settings bar.
    Recalling will automatically replace the old label.
    '''
    def update_day_label(self):
        if hasattr(self, 'day_label') and self.day_label: self.day_label.destroy()
        ref_time = self._get_reference_day()
        self.day_label = TKUtils.DayLabel(self.settings_bar, ref_time, borderwidth=0)
        self.day_label.config(font=("Arial", 13), bg=Constants.BACKGROUND)
        self.day_label.place(relx=0.95, rely=0.55, anchor=tk.E)


    '''
    A datetime object from the day of the shown table
    '''
    def _get_reference_day(self) -> datetime:
        if self.currentBreak: return self.currentBreak
        if self.is_today:
            return datetime.now() + timedelta(days=self.natural_offset)
        return datetime.now() + timedelta(days=self.natural_offset+self._get_next_day())


    # ======= exit bar =======>


    def _create_exit_bar(self):
        exit_bar = tk.Frame(self, bg=Constants.BACKGROUND, height=80, relief='groove', highlightthickness=2)
        b1 = tk.Button(exit_bar, padx=5, text="Log Out")
        b2 = tk.Button(exit_bar, padx=5, text="Beenden", command=self.finishMainloop)
        b1.place(relx=0.45, rely=0.5, anchor=tk.E)
        b2.place(relx=0.55, rely=0.5, anchor=tk.W)
        return exit_bar



    # =============== middle frame =================>


    # whether a table can be created
    def is_displayable(self):
            return self.currentBreak


    def reload_tables(self):
        self.toggle_load_buttons(False)
        self._change_table(None, _fEmpty=True, _fMessage="aktualisiert Inhalte...")
        self.update()
        get = self.fetch_break_info if self.is_today else self.fetch_nextday_info
        self.after_init(data_source=get)


    '''
    param forceEmpty: 2-tuple with [0: create-empty-table] and [1: Text to be displayed on empty frame]
    '''
    def _create_table_frame(self, forceEmpty=(False, None)):
        frame = TKUtils.FillerFrame(self)
        self._create_arrow(frame, '\u2B9C', -1).pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        if not forceEmpty[0] and self.is_displayable():
            self._create_table(frame).pack(anchor=tk.W, fill=tk.BOTH, expand=True, side=tk.LEFT)
        else:
            self._create_empty_table(frame, forceEmpty[1]).pack(anchor=tk.W, fill=tk.BOTH, expand=True, side=tk.LEFT)
        self._create_arrow(frame, "\u2B9E", 1).pack(anchor=tk.W, fill=tk.Y, side=tk.RIGHT)
        return frame


    def _create_arrow(self, parent, text, offset):
        arrow_frame = TKUtils.FillerFrame(parent, width=120)

        arrow = tk.Button(arrow_frame, text=text)
        arrow.configure(borderwidth=0, font=("Arial", 30))
        self._toggle_button(arrow, offset)
        arrow.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return arrow_frame


    '''
    existence of previous/next decides whether arrow should be activated or not
    @param arrow: arrow-button to toggle
    @param offset: how many breaks too look back or forward to. Since the arrows only change break position by one, this value should be 1 or -1.
    '''
    def _toggle_button(self, arrow, offset):
        bg=Constants.BACKGROUND
        def do():
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
        self._api_fail_save(do)

    
    '''
    Difference to reload_tables: Not refreshing data, only displaying different breaks.
    '''
    def _change_table(self, selected_break_time, _fEmpty=False, _fMessage=None):
        self.currentBreak = selected_break_time
        self.table_frame.destroy()
        self.table_frame = self._create_table_frame(forceEmpty=(_fEmpty, _fMessage))
        self.table_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)



    # ==== empty table ====>


    def _create_empty_table(self, parent, message):
        msg = message if message else "Hier ist nichts zu sehen :/"
        empty = tk.Frame(parent, bg=Constants.BACKGROUND)
        empty.pack_propagate(False)
        label = tk.Label(empty, text=msg, bg=Constants.BACKGROUND)
        label.configure(font="Helvetica 10 italic")
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return empty


    # ==== inner Table (scrollbar-layer) ====>


    def _create_table(self, parent):
        table = TKUtils.FillerFrame(parent, bg="blue")
        self._addTime(table)
        container = TKUtils.WidthControlledScrollContainer(table, Constants.ITEM_WIDTH)
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
        borderFrame = tk.Frame(parent, bg="gray", width=Constants.ITEM_WIDTH)
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
        upperside = TKUtils.FillerFrame(parent, height=70)
        tk.Label(upperside, text=self._getTime(), padx=5, pady=5, bg=Constants.BACKGROUND, font=("Courier", 18)).pack(anchor=tk.W)
        upperside.pack(anchor=tk.N, fill=tk.X, expand=False, side=tk.TOP)


    def _getTime(self):
        date=self.currentBreak
        minute = date.minute if date.minute > 9 else f"0{date.minute}"
        return f"Start: {date.hour}:{minute}"


    # ==== color configs =====>
    

    def getPeriodBG(self, period):
        if period.code=='cancelled':
            return '#ff4d4d'
        if period.code=='irregular':
            return '#fc00fc'
        return Constants.C_PERIOD


    def getPeriodFG(self, period):
        if period.code=='cancelled':
            return "white"
        return "black"