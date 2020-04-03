from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('login/', views.login, name = 'login'),
   path('login_post/', views.login_post, name = 'login_post'),
#   path('logout/',views.logout, name = 'logout'),
   path('register/', views.register, name = 'register'),
#   path('register_post/',views.register.post,name = 'register_post')
   path('dashboard/', views.dashboard, name = 'dashboard'),
   path('allocate/', views.allocate, name = 'allocate'),
 #  path('allocate_post/',views.allocate_post,name='allocate_post'),
#   path('swap_req/',views.swap_req,name = 'swap_request'),
#   path('swap/',views.swap),
#   path('swap_req_show/',views.swap_req_show),
#   path('roommate_req/',views.roommate_req),
#   path('roommate_acpt/',views.roommate),
#   path('end/',views.end),
#   path('check_vacancy/',views.vacancy),
#   path('show_student/',views.show_student),
#   path('show_room/',views.show_room),
#   path('show_swap_warden/',views.show_swap_warden),
#   path('warden_links/', views.warden_links, name = 'warden_links'),
]
