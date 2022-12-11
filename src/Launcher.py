import webuntis
import src.Application as App
import src.TKUtils as tku


def launch(session: webuntis.Session=None):
    try:
        root = App.MainFrame()
        root.mainloop(session=session)
    except Exception as e:
        tku.TKErrorHandler.report_callback_exception(None, e.__class__.__name__, str(e), e.__traceback__)