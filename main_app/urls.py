from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('monsters/', views.monsters_index, name='index'),
    path('monsters/<int:monster_id>/', views.monsters_detail, name='detail'),
    path('monsters/create', views.MonsterCreate.as_view(), name='monsters_create'),
    path('monsters/<int:pk>/update/', views.MonsterUpdate.as_view(), name='monsters_update'),
    path('monsters/<int:pk>/delete/', views.MonsterDelete.as_view(), name='monsters_delete'),
    path('monsters/<int:monster_id>/add_feeding/',
    views.add_feeding, name='add_feeding'),
    path('skills/', views.SkillList.as_view(), name='skills_index'),
    path('skills/<int:pk>/', views.SkillDetail.as_view(), name='skills_detail'),
    path('skills/create/', views.SkillCreate.as_view(), name='skills_create'),
    path('skills/<int:pk>/update/', views.SkillUpdate.as_view(), name='skills_update'),
    path('skills/<int:pk>/delete/', views.SkillDelete.as_view(), name='skills_delete'),
    path('monsters/<int:monster_id>/assoc_skill/<int:skill_id>/',
    views.assoc_skill, name='assoc_skill'),
    path('monsters/<int:monster_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
]
