from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'app_main/index.html'
    extra_context = {'title': 'Главная'}
    

class AboutView(TemplateView):
    template_name = 'app_main/about.html'
    extra_context = {'title': 'О нас'}


class ContactsView(TemplateView):
    template_name = 'app_main/contacts.html'
    extra_context = {'title': 'Контакты'}
    