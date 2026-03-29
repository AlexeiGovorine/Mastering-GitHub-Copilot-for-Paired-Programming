import os
import random
from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key")

CHOICES = ["rock", "paper", "scissors"]

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { text-align: center; color: #e94560; }
        .game { text-align: center; margin: 30px 0; }
        .btn { display: inline-block; padding: 15px 30px; margin: 10px; font-size: 18px; border: none; border-radius: 8px; cursor: pointer; background: #0f3460; color: #eee; text-decoration: none; }
        .btn:hover { background: #e94560; }
        .result { padding: 20px; margin: 20px 0; border-radius: 8px; font-size: 20px; }
        .win { background: #16813d; }
        .lose { background: #b91c1c; }
        .tie { background: #92400e; }
        .score { text-align: center; font-size: 18px; margin: 20px 0; padding: 15px; background: #16213e; border-radius: 8px; }
        .env-info { text-align: center; font-size: 14px; color: #888; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>{{ app_name }}</h1>
    <p style="text-align:center;">{{ app_description }}</p>
    <div class="score">
        Wins: {{ wins }} | Losses: {{ losses }} | Ties: {{ ties }} | Rounds: {{ rounds }}
    </div>
    {% if result %}
    <div class="result {{ result_class }}">
        <p>You chose: <strong>{{ player_choice }}</strong></p>
        <p>Computer chose: <strong>{{ computer_choice }}</strong></p>
        <p><strong>{{ result }}</strong></p>
    </div>
    {% endif %}
    <div class="game">
        <p>Choose your move:</p>
        <a class="btn" href="/?choice=rock">🪨 Rock</a>
        <a class="btn" href="/?choice=paper">📄 Paper</a>
        <a class="btn" href="/?choice=scissors">✂️ Scissors</a>
    </div>
    <div class="game">
        <a class="btn" href="/reset" style="background:#333;font-size:14px;">Reset Score</a>
    </div>
    <div class="env-info">
        Environment: {{ environment }}
    </div>
</body>
</html>
"""


def determine_winner(player, computer):
    if player == computer:
        return "tie"
    if (player == "rock" and computer == "scissors") or \
       (player == "scissors" and computer == "paper") or \
       (player == "paper" and computer == "rock"):
        return "win"
    return "lose"


@app.route("/")
def index():
    player_choice = request.args.get("choice", "").lower()
    result = None
    result_class = ""
    computer_choice = ""

    if player_choice in CHOICES:
        computer_choice = random.choice(CHOICES)
        outcome = determine_winner(player_choice, computer_choice)

        session.setdefault("wins", 0)
        session.setdefault("losses", 0)
        session.setdefault("ties", 0)
        session.setdefault("rounds", 0)
        session["rounds"] += 1

        if outcome == "win":
            result = "You win!"
            result_class = "win"
            session["wins"] += 1
        elif outcome == "lose":
            result = "You lose!"
            result_class = "lose"
            session["losses"] += 1
        else:
            result = "It's a tie!"
            result_class = "tie"
            session["ties"] += 1

    return render_template_string(
        TEMPLATE,
        app_name=os.environ.get("APP_NAME", "Rock Paper Scissors"),
        app_description=os.environ.get("APP_DESCRIPTION", "A classic mini-game built with Flask & GitHub Copilot"),
        environment=os.environ.get("FLASK_ENV", "production"),
        wins=session.get("wins", 0),
        losses=session.get("losses", 0),
        ties=session.get("ties", 0),
        rounds=session.get("rounds", 0),
        result=result,
        result_class=result_class,
        player_choice=player_choice,
        computer_choice=computer_choice,
    )


@app.route("/reset")
def reset():
    session.clear()
    return '<meta http-equiv="refresh" content="0;url=/">'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
