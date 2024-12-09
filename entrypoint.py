"""
    Gunicorn should only need 4-12 worker processes to handle hundreds or thousands of requests per second.
    Gunicorn relies on the operating system to provide all of the load balancing when handling requests.
    Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off with.
    
    docs: https://docs.gunicorn.org/en/latest/design.html
"""
import os

cpu_count = os.cpu_count()

print(f"cpu count is {cpu_count}")

if cpu_count == 1:
    WORKERS = 4
else:
    WORKERS = (cpu_count * 2) + 1


# running django
os.system("python3 manage.py migrate --no-input")
os.system("python3 manage.py collectstatic --no-input")
os.system(
    f"gunicorn -k gevent --workers {WORKERS} "
    f"--worker-tmp-dir /dev/shm --chdir config config.wsgi:application "
    f"-b 0.0.0.0:{os.getenv('DJANGO_PORT')}")
