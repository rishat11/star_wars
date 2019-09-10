from django.urls import path
from .views import index, sith_page, recruit_page, questions_page, siths, make_hand_of_shadow, hand_amount, more_than_one_hand

urlpatterns = [
    path('', index, name='index'),
    path('sith', siths, name='sith'),
    path('recruit', recruit_page, name='recruit'),
    path('questions/<int:recruit_id>', questions_page, name='questions'),
    path('sith/<int:sith_id>', sith_page, name='sith_page'),
    path('make_hand_of_shadow/<int:recruit_id>/<int:sith_id>', make_hand_of_shadow, name='make_hand_of_shadow'),
    path('hand_amount', hand_amount, name='hand_amount'),
    path('more_than_one_hand', more_than_one_hand, name='more_than_one_hand'),
]
