from datetime import datetime

def today(request):
    """
    Adds today's date to the template context as 'today'.
    """
    return {'today': datetime.now().strftime('%A %B %d, %Y')}

