from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Conexão com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

# Abra a planilha pelo nome (troque para o nome da sua planilha real!)
sheet = client.open("CadastrosTeste").sheet1

@app.route("/", methods=["GET", "POST"])
def cadastro():
    # debug: checar caminho do template
    print("templates dir:", os.listdir(os.path.join(os.path.dirname(__file__), "templates")))
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        # Salva no Google Sheets
        sheet.append_row([nome, email])

        return "Cadastro salvo com sucesso!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

