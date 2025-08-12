import os
import sys
import gunicorn.app.wsgiapp as app

if __name__ == "__main__":
    port = os.getenv("PORT", "8000")
    sys.argv[1:] = [
        "--workers", "1",
        "--threads", "2",
        "--timeout", "60",
        "--access-logfile", "-",
        "--bind", f"0.0.0.0:{port}",
        "yana.site_app.wsgi:application",
    ]
    app.run()