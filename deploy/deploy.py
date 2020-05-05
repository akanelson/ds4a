from flask import Flask, request
import git

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/var/www/practicum/')
        origin = repo.remotes.origin
        origin.pull()
        return 'Update successfully', 200
    else:
        return 'Wrong event type', 400