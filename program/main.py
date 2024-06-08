import multiprocessing

from gui.MainFrame import MainFrame

if __name__ == "__main__":
    multiprocessing.freeze_support()
    MainFrame.start()
