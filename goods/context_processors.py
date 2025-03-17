from .forms import GoodsSearchForm


def search_form(request):
    return {'search_form': GoodsSearchForm()}
