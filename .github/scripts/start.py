import sys
import gunicorn.app.wsgiapp as app

if __name__ == "__main__":
    sys.argv[1:] = ["yana.site_app.wsgi:application"]
    app.run()