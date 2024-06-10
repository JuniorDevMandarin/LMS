import form as form
import stripe
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from school_app.models import Categories, Course, Level, Video, UserCourse, Payment, SubscribedUsers, Comment, Comment_video_lecture, BlogPost
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib.auth import get_user_model
from school_app.decorators import user_is_superuser
from django.core.mail import EmailMessage
from time import time
from school_app.forms import NewsletterForm
from django.utils.translation import activate, deactivate
from django.core.mail import send_mail
from django.conf import settings

def getLanguageCookie(request):
    lang = request.COOKIES.get('language')
    if lang is None:
        lang = request.LANGUAGE_CODE

    return lang


# client = stripe.Client(auth=(STRIPE_PUBLIC_KEY,STRIPE_SECRET_KEY))
customer = stripe.Customer.retrieve(
  id ="cus_OJdMOycmkDToVn",
  api_key="sk_test_51NVsRmGV7zXVbgUXaad1awTOPTdikvzTnk8xdRimrRilEVZoh8MaLDsTXC7fg3OCoP272mK6v4FBTa45W5PQ6Qw200q7nQ6Rsc"
)
def BASE(request):
    from django.utils import translation

    # user_language = 'ru'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    return render(request, 'base.html')


def HOME(request):
    current_lang = {'lang': getLanguageCookie(request)}

    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        comment = request.POST['comment']

        message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nComment: {comment}"

        send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['vitalii.podgornii@gmail.com'],
                  fail_silently=False)


    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')
    blog = BlogPost.objects.all()
    print(blog)
    context = {
        'category': category,
        "course": course,
        'blog': blog,
        'newlan': current_lang['lang'],

    }
    return render(request, 'Main/home.html', context)


def post_detail(request, slug):

    post_id = BlogPost.objects.get(slug=slug)
    context = {
        'post_id': post_id,
    }
    return render(request, 'post/post_detail.html', context)


def SINGLE_COURSE(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
        "category": category,
        'level': level,
        'course': course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count': PaidCourse_count,
        'newlan': current_lang['lang'],
    }
    return render(request, 'Main/single_course.html', context)


def filter_data(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()

    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    context = {
        'course': course,
        'newlan': current_lang['lang'],
    }
    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})


def CONTACT_US(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
        'newlan': current_lang['lang'],
    }
    return render(request, 'Main/contact_us.html', context)


def ABOUT_US(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
        'newlan': current_lang['lang'],
    }
    return render(request, 'Main/about_us.html', context)


def SEARCH_COURSE(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = Categories.get_all_category(Categories)
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)

    context = {
        'course': course,
        'category': category,
        'newlan': current_lang['lang'],
    }
    return render(request, 'search/search.html', context)


def COURSE_DETAILS(request, slug):

        current_lang = {'lang': getLanguageCookie(request)}
        print(current_lang['lang'])
        activate(current_lang['lang'])
    
        category = Categories.get_all_category(Categories)
        time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
        course_id = Course.objects.get(slug = slug)
        
        course = Course.objects.filter(slug=slug)
        c = Course.objects.get(slug=slug)
        comment = Comment.objects.filter(courses=c)
        if course.exists():
            course = course.first()
        else:
            return redirect('404')
        context = {
            'course': course,
            'category': category,
            'time_duration': time_duration,
           
            'comment': comment,
            'newlan': current_lang['lang'],
        }
        if request.method == 'POST':
            review = request.POST['review']
            content = request.POST['content']
            u = request.user
            current_user = User.objects.get(id=u.id)
            user_comment = Comment(courses=c, user=current_user, review_title=review,description=content)
            user_comment.save()
        return render(request, 'course/course_details.html', context)
  

def PAGE_NOT_FOUND(request):
    current_lang = {'lang': getLanguageCookie(request)}

    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
        'newlan': current_lang['lang'],
    }
    return render(request, 'error/404.html', context)




