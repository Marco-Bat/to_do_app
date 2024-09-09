from website import create_app

app = create_app()#the returned object from create_app with all config

if __name__=="__main__":
    app.run (debug=True, port=8000)

