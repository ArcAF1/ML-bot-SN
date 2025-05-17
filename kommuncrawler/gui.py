import tkinter as tk
from threading import Thread
from queue import Queue, Empty

from .run_pipeline import run

class CrawlThread(Thread):
    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def run(self):
        run(progress_callback=lambda msg: self.queue.put(msg))
        self.queue.put('DONE')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KommunCrawler")
        self.geometry("400x300")

        self.start_btn = tk.Button(self, text="Start", command=self.start_crawl)
        self.start_btn.pack(pady=10)

        self.log_box = tk.Text(self, height=15, width=50)
        self.log_box.pack(expand=True, fill='both')

        self.queue = Queue()
        self.after(100, self.process_queue)

    def start_crawl(self):
        self.start_btn.config(state=tk.DISABLED)
        self.log_box.delete("1.0", tk.END)
        self.worker = CrawlThread(self.queue)
        self.worker.start()

    def process_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg == 'DONE':
                    self.start_btn.config(state=tk.NORMAL)
                    self.log_box.insert(tk.END, "\nCrawl completed.\n")
                else:
                    self.log_box.insert(tk.END, msg + "\n")
                self.log_box.see(tk.END)
        except Empty:
            pass
        self.after(100, self.process_queue)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
