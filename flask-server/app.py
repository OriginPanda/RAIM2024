from website import create_app

app = create_app()

# testowanie do react.js 
# @app.route("/members")
# def members():
#     return{"members": ["Member1","Member2","Member3"]}



if __name__ == '__main__':
    app.run(debug=True) #Odświeżenie w trakcie zmian