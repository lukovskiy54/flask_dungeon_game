from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import NumberRange, DataRequired
from config import Config


class playerForm(FlaskForm):
    way = SelectField(
        'Choose the side of the world you wish to move to.',
        coerce=int,
        choices=[
        (0, 'North'),
        (1, 'East'),
        (2, 'South'),
        (3, 'West')],
        render_kw={'class': 'form-control'}
    )
    number_steps = IntegerField(
    'How far you want to move?',
    validators=[NumberRange(min=1), DataRequired()],
    default=1, render_kw={
    'class': 'form-control'
    },
    )
    submit = SubmitField("Let's go!")

class Room():
    def __init__(self,name, north, south, west, east):
        self.name = name
        self.neigh = {
            "north" : north,
            "west" : west,
            "east" : east,
            "south" : south
        }
    def getName(self):
        return self.name
    
        
bedroom = Room("bedroom", None, "dungeon", None, "hall")
hall = Room("hall", "balcony", "corridor", "bedroom", 'kitchen')
balcony = Room("balcony",None, "hall", None, None)
kitchen = Room('kitchen',None, "armory", "hall", None)
dungeon = Room('dungeon', 'bedroom', None, None, 'corridor')
corridor = Room('corridor', 'hall', None, 'dungeon', 'armory')
armory = Room('armory', 'kitchen',None, 'corridor', None )
map = [bedroom,hall,balcony,kitchen,dungeon,corridor,armory]

class Player():
    def __init__(self, map):
        self.map = map
        self.current = dungeon
        self.goal = 'balcony'
        self.canMove= 1
    def move(self, direction, steps):
        for i in range(steps):
            if self.findDir(direction) != None:
                self.current = self.findDir(direction)
                self.canMove = 1
            else: 
                print("Cant move")
                self.canMove = 0
                break
            
    def findDir(self, direction):
        dct = {
            1: self.moveEast,
            3: self.moveWest,
            0: self.moveNorth,
            2: self.moveSouth
        }
        return dct[direction]()
    def moveNorth(self):
        for i in self.map:
            if i.getName() == self.current.neigh["north"]:
                return i
    def moveSouth(self):
        for i in self.map:
            if i.getName() == self.current.neigh["south"]:
                return i
    def moveWest(self):
        for i in self.map:
            if i.getName() == self.current.neigh["west"]:
                return i
    def moveEast(self):
        for i in self.map:
            if i.getName() == self.current.neigh["east"]:
                return i

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')


player = Player(map)

@app.route('/ingame/', methods=['POST', 'GET'])
def ingame():
    form = playerForm()
    if form.validate_on_submit():
        way = form.way.data
        number_steps = form.number_steps.data
        curr = player.current.name
        print(curr)
        player.move(way,number_steps)
        canmove = player.canMove
        print(canmove)
        return render_template('game.html', form = form, way = way, number_steps = number_steps, current = curr, new = player.current.name, canmove= canmove )
    return render_template('game.html', form = form, new = "dungeon" )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000, debug=True)
