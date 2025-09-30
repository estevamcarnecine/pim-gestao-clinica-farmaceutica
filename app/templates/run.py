# run.py
# Script simples para executar a aplicação Flask.
# MODIF: novo arquivo.

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Desenvolvimento: debug ligado, host localhost
    app.run(debug=True)
