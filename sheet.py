@app.route('/')
def index():
    sheet_iframe = '''
    <iframe 
      src="https://docs.google.com/spreadsheets/d/1N8yDPDrBog6QxJxRfoaWNolg6qqWPEFmFvgiD2ODph4/edit?usp=sharing" 
      width="100%" 
      height="600" 
      frameborder="0">
    </iframe>
    '''
    return render_template("index.html", sheets_embed=sheet_iframe)
