from pathlib import Path
from threading import Thread, enumerate, main_thread
import sys
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Sort_folder:
    path_to = None

    def __init__(self, path_from):
        self.path_from = path_from
    
    def __call__(self):
        files = (self.path_from.glob('*.*'))
        for src_file in files:
            new_path = self.path_to.joinpath(src_file.suffix[1:])
            new_file = new_path.joinpath(src_file.name)
            try:
                Path.mkdir(new_path)
            except:
                pass

            iter_post = 1
            while True:
                try:
                    src_file.rename(new_file)
                    break
                except:
                    new_file = Path(new_path, src_file.stem + str(iter_post) + src_file.suffix)
                    iter_post += 1


def create_threed(path_from):
    threed_ = Thread(target=Sort_folder(path_from))
    threed_.start()

def iter_dir(path):
    for i in path.iterdir():
        if i.is_dir():
            create_threed(i)
            iter_dir(i)

def kill_dir(path):
    for i in path.iterdir():
        if i.is_dir():
            kill_dir(i)
            try:
                i.rmdir()
            except:
                pass


if __name__ == '__main__':
    if  len(sys.argv) != 2:
        logger.debug("Insert path")
        sys.exit(1)
    path = Path((sys.argv[1]).lower())
    if not path.is_dir():
        logger.debug("path not found")
        sys.exit(1)

    Sort_folder.path_to = path
    create_threed(path)     
    iter_dir(path)

    threads = enumerate()
    threads.pop(threads.index(main_thread()))
    [thr.join() for thr in threads]
    
    kill_dir(path)

    logger.debug("End")