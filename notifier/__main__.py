from .core.notifierapp import NotifierApp

if __name__ == "__main__":
    app = NotifierApp.instance()
    app.start_app()
