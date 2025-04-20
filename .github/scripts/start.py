import sys
import gunicorn.app.wsgiapp as app

if __name__ == "__main__":
    sys.argv[1:] = ["--workers", "1", "--threads", "2", "--timeout", "60", "yana.site_app.wsgi:application"]
    app.run()