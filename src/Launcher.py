import webuntis
import src.Application as App


def launch(session: webuntis.Session=None):
    try:
        root = App.MainFrame()
        root.mainloop(session=session)
    except Exception as e:
        # TODO ModalWindow (something went wrong/see details/send info) => close
        raise e