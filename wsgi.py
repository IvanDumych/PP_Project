from waitress import serve
from pp_project import app

# serve(app, host='0.0.0.0', port=5000)
app.run(debug=True)