def CHECKOUT(request, slug):
    current_lang = {'lang': getLanguageCookie(request)}

    if request.method == "POST":

        course = Course.objects.get(slug=slug)
        print(course.featured_image.url)

        img = course.featured_image.url
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": course.stripe_price_id,
                    "quantity": 1,
                    # "images": [img],

                },
            ],

            custom_fields=[
                {
                    "key": "engraving",
                    "label": {"type": "custom", "custom": "Full Name"},
                    "type": "text",
                },
            ],

            mode="payment",
            success_url='http://127.0.0.1:8000' + f'/success/{course.slug}',
            cancel_url='http://127.0.0.1:8000' + '/cancel',
        )
        return redirect(checkout_session.url, code=303)
    else:

        course = Course.objects.get(slug=slug)
        action = request.GET.get('action')
        order = None
        if course.price == 0:
            course = UserCourse(
                user=request.user,
                course=course,
            )
            course.save()
            messages.success(request, 'Course Are Successfully Enrolled!')
            return redirect('my_course')
        elif action == "{% url 'checkout' %}":
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                first_name = request.POST.get('first_name')
                country = request.POST.get('country')
                address_1 = request.POST.get('address_1')
                address_2 = request.POST.get('address_2')
                city = request.POST.get('city')
                state = request.POST.get('state')
                postcode = request.POST.get('postcode')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                order_comments = request.POST.get('order_comments')

                amount = course.price
                currency = 'USD'
                notes = {
                    'name': f'{first_name} {last_name}',
                    'country': country,
                    'address': f'{address_1} {address_2}',
                    'city': city,
                    'state': state,
                    "postcode": postcode,
                    'phone': phone,
                    'email': email,
                    'order_comments': order_comments,
                }
                receipt = f'Skola-{int(time())}'
                order = customer.order.create (
                    {
                        'receipt': receipt,
                        'notes': notes,
                        'amount': amount,
                        'currency': currency,
                    }
                )
                payment = Payment(
                    course=course,
                    user=request.user,
                    order_id = order.get('id')
                )
                payment.save()
        context = {
            'course': course,
            'order': order,
            's': slug,
            'id': id,
            'newlan': current_lang['lang'],
        }
        return render(request, 'checkout/checkout-page.html', context)


def MY_COURSE(request):
    current_lang = {'lang': getLanguageCookie(request)}

    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course': course,
        'newlan': current_lang['lang'],
    }

    return render(request, 'course/my-course.html', context)


# stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = 'sk_test_51NVsRmGV7zXVbgUXaad1awTOPTdikvzTnk8xdRimrRilEVZoh8MaLDsTXC7fg3OCoP272mK6v4FBTa45W5PQ6Qw200q7nQ6Rsc'




def success_page(request,slug):
    current_lang = {'lang': getLanguageCookie(request)}

    course = Course.objects.get(slug=slug)
    print(course.slug)
    context = {
        'course': course,
        'newlan': current_lang['lang'],
    }
    return render(request, 'checkout/success.html', context)

def cancel_page(request):
    current_lang = {'lang': getLanguageCookie(request)}
    context = {
        'newlan': current_lang['lang'],
    }
    return render(request,'checkout/cancel.html', context)




def WATCH_COURSE(request, slug):
    current_lang = {'lang': getLanguageCookie(request)}
    lecture = request.GET.get('lecture')

    course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)

    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
        video = Video.objects.get(id = lecture)

        if course.exists():
            course = course.first()
        else:
            return redirect('404')
    except UserCourse.DoesNotExist:
        return redirect('404')
    print('hi', lecture)
    v = Video.objects.get(id = lecture)
    comment = Comment_video_lecture.objects.filter(videos=v)
    print(comment)
    context = {
        'course':course,
        'video': video,
        'lecture': lecture,
        'comment': comment,
        'newlan': current_lang['lang'],
    }
    if request.method == 'POST':
        review = request.POST['review']
        content = request.POST['content']
        u = request.user
        current_user = User.objects.get(id=u.id)
        user_comment = Comment_video_lecture(videos=v, user=current_user, review_title=review, description=content)
        user_comment.save()
    return render(request, 'course/watch-course.html', context)


def subscribe(request):
    current_lang = {'lang': getLanguageCookie(request)}
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, 'You must Type logit email to subscribe to a Newsletter')
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f'Found registered user with associated {email}. You must login to subscribe or unsubscribe')
            return redirect(request.META.get("HTTP_REFERER",'/'))

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f' {email} email address is already subscriber.')
            return redirect(request.META.get("HTTP_REFERER",'/'))
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return render(request, 'Main/home.html')



@user_is_superuser
def newsletter(request):
    current_lang = {'lang': getLanguageCookie(request)}
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            mail = EmailMessage(subject, email_message, f"PyLessons <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, 'Email sent succesfully')
            else:
                messages.error(request, 'There was an error sending email')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('newsletter')
    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='Main/newsletter.html', context={'form': form})