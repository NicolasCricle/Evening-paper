import sys, os
from flask import request, jsonify
from . import git


@git.route("/reload", methods=["POST"])
def reload():
    os.system("cd /var/www/Evening-paper && git pull")
    os.system("supervisorctl reload")

    return jsonify()

