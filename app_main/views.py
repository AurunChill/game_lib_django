from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib import messages

# Project
import app_main.forms as forms


class IndexView(TemplateView):
    template_name = 'app_main/index.html'
    extra_context = {'title': 'Главная'}
    

class AboutView(TemplateView):
    template_name = 'app_main/about.html'
    extra_context = {'title': 'О нас'}


class ContactsView(FormView):
    form_class = forms.SendMessageForm
    template_name = 'app_main/contacts.html'
    success_url = reverse_lazy('games:catalog')

    def form_valid(self, form):
        user = self.request.user
        if not user.is_authenticated:
            messages.add_message(self.request, messages.INFO, 'Зарегистрируйтесь, чтобы отправить нам сообщение!')
            return redirect(reverse('users:login'))
        
        subject = form.cleaned_data['name'] + ' отправил сообщение'
        contact_email = form.cleaned_data['contact_email']
        message = form.cleaned_data['message'] + '\n\nПочта отправщика: ' + contact_email
        recipient_list = [settings. EMAIL_HOST_USER]
        try:
            send_mail(
                    subject=subject, 
                    message=message, 
                    from_email=user.email, 
                    recipient_list=recipient_list, 
                    fail_silently=False
            )
        except Exception as e:
            print('Send email error!', e)
            messages.add_message(self.request, messages.ERROR, 'Ошибка отправления. Вы уверены, что почта вашего аккаунта правильная?')
            return redirect('main:contacts')

        messages.add_message(self.request, messages.INFO, 'Вы успешно отправили письмо!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        if self.request.method == 'POST':
            context['form'] = forms.SendMessageForm(self.request.POST)
        else:
            context['form'] = forms.SendMessageForm()
        return context 