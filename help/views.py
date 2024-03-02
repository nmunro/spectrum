from django.shortcuts import render

def overview(request):
    return render(request, "help/index.html", {})

def organisations(request):
    return render(request, "help/organisations.html", {})

def organisations_edit(request):
    return render(request, "help/organisations_edit.html", {})

def events(request):
    return render(request, "help/events.html", {})

def events_add(request):
    return render(request, "help/events_add.html", {})

def events_edit(request):
    return render(request, "help/events_edit.html", {})

def events_delete(request):
    return render(request, "help/events_delete.html", {})

def resources(request):
    return render(request, "help/resources.html", {})

def resources_add(request):
    return render(request, "help/resources_add.html", {})

def resources_edit(request):
    return render(request, "help/resources_edit.html", {})

def resources_delete(request):
    return render(request, "help/resources_delete.html", {})

def locations(request):
    return render(request, "help/locations.html", {})

def locations_add(request):
    return render(request, "help/locations_add.html", {})

def locations_edit(request):
    return render(request, "help/locations_edit.html", {})

def locations_delete(request):
    return render(request, "help/locations_delete.html", {})

def contacts(request):
    return render(request, "help/contacts.html", {})

def contacts_add(request):
    return render(request, "help/contacts_add.html", {})

def contacts_edit(request):
    return render(request, "help/contacts_edit.html", {})

def contacts_delete(request):
    return render(request, "help/contacts_delete.html", {})
