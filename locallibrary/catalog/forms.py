from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import BookInstance
from .models import Author

# from django.utils.translation import ugettext_lazy as _  ДЛЯ ПЕРЕВОДА ТЕКСТА САЙТА
#ф-ия render генерирует HTML запросы




class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату в диапазоне 3 недель ")
 #Функция проверки заполнения данной формы
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date'] #cleaned_ - ("очистка") нормализация до согласованного формата
                                                 #Предупреждение: Важно: Хотя вы также можете получить доступ к данным формы непосредственно через запрос (например request.POST['renewal_date'],
                                                 # или request.GET['renewal_date'] (в случае GET-запроса), это НЕ рекомендуется. Очищенные данные проверены на вредоносность и преобразованы в типы, совместимые с Python.
                                                 # то есть очистка - это удаление неправильных символов, которые потенциально могут использоваться для отправки вредоносного содержимого на сервер
        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError('Некорректная дата, указано прошлое время')

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Некорректная дата, указано больше чем 3 недели')

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data


# Если необходимо иметь много полей, то такой способ построения формы может значительно уменьшить количество кода и ускорить разработку!
class UpdateAuthorForm(ModelForm):
    update_author_name = forms.CharField(max_length=100, help_text="Введите новое имя")
    update_author_last_name = forms.CharField(max_length=100, help_text="Введите новое имя")
    update_author_date_of_death = forms.DateField(help_text="Введите новую дату смерти ")

    def clean_update_author_date_of_death (self):
        data = self.cleaned_data['update_author_date_of_death'] #cleaned_ - ("очистка") нормализация до согласованного формата
                                                 #Предупреждение: Важно: Хотя вы также можете получить доступ к данным формы непосредственно через запрос (например request.POST['renewal_date'],
                                                 # или request.GET['renewal_date'] (в случае GET-запроса), это НЕ рекомендуется. Очищенные данные проверены на вредоносность и преобразованы в типы, совместимые с Python.
                                                 # то есть очистка - это удаление неправильных символов, которые потенциально могут использоваться для отправки вредоносного содержимого на сервер
        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data > datetime.date.today():
            raise ValidationError('Некорректная дата, указано будущее время')
        # Помните, что всегда надо возвращать "очищенные" данные.
        return data
    # Чтобы  добавить валидацию, вы можете  использовать  тот  же  способ как и  для класса Form —
    # вы определяете функцию с  именем clean_field_name()  из которой выбрасываете исключение ValidationError,если  это необходимо.
    # Единственным отличием от нашей оригинальной формы будет  являться  то, что  поле модели  имеет  имя  due_back,а не "renewal_date
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_death']
        labels = {'date_of_death': ('Обновить Дату смерти'),'first_name': ('Обновить Имя'), 'last_name': ('Обновить Фамилию')}  # Переопределяем названия через словарь








class RenewBookModelForm(ModelForm):
    #Чтобы  добавить валидацию, вы можете  использовать  тот  же  способ как и  для класса Form —
    #вы определяете функцию с  именем clean_field_name()  из которой выбрасываете исключение ValidationError,если  это необходимо.
    #Единственным отличием от нашей оригинальной формы будет  являться  то, что  поле модели  имеет  имя  due_back,а не "renewal_date
    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = {'due_back': ('Renewal date'), } # Переопределяем названия через словарь
        help_texts = {'due_back': ('Enter a date between now and 4 weeks (default 3).'), }