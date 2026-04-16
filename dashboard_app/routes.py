from flask import render_template


def register_routes(server):
    @server.route("/")
    def home():
        return render_template("index.html")

    @server.route("/data-analysis")
    def data_analysis():
        return render_template("data-analysis.html")

    @server.route("/automation")
    def automation():
        return render_template("automation-section.html")

    @server.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @server.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500
