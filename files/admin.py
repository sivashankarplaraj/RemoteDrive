from django.contrib import admin
from .models import User, File, FileVersion, Share

admin.site.register(User)
admin.site.register(File)
admin.site.register(FileVersion)
admin.site.register(Share)
