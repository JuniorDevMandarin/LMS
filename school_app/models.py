from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField
class Categories(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('id')


class Author(models.Model):
    author_profile = models.ImageField(upload_to='Media/author')
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    data = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=900, null=True)
    image = models.ImageField(upload_to="Media/post_image", null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={'slug': self.slug})





class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language



class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = CloudinaryField('image')
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    Deadline = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    Certificate = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

class Comment(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_title = models.CharField(max_length=500, blank=True, default="")
    description = models.TextField(max_length=2000, blank=True, default="")

    def __str__(self):
        return self.user







def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Course)


class What_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='Media/YT_Thumbnail', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    description = RichTextUploadingField(blank=True, null=True)
    description2 = RichTextUploadingField(blank=True, null=True, config_name='special')
    code = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment_video_lecture(models.Model):
    videos = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_title = models.CharField(max_length=500, blank=True, default="")
    description = models.TextField(max_length=2000, blank=True, default="")

    def __str__(self):
        return self.review_title





class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title


class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title


class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email