import webuntis
import src.Application as App


def launch(session: webuntis.Session=None):
    root = App.MainFrame()
    root.mainloop(session=session)