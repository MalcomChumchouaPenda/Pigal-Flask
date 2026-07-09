
from flask import Flask, request, url_for
from flask.views import View


app = Flask(__file__)


class DemoView(View):
    def dispatch_request(self, **params):
        return {
            'params':params,
            'path':request.path,
            'rule':request.url_rule.rule,
            'view': url_for('solve')
        }
                


view_func = DemoView.as_view("solve")
app.add_url_rule("/", view_func=view_func)
app.add_url_rule("/demo/12", view_func=view_func)
app.add_url_rule("/demo/<int:a>", view_func=view_func)
app.add_url_rule("/demo/13", view_func=view_func)
app.add_url_rule("/<path:path>", view_func=view_func)

print({r.rule:r for r in app.url_map.iter_rules()})

if __name__ == '__main__':
    app.run(debug=True)