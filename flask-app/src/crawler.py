import threading


class CrawlingThread(threading.Thread):
    def __init__(self):
        super(CrawlingThread, self).__init__()
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            pass
        finally:
            print("収集が完了しました")