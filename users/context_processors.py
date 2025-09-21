from movie.utils import menu

def get_movie_context(request):
    return {'mainmenu': menu}