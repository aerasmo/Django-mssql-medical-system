# switch for login and logged out
def logged_in_switch_view(logged_in_view, logged_out_view):

    def inner_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return logged_in_view(request, *args, **kwargs)
        return logged_out_view(request, *args, **kwargs)

    return inner_view


def user_switch_view(patient_view, staff_view):

    def inner_view(request, *args, **kwargs):
        if request.session.get("type") == "PATIENT":
            return patient_view(request, *args, **kwargs)
        elif request.session.get("type") == "STAFF":
            return staff_view(request, *args, **kwargs)
        else:
            raise Exception("User type is undefined")

    return inner_view
