from cafe import app, db

# from cafe.models import Tables
# import atexit

if __name__ == '__main__':
    app.run(debug=True)

    # def exit_handler():
    #     tables = Tables.query.all()
    #     for table in tables:
    #         table.use = False
    #         db.session.commit()
    #
    #
    # atexit.register(exit_handler)
