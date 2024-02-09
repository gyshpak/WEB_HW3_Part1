from pathlib import Path
from threading import Thread, Lock, enumerate, main_thread
import sys
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

class Sort_folder:
    path_to = None
    
    def __init__(self, path_from, lock_mov_file: Lock, lock_mk_dir: Lock):
        self.path_from = path_from
        self.lock_mov_file = lock_mov_file
        self.lock_mk_dir = lock_mk_dir
    
    def __call__(self):
        files = (self.path_from.glob('*.*'))
        for src_file in files:
            new_path = self.path_to.joinpath(src_file.suffix[1:])
            new_file = new_path.joinpath(src_file.name)

            self.lock_mk_dir.acquire()
            if not Path.is_dir(new_path):
                Path.mkdir(new_path)
            self.lock_mk_dir.release()

            iter_post = 1
            self.lock_mov_file.acquire()
            while True:
                if Path.is_file(new_file):
                    new_file = Path(new_path, src_file.stem + str(iter_post) + src_file.suffix)
                    iter_post += 1
                else:
                    src_file.rename(new_file)
                    break
            self.lock_mov_file.release()


def create_threed(path_from, lock_move_file, lock_mk_dir):
    threed_ = Thread(target=Sort_folder(path_from, lock_move_file, lock_mk_dir))
    threed_.start()

def iter_dir(path, lock_move_file, lock_mk_dir):
    for i in path.iterdir():
        if i.is_dir():
            create_threed(i, lock_move_file, lock_mk_dir)
            iter_dir(i, lock_move_file, lock_mk_dir)

def kill_dir(path):
    for i in path.iterdir():
        if i.is_dir():
            kill_dir(i)
            try:
                i.rmdir()
            except:
                pass


if __name__ == '__main__':
    lock_move_file = Lock()
    lock_mk_dir = Lock()

    if  len(sys.argv) != 2:
        logger.debug("Insert path")
        sys.exit(1)
    path = Path((sys.argv[1]).lower())
    if not path.is_dir():
        logger.debug("path not found")
        sys.exit(1)

    Sort_folder.path_to = path
    create_threed(path, lock_move_file, lock_mk_dir)     
    iter_dir(path, lock_move_file, lock_mk_dir)

    threads = enumerate()
    threads.pop(threads.index(main_thread()))
    [thr.join() for thr in threads]
    
    kill_dir(path)

    logger.debug("End")
