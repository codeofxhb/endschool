from .forms import Loginform

def login_modal_form(request):
    return {'login_modal_form': Loginform()}