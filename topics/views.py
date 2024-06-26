from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic,Answer,UpvoterAnswer
from .forms import TopicForm, AnswerForm, Upvoter 
from django.views.generic import ListView, DeleteView,DetailView,UpdateView, CreateView
from django.contrib import messages
from .models import Topic, SavedTopic
from taggit.models import Tag

            
            
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Topic


def about(request):
    return render(request, 'topics/about.html')



class TopicListView(ListView):
    paginate_by = 10    
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics/home.html'
    
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Topic.objects.filter(
                Q(topic_title__icontains=query) |
                Q(topic_body__icontains=query) |
                Q(topic_hashtag__icontains=query)
            ).order_by("-topic_pub_date", 'topic_title')


        else:
            
            return Topic.objects.order_by('-topic_pub_date', 'topic_title')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['q'] = query
        
        topics = context['topics']

        for topic in topics:
            topic.upvotes = Upvoter.objects.filter(topic=topic, vote_type=1).count()
        return context

    


    

@login_required
def save_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    SavedTopic.objects.get_or_create(user=request.user, topic=topic)
    return redirect('topic-detail', pk=topic_id)

@login_required
def saved_topics_list(request):
    saved_topics = SavedTopic.objects.filter(user=request.user).select_related('topic')
    context = {'saved_topics': saved_topics}
    return render(request, 'topics/saved_topics.html', context)

@login_required
def unsave_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    saved_topic = SavedTopic.objects.filter(user=request.user, topic=topic)
    if saved_topic.exists():
        saved_topic.delete()
    return redirect('topic-detail', pk=topic_id)


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    answers = Answer.objects.filter(topic_parent=topic)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedTopic.objects.filter(user=request.user, topic=topic).exists()
    is_own_topic = request.user.is_authenticated and request.user == topic.topic_author
    
    is_upvoted = False
    if request.user.is_authenticated:
        is_upvoted = Upvoter.objects.filter(user = request.user, topic = topic, vote_type =1).exists()
    
    is_downvoted = False
    if request.user.is_authenticated:
        is_downvoted = Upvoter.objects.filter(user = request.user, topic = topic, vote_type = -1).exists()

    for answer in answers:
        answer.upvotes = answer.votes.filter(vote_type=1).count()
        answer.downvotes = answer.votes.filter(vote_type=-1).count()
    if request.method == 'POST':
        
        form = AnswerForm(request.POST)
        if not request.user.is_authenticated:
               
                return redirect('login')
        if form.is_valid():
            answer = form.save(commit=False)
            answer.topic_parent = topic
            answer.answer_author = request.user
            answer.save()
            return redirect('topic-detail', pk=pk)
    else:
        form = AnswerForm()
    context = {
        'topic': topic,
        'answers': answers,
        'own_topic':is_own_topic, 
        
        'form' : form,
        'is_saved': is_saved,
        'is_upvoted':is_upvoted,
        'is_downvoted':is_downvoted,
        'upvotes': topic.question.filter(vote_type=1).count(),
        'downvotes': topic.question.filter(vote_type=-1).count(),
    }
    return render(request, 'topics/topic_detail.html', context)

@login_required
def createTopic(request):
    
    if request.method =='POST':
        form = TopicForm(request.POST)
        if form.is_valid:
            topic = form.save(commit=False)
            topic.topic_author = request.user
            topic.save() 
            return redirect('/')
    else:
        form = TopicForm()
    context = {'form':form}
    return render(request, 'topics/topic_create.html', context)

@login_required
def updateTopic(request, pk):
    topic = get_object_or_404(Topic, pk = pk, topic_author = request.user)
    if request.method =='POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid:
            form.save() 
            return redirect('/', pk = topic.pk)
    else:
        form = TopicForm(instance=topic)
    context = {'form':form}
    return render(request, 'topics/topic_update.html', context)

@login_required
def updateAnswer(request, pk):
    answer = get_object_or_404(Answer, pk = pk, answer_author = request.user)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('topic-detail', pk=answer.topic_parent.pk)
    else:
        form = AnswerForm(instance=answer)
    context = {'form':form}
    return render(request, 'topics/answer_update.html', context)
        

@login_required
def deleteTopic(request, pk):
    topic = get_object_or_404(Topic, pk = pk, topic_author = request.user)
    if request.method == 'POST':
        topic.delete()
        
        return redirect('/')
    context = {'topic':topic}
    return render(request, 'topics/topic_delete.html', context)


@login_required
def deleteAnswer(request, pk):
    answer = get_object_or_404(Answer, pk = pk, answer_author = request.user)
    alfa = answer.topic_parent
    if request.method == 'POST':
        answer.delete()
        
        return redirect('topic-detail', pk = alfa.pk )

    
    context = {'topic':answer}
    return render(request, 'topics/answer_delete.html', context)
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Topic, Upvoter

def upvote_topic(request, topic_id):
    if not request.user.is_authenticated:
        
        return redirect('login')

    topic = get_object_or_404(Topic, id=topic_id)
    user = request.user

    # Check if the user has already voted on this topic
    vote = Upvoter.objects.filter(topic=topic, user=user).first()

    if vote:
        # If an existing vote is an upvote, remove it (toggle off)
        if vote.vote_type == 1:
            vote.delete()
            
        # If it was a downvote, change it to an upvote
        else:
            vote.vote_type = 1
            vote.save()
            
    else:
        # If no existing vote, create a new upvote
        Upvoter.objects.create(topic=topic, user=user, vote_type=1)
        

    return redirect('topic-detail', pk=topic_id)

def downvote_topic(request, topic_id):
    if not request.user.is_authenticated:
        
        return redirect('login')

    topic = get_object_or_404(Topic, id=topic_id)
    user = request.user

    # Check if the user has already voted on this topic
    vote = Upvoter.objects.filter(topic=topic, user=user).first()

    if vote:
        # If an existing vote is an upvote, remove it (toggle off)
        if vote.vote_type == -1:
            vote.delete()
            
        # If it was a downvote, change it to an upvote
        else:
            vote.vote_type = -1
            vote.save()
            
    else:
        # If no existing vote, create a new upvote
        Upvoter.objects.create(topic=topic, user=user, vote_type=-1)
        

    return redirect('topic-detail', pk=topic_id)

@login_required
def upvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    vote, created = UpvoterAnswer.objects.get_or_create(user=user, answer=answer, defaults={'vote_type':1})
    if not created and vote.vote_type != 1:
        vote.vote_type = 1
        vote.save()   
    return redirect('topic-detail', pk=answer.topic_parent.id)

@login_required
def downvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    vote, created = UpvoterAnswer.objects.get_or_create(user=user, answer=answer, defaults={'vote_type':-1})
    if not created and vote.vote_type != -1:
        vote.vote_type = -1
        vote.save()        
    return redirect('topic-detail', pk=answer.topic_parent.id)

def unauthorized_vote(request):
    
    return redirect('login')

def tag_list(request, tag):
    topics = Topic.objects.filter(topic_hashtag__in = [tag])
    context = {'topics':topics}
    return render(request, 'topics/tags.html', context)
    