from flask import Flask, render_template, jsonify, request, url_for
app=Flask(__name__)

@app.route("/")
def inicio():
    return "Bem-vindo ao Footbal Tactics Lab"


# Routa para a configuração
@app.route("/config", methods=["GET"])
def configuracao():
    return render_template("config.html")


# Routa para informar os parametros a Inven!RA
@app.route("/json-params",methods=["GET"])
def parametros_json():
    parametros=[
        {"name": "tema", "type":"text/plain"},
        {"name":"dificuldade", "type":"text/plain"},
        {"name":"num_cenarios", "type":"text/plain"},
        {"name":"tempo_limite", "type":"text/plain"},
    ]
    return jsonify(parametros)

# Routa de deploy
@app.route("/deploy", methods=["GET"])
def disponibilizar_atividade():
    activity_id=request.args.get("activityID")

    if not activity_id:
        return jsonify({"erro": "Identificador da atividade em falta"}), 400

  #  url_atividade = url_for(
  #      "acesso_atividade",
   #     id=activity_id,
    #    _external=True
   # )
    url_atividade = request.host_url.rstrip("/") + "/atividade?id=" + activity_id

    return url_atividade


#
@app.route("/analytics-list", methods=["GET"])
def lista_analiticas():
    analiticas = {
        "qualAnalytics": [
            {
                "name": "Feedback tático",
                "type": "text/plain"
            },
            {
                "name": "Relatório da atividade",
                "type": "URL"
            }
        ],
        "quantAnalytics": [
            {
                "name": "Pontuação final",
                "type": "integer"
            },
            {
                "name": "Atividade concluída",
                "type": "boolean"
            }
        ]
    }

    return jsonify(analiticas)


@app.route("/analytics", methods=["POST"])
def obter_analiticas():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados.get("activityID"):
        return jsonify({"erro": "Identificador da atividade em falta"}), 400

    resultados = [
        {
            "inveniraStdID": "1001",
            "quantAnalytics": [
                {
                    "name": "Pontuação final",
                    "type": "integer",
                    "value": 80
                },
                {
                    "name": "Atividade concluída",
                    "type": "boolean",
                    "value": True
                }
            ],
            "qualAnalytics": [
                {
                    "name": "Feedback tático",
                    "type": "text/plain",
                    "value": "Boa leitura do cenário ofensivo."
                },
                {
                    "name": "Relatório da atividade",
                    "type": "URL",
                    "value": "https://example.com/relatorios/1001"
                }
            ]
        }
    ]

    return jsonify(resultados)


if __name__ == "__main__":
    app.run(debug=True)