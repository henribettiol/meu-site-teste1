from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json

app = Flask(__name__)

# Conexão com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Se estiver no Render, pega da variável de ambiente GOOGLE_CREDENTIALS
if os.getenv("GOOGLE_CREDENTIALS"):
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    # Local: usa o arquivo credenciais.json
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)

client = gspread.authorize(creds)

# Abre a planilha (troque "CadastrosTeste" pelo nome da sua planilha real!)
sheet = client.open("CadastrosTeste").sheet1

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        # Salva no Google Sheets
        sheet.append_row([nome, email])

        return "Cadastro salvo com sucesso!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


