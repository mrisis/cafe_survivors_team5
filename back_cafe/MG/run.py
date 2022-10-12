from cafe import app, db
from cafe.models import Tables
import signal
import sys


def handle_signal(signum, frame):
    print(f'handling signal {signum}')
    # When we stop the server, we need to set all tables to available
    tables = Tables.query.all()
    for table in tables:
        table.use = False
        db.session.commit()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_signal)

if __name__ == '__main__':
    app.run(debug=True)
