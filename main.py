import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)

'''
______________________________________________
from here my code starts 
'''

def get_coordinate(dic):
    ''' 
    dictinary -> integer tuple
    get's a dic of the form {"y": a, "x": b} and
    returns a tuple of the form (a,b)
    '''
    
    return (dic['y'],dic['x'])

def get_coordinates (coordinate_dic_list):
    '''
    list of dictionarys -> coordinate_list
    '''
    tuple_list = [];
    for a in coordinate_dic_list:
        tuple_list.append(get_coordinate(a))
    
    return tuple_list



def get_coordinates_my_snake(data):
    ''' 
    json_Data -> coordinates_list
    '''
    return get_coordinates(data['you']['body'] )



def get_head_my_snake(data):
    '''
    jsondata -> coordinate (integer tuple)
    expects data as in json and returns head of snake that is last in dic"
    '''
    return get_coordinates_my_snake(data)[0];



def get_all_snakes(data): ##currently is getting all snakes!!!
    '''
    json_data->coordinates_list
    '''
    data = data['board']['snakes']
    index = len(data)
    temp=[]
    for a in range(index):
        temp2=get_coordinates(data[a]['body'])
        for b in temp2:
            temp.append(b)
    
    return temp

def get_all_snakes_without_tails(data):
    '''
    json_data->coordinate_list
    '''
    data = data['board']['snakes']
    index = len(data)
    temp=[]
    for a in range(index):
        temp2=get_coordinates(data[a]['body'])
        temp2.pop(-1)
        for b in temp2:
            temp.append(b)
    
    return temp
    


def is_no_wall(coordinate, field_size):     
    '''
    integer tuple, integer -> boolean
    yes if a coordinate is no wall (-1 <  coordinates < field_size)
    '''
    first = (coordinate[1] < field_size) and (coordinate[0] < field_size)
    second = (coordinate[1] > -1) and (coordinate [0] > -1)
    
    return first and second


def move_to(coordinate, direction):
    '''
    coordinate, string -> coordinate
    '''
    if direction == 'up':
        return (coordinate[0]-1,coordinate[1])
    if direction == 'down':
        return (coordinate[0]+1,coordinate[1])
    if direction == 'left':
        return (coordinate[0],coordinate[1]-1)
    if direction == 'right':
        return (coordinate[0],coordinate[1]+1)
    
    return coordinate


def moves_that_do_not_kill_you(data, size_board):
    '''
    data -> list of moves
    '''
    pos_moves=[]
    head = get_head_my_snake(data)
    snakes = get_all_snakes_without_tails(data)
    
    
    if is_no_wall(move_to(head, 'up'),size_board):
        if not (move_to(head, 'up') in snakes):
            pos_moves.append('up')
            
    if is_no_wall(move_to(head, 'down'),size_board):
        if not (move_to(head, 'down') in snakes):
            pos_moves.append('down')
            
    if is_no_wall(move_to(head, 'right'),size_board):
        if not (move_to(head, 'right') in snakes):
            pos_moves.append('right')
            
    if is_no_wall(move_to(head, 'left'),size_board):
        if not (move_to(head, 'left') in snakes):
            pos_moves.append('left')
            
        
    return pos_moves



#to do: build function that finds deadly stuff around and returns
# options that do not kill you
    
STANDARD_SIZE = 15 ##Standard board size

@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    
    

    directions = moves_that_do_not_kill_you(data, STANDARD_SIZE)
    if len(directions)==0:
        directions = ['left', 'right', 'up','down']
    direction = random.choice(directions)
    

    return move_response(direction)


'''
______________________________________________
here (for now) edited code ends
'''

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))


    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
