from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.http import HttpResponseRedirect,HttpResponse
from polls.models import Question,Choice
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

# needed for verbose style, of course
# from django.template import RequestContext, loader

# def index(request):
#     latest_question_list = Question.objects.order_by('pub_date')[:5]
#
#     # Verbose style
#     # template = loader.get_template('polls/index.html')
#     # context = RequestContext(request,
#     #     {
#     #         'latest_question_list':latest_question_list,
#     #     })
#     # return HttpResponse(template.render(context))
#
#     # shortcut
#     context={'latest_question_list':latest_question_list}
#     return render(request,'polls/index.html',context)
#
# def detail(request, question_id):
#     # Verbose
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404
#
#     # shortcut
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': 'How about making a selection?'
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        return HttpResponse("You're voting on question %s" % question_id)


# Create your views here.
