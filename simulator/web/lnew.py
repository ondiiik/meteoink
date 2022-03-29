from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Add new location'))

    with page.form('nloc') as form:
        form.input(trn('Location name'),   'name')
        form.input(trn('GPS coordinates'), 'gps')
