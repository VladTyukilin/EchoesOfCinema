from movie.menu import MENU_ITEMS

def get_movie_context(request):
    return {'mainmenu': MENU_ITEMS}



