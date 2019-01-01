# -*- coding: utf-8 -*-#
import connexion

app = connexion.App(__name__, specification_dir="./api/schema")
app.add_api('swagger.yml')

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=True
    )
