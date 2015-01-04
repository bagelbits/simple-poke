from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q

from pokes.models import Poke, User


class IndexView(generic.ListView):
  template_name = 'pokes/index.html'
  context_object_name = 'poke_list'

  def get_queryset(self):
    """
    Return all pokes not including pokes set in the future. Shows all
    """
    return Poke.objects.filter(
        poke_date__lte=timezone.now()
      ).order_by('-poke_date')

class NewUserView(generic.ListView):
  template_name = 'pokes/new_user.html'
  context_object_name = 'user_list'

  def get_queryset(self):
    """
    Return all users.
    """
    return User.objects.order_by('-username')

def add_user(request):
  username = request.POST['username']
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    User.objects.create(username=username)
    return HttpResponseRedirect(reverse('pokes:index'))
  else:
    # Redisplay new user form.
    return render(request, 'pokes/new_user.html', {
      'error_message' : "User already exists.",
      'user_list' : User.objects.order_by('-username'),
    })

# Convert to detail or list view?
def detail(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  poke_list = Poke.objects.filter(Q(send_user__exact=user) | Q(receive_user__exact=user))
  return render(request, 'pokes/detail.html', {'user' : user, 'poke_list' : poke_list})


def create_poke(request, user_id):
  pass