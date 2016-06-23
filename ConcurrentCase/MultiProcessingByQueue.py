# encoding: 'utf-8'
__author__ = 'xyc'


"""
__doc__: 这个案例是基于使用multiprocessing.JoinableQueue,multiprocessing.Queue完成多进程的并发任务，此方案可避免在应用中使用锁
         本案例为缩小指定文件夹图片，并保持到目标目录

tips：对于python由于GIL的限制，一般建议采用多进程来实现计算密集性任务，对于I／O密集型任务，多进程和多线程都可以

"""


import argparse, multiprocessing, os, collections, sys, math
import Image

Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
                        default=multiprocessing.cpu_count(),
                        help="specify the concurrency (for debugging and " "timing) [default: %(default)d]")
    parser.add_argument("-s", "--size", default=400, type=int,
                        help="make a scaled image that fits the given dimension" "[default: %(default)d]")
    parser.add_argument("-S", "--smooth", action="store_true",
                        help="use smooth scaling (slow bug good for text)")
    parser.add_argument("source",
                        help="the directory containing the original .xpm images")
    parser.add_argument("target",
                        help="the directory for the scaled .xpm images")
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)
    if source == target:
        args.error("source and target must be different")
    if not os.path.exists(args.target):
        os.makedirs(target)
    return args.size, args.smooth, source, target, args.concurrency


def report(message="", error=False):
    if len(message) >= 70 and not error:
        message = message[:67] + "..."
    sys.stdout.write("\r{:70}{}".format(message, "\n" if error else ""))
    sys.stdout.flush()


def scale(size, smooth, source, target, concurrency):
    canceled = False
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_process(size, smooth, jobs, results, concurrency)
    todo = add_jobs(source, target, jobs)
    try:
        jobs.join()
    except KeyboardInterrupt:
        report("canceling...")
    copied = scaled = 0
    while not results.empty(): # Safe because all jobs have finished
        result = results.get_nowait()
        copied += result.copied
        scaled += result.scaled
    return Summary(todo, copied, scaled, canceled)


def create_process(size, smooth, jobs, results, concurrency):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=(size,
                                                    smooth, jobs, results))
        process.daemon = True  # 设置为守护进程，随主进程终止而退出，如果为非守护进程在主进程退出后仍运行，会成为僵尸进程
        process.start()


def worker(size, smooth, jobs, results):
    while True:
        try:
            source_image, target_image = jobs.get()
            try:
                result = scale_one(size, smooth, source_image, target_image)
                report("{} {}".format("copied" if result.copied else
                                        "scaled", os.path.basename(result.name)))
                results.put(result)
        except Image.Error as err:
            report(str(err), True)
        finally:
            jobs.task_done()


def add_jobs(source, target, jobs):
    for todo, name in enumerate(os.listdir(source), start=1):
        source_image = os.path.join(source, name)
        target_image = os.path.join(target, name)
        jobs.put(source_image, target_image)
    return todo

def scale_one(size, smooth, source_image, target_image):
    old_image = Image.from_file(source_image)
    if old_image.width <= size and old_image.height <= size:
        old_image.save(target_image)
        return Result(1, 0, target_image)
    else:
        if smooth:
            scale = min(size / old_image.width, size / old_image.height)
            new_image = old_image.scale(scale)
        else:
            stride = int(math.ceil(max(old_image.width / size,
                                        old_image.height / size)))
            new_image = old_image.subsample(stride)
        new_image.save(target_image)
        return Result(0, 1, target_image)


def summarize(summary, concurrency):
    message = "copied {} scaled {}".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {}".format(concurrency)
    message += "using {} processes".format(concurrency)
    if summary.canceled:
        message += " [canceled]"
        report(message)
        print()


def main():
    size, smooth, source, target, concurrency = handle_commandline()
    report("starting...")
    summary = scale(size, smooth, source, target, concurrency)
    summarize(summary, concurrency)

if __name__ == "__main__":
    main()

