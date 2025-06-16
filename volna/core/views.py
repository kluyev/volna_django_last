from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from auth_app.models import ParentProfile
from core.models import ContactRequest

@login_required
def parent_profile(request):
    if request.user.role != 'parent':
        return redirect('/')
    
    if request.method == 'POST':
        # Сохраняем телефон в User
        request.user.phone = request.POST.get('phone', '')
        request.user.save()
        
        # Сохраняем данные ребенка в ParentProfile
        profile = request.user.parentprofile
        profile.child_name = request.POST.get('child_name', '')
        profile.child_age = request.POST.get('child_age', None)
        profile.child_health_notes = request.POST.get('child_health_notes', '')
        profile.save()
        
        return redirect('parent_profile')
    
    return render(request, 'core/parent_profile.html')

def home(request):
    context = {
        'promotions': [
            {
                'title': 'Раннее бронирование',
                'description': 'Скидка 10% при оплате до 1 июня',
                'image': 'promo1.png'
            },
            {
                'title': 'Здоровье без перерыва',
                'description': 'Замораживание абонемента на 1 неделю – бесплатно!',
                'image': 'promo2.png'
            },
            {
                'title': 'Приведи друга – получи скидку',
                'description': '-1000 руб. на следующий абонемент за каждого приведённого друга',
                'image': 'promo3.png'
            },
            {
                'title': 'Скидка 20% на второй абонемент',
                'description': 'Если оформляете программу для двоих детей',
                'image': 'promo4.png'
            },
        ],
        'feedbacks': [
            {
                'name': 'Марина',
                'title': 'Мама Светы (9 лет)',
                'description': "Ребёнок в восторге! Улучшилось общее состояние здоровье, дочка стала более активная и любознательная:)",
                'image': 'mother.png'
            },
            {
                'name': 'Вячеслав',
                'title': 'Папа Вани (7 лет)',
                'description': "Сыну все понравилось, интересная и в тоже время эффективная программа по оздоровлению, приедем еще.",
                'image': 'father.jpg'
            },
            {
                'name': 'Анна',
                'title': 'Мама Кирилла (5 лет)',
                'description': "Очень довольна центром! Кирилл стал крепче, реже болеет. Персонал внимательный, программы эффективные. Рекомендую!",
                'image': 'mother.png'
            },
            {
                'name': 'Дмитрий',
                'title': 'Папа Софии (6 лет)',
                'description': "Отличный центр! София с радостью ходит на занятия. Заметно улучшился иммунитет. Спасибо за профессиональный подход!",
                'image': 'father.jpg'
            },
            {
                'name': 'Ольга',
                'title': 'Мама Артема (9 лет)',
                'description': "Артем стал активнее и здоровее. Нравится индивидуальный подход и доброжелательная атмосфера. Очень благодарны!",
                'image': 'mother.png'
            },
            {
                'name': 'Игорь',
                'title': 'Папа Алисы (7 лет)',
                'description': "После курса в центре Алиса реже простужается. Занятия интересные, врачи грамотные. Однозначно советую другим родителям!",
                'image': 'father.jpg'
            },
        ],
        'advantages': [
            {'title': 'Безопасность', 'icon': 'shield', 'text': 'Круглосуточная охрана и медпункт'},
            {'title': 'Питание', 'icon': 'egg-fried', 'text': '5-разовое сбалансированное меню'},
            {'title': 'Здоровье', 'icon': 'heart', 'text': 'Оздоровительные и творческе занятия'},
        ]
    }
    return render(request, 'core/home.html', context)

def about(request):
    context = {
        'history': {
            'title': 'Наша история',
            'years': [
                {'year': '2010', 'event': 'Основание центра с 2 корпусами на берегу озера'},
                {'year': '2015', 'event': 'Реконструкция и расширение до 5 корпусов'},
                {'year': '2020', 'event': 'Открытие современного спортивного комплекса'},
                {'year': '2023', 'event': 'Сертификация по международным стандартам безопасности'}
            ],
            'achievements': [
                'Победитель конкурса "Лучший детский центр-2022"',
                'Экологический сертификат "Зеленый стандарт"',
                '100% безопасность за все годы работы',
                'Премия "Инновации в реабилитации-2023"'
            ]
        },
        'mission': {
            'title': 'Наша философия',
            'principles': [
                {'icon': 'emoji-smile', 'title': 'Счастье детей', 'text': '95% ребят возвращаются к нам снова'},
                {'icon': 'people-fill', 'title': 'Команда мечты', 'text': 'Педагоги с 10+ летним опытом'},
                {'icon': 'award-fill', 'title': 'Проверено временем', 'text': '13 лет успешной работы'},
                {'icon': 'house-heart', 'title': 'Домашняя атмосфера', 'text': 'Уютные корпуса с дизайном для детей'}
            ],
            'goal': 'Наша цель — создать пространство, где дети укрепляют здоровье, раскрывают таланты и учатся дружить.'
        },
        'team': [
            {'name': 'Анна Петрова', 'role': 'Директор', 'photo': 'team1.jpg', 'quote': 'Работаю с детьми 15 лет. Для меня важно, чтобы каждый ребенок чувствовал себя как дома.'},
            {'name': 'Иван Сидоров', 'role': 'Педагог-организатор', 'photo': 'team2.jpg', 'quote': 'Разрабатываю программы, которые делают отдых полезным и увлекательным.'},
            {'name': 'Мария Козлова', 'role': 'Врач-педиатр', 'photo': 'team3.jpg', 'quote': 'Контролирую здоровье детей и составляю индивидуальные оздоровительные планы.'},
        ]
    }
    return render(request, 'core/about.html', context)

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        ContactRequest.objects.create(
            name=name,
            phone=phone,
            email=email
        )
        
        return render(request, 'core/contacts.html', {'success': True})

    return render(request, 'core/contacts.html', {
        'contacts': {
            'address': 'г. Екатеринбург, ул. Шпинева, 62',
            'phone': '+7 (123) 456-78-90',
            'email': 'info@volna-center.ru',
            'work_hours': 'Пн-Пт: 9:00 - 18:00, Сб: 10:00 - 15:00'
        }
    })
