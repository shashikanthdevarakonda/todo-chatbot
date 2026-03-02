from flask import Flask, render_template, request, jsonify
from services import get_user_summary

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()

    if not message.isdigit():
        return jsonify({
            "reply": "Hmm 🤔 I didn't understand that. Please enter a user number like 1."
        })

    user_id = int(message)

    try:
        summary = get_user_summary(user_id)

        if summary is None:
            return jsonify({
                "reply": f"No todos found for userId {user_id}."
            })

        reply = (
            f"Total: {summary['total']}\n"
            f"Completed: {summary['completed']}\n"
            f"Pending: {summary['pending']}\n"
            f"Completion: {summary['percentage']:.2f}%\n\n"
            "First 5 titles:\n" +
            "\n".join(f"- {title}" for title in summary["titles"])
        )

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "reply": "Sorry, something went wrong while fetching data. Please try again later."
        })

if __name__ == "__main__":
    app.run(debug=True)
