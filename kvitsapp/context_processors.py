from datetime import datetime

def year(request):
    return {
        'gads': datetime.now().year
    }