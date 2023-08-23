import argparse
import os
import time
from pathlib import Path
import requests
import threading
import multiprocessing
import asyncio

endtime_asynhr = 0

image_urls = []
with open('images.txt', 'r') as images:
    for image in images.readlines():
        image_urls.append(image.strip())

if not os.path.isdir("images"):
    os.mkdir("images")

def download_image(url):
    image_path = Path('images')
    start_time = time.time()
    response = requests.get(url, stream=True).content
    filename = image_path.joinpath(os.path.basename(url))
    f = open(filename, 'wb')
    f.write(response)
    f.close()
    end_time = time.time() - start_time
    print(f"Downloaded {filename} in {end_time:.2f} seconds")
    return end_time

async def download_image_async(url):
    image_path = Path('images')
    start_time = time.time()
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, {"stream": True})
    filename = image_path.joinpath(os.path.basename(url))
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    end_time = time.time() - start_time
    print(f"Downloaded {filename} in {end_time:.2f} seconds")

def download_images_threading(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=download_image, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end_time = time.time() - start_time
    print(f"Общее время сохранения файлов при многопоточном подходе: {end_time:.2f} seconds")
    return end_time

def download_images_multiprocessing(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_image, args=(url,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    end_time = time.time() - start_time
    print(f"Общее время сохранения файлов при мультипроцессорном подходе: {end_time:.2f} seconds")
    return end_time

async def download_images_asyncio(urls):
    global endtime_asynhr
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_image_async(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time() - start_time
    print(f"Total time using asyncio: {end_time:.2f} seconds")
    endtime_asynhr = end_time



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download images from URLs and save them to disk.")
    parser.add_argument("--urls", nargs="+", help="A list of URLs to download images from.")
    args = parser.parse_args()
    urls = args.urls
    if not urls:
        urls = image_urls


    print(f"Downloading {len(urls)} images using synhr...")
    endtime_synhr = download_images_synhr(urls)

    print(f"Downloading {len(urls)} images using threading...")
    endtime_thread = download_images_threading(urls)                                

    print(f"\nDownloading {len(urls)} images using multiprocessing...")
    end_time_procces = download_images_multiprocessing(urls)                          

    print(f"\nDownloading {len(urls)} images using asyncio...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images_asyncio(urls))

    endtime_list = sorted([(endtime_thread, 'Thread'), (endtime_synhr, 'synhr'), ( end_time_procces, 'Process'), (endtime_asynhr, 'asynhr')])
    print ('\nВРЕМЯ ОБРАБОТКИ КОДА ПРИ РАЗЛИЧНЫХ ПОДХОДАХ: ')
    for item in endtime_list:
        print(item)

