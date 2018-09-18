## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
# I worked with Joseph Stempel on question number three. He helped me by showing me that I needed to alter my import requests. 


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, render_template, request
import json
import requests
app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return 'Welcome to SI 364!'





## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 
#'http://localhost:5000/movie/<name-of-movie-here-one-word>' 
#you see a big dictionary of data on the page. For example, 
#if you go to the URL 'http://localhost:5000/movie/ratatouille', 
#you should see something like the data shown in the included file 
#sample_ratatouille_data.txt, which contains data about the 
#animated movie Ratatouille. However, if you go to the url 
#http://localhost:5000/movie/titanic, you should get different data, and 
#if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' 
#for example, you should see data on the page that looks like this:
# {
#  "resultCount":0,
#  "results": []
# }
@app.route('/movie/<title_of_movie>')
def what_movie(title_of_movie):
    base_url = 'https://itunes.apple.com/search'
    param_dict = {}
    param_dict['term'] = title_of_movie
    resp = requests.get(base_url, params = param_dict)
    txt = resp.text
    obj = json.loads(txt)
    return str(obj)

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL 
##http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says 
#"Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says 
##"Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def formView():
    html_form = '''
    <html>
    <body>
    <form action = "/result" method = "GET">
        Enter Your Favorite Number: <input type = "number" name = "favorite number"><br>
        <input type = "submit" value = "Submit">
    </form>
    </body>
    </html>
    '''
    return html_form

@app.route('/result', methods=['GET','POST'])
def secondPage():
    if request.method == "GET":
        integer = request.args.get("favorite number")
    dub = int(integer)*2
    return "Double your favorite number is {}".format(str(dub))



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
OMDB_API_KEY = '88dfac0f'

@app.route('/problem4form', methods=["GET","POST"])
def mediaSearch():
    my_html_form_pt1 = '''
    <html>
    <body>
    <form method = "POST" action = '/problem4form'>
        <label> Please enter the title of a movie:</label><br>
        <input type='text' name='title'</input>
        <br> Do you want the movie's plot or IMDB rating? </br>
        <input type='radio' name="RatingSystem" value="Plot">Movie's Plot</input><br>
        <input type='radio' name='RatingSystem' value="IMDB">IMDB Rating</input><br>
        <input type='submit' name='submit'></input>
    </form>'''

    my_html_form_pt2 = '''
    </body>
    </html>
    '''
    
    OMDB_API_KEY = '88dfac0f'
    if request.method =="POST":
        movie_title = request.form.get('title')
        movie_rating = request.form.get('RatingSystem')
        OMDB_base_url = 'http://www.omdbapi.com/'
        resp1 = requests.get(OMDB_base_url, params={'apikey': OMDB_API_KEY, 't': movie_title})
        obj1 = json.loads(resp1.text)

        if movie_rating == "IMDB":
            return my_html_form_pt1 + "The IMDB rating of " + movie_title + " is " + (obj1['Ratings'][0]['Value']) + my_html_form_pt2
        if movie_rating == "Plot":
            return my_html_form_pt1 + f"The plot of {movie_title} is {obj1['Plot']}" + my_html_form_pt2
    else:
        return my_html_form_pt1 + my_html_form_pt2

        


    #     # <fieldset>
    #         <legend>Which of the following would you like to search for?</legend>
    #         <input type = 'checkbox' name = 'media' value = 'movie'> Movie <br>
    #         <input type = 'checkbox' name = 'media' value = 'show'> TV Show <br>
    #     </fieldset><br>
    #     <input type = "submit" value = "Submit"
    # </form>
    # </body>
    # </html>
    # '''

    # if request.method == "POST":
    #     medias = request.values.get("media")
    #     terms = request.values.get("term")
    #     base_url = 'https://itunes.apple.com/search'
    #     params_dict = {}
    #     params_dict['media'] = medias
    #     params_dict['term'] = terms
    #     r = requests.get(base_url, params = params_dict)
    #     objs = json.loads(r.text)
    #     results = "<h1>The top results are as follows:\n\n</h1>"
    #     for x in objs['results']:
    #         song_artist = x['artistName']
    #         song_name = x['trackName']
    #         format = "{} by {}<br>".format(song_name, song_artist)
    #         results += format
    #     return my_html_form + results

    # else:
    #     return my_html_form


if __name__ == '__main__':
    app.run()