import random
import string

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    print(result_str)

# string of length 8
get_random_string(8)
get_random_string(8)


from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail as sm

usr = User.objects.get(username=username)
    usr.set_password('12345')
    usr.save()

    res = sm(
        subject = 'Subject here',
        message = 'Here is the message.'+str(password),
        from_email = 'sacheeii.test@gmail.com',
        recipient_list = ['sachh93@gmail.com'],
        fail_silently=False,
    )    

    return HttpResponse(f"Email sent to {res} members")
    #return HttpResponse("Email sent to "+ res +" members")


EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sacheeii.test@gmail.com'
EMAIL_HOST_PASSWORD = 'jqohztuanwdabuiu'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

"mrpaintozi@gmail.com", "izotniaprm"

var strength = 0;
if (password.match(/[a-z]+/)) {
strength += 1;
}
if (password.match(/[A-Z]+/)) {
strength += 1;
}
if (password.match(/[0-9]+/)) {
strength += 1;
}
if (password.match(/[$@#&!]+/)) {
strength += 1;

}

if (password.length < 6) {
display.innerHTML = "minimum number of characters is 6";
}

if (password.length > 12) {
display.innerHTML = "maximum number of characters is 12";
}