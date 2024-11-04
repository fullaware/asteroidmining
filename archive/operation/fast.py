# Start as normal, importing from fasthtml.common
from fasthtml.common import *

# Define a function to generate the HTML for rolling a die
def roll_die(n):
    return Titled(
        P(f"You rolled: {n}"),
        div(id='roll', style='margin-bottom: 10px'),
        br()
    )

# Define a function that generates a random number between 1 and 6 (inclusive)
import random

def roll():
    return random.randint(1, 6)

# Create the main FastHTML app
app = fast_app(
    hdrs=(picolink,),
    ftrs=[('roll', roll)],
    tbls=['roll_table']
)

# Define a route to handle rolling the die and rendering its HTML
@app.route('/')
def index(request):
    n = roll()
    return roll_die(n)