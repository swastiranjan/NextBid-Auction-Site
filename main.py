#this is the file when we want to run our webserver or website

from website import create_app

app = create_app()

if __name__ == '__main__': #this means that if main.py is imported and not run directly, the webserver won't run
    app.run(debug=True)
