from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic,Answer,UpvoterAnswer,SavedTopic
from .forms import TopicForm, AnswerForm, Upvoter 
from django.views.generic import ListView, DeleteView,DetailView,UpdateView, CreateView
from django.contrib import messages
from django.http import JsonResponse
from taggit.models import Tag
from exam.models import Test
from tutor.models import Tutoring,SavedTutorial
from podcasts.models import Podcast, SavedPodcast
from users.models import UserProfile, User
from book.models import Book, BookCart, BookCartItem
from job.models import Job
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics
   
def about(request):
    return render(request, 'topics/about.html')


@login_required
def saved_all(request):
    saved_topics = SavedTopic.objects.filter(user=request.user).select_related('topic')
    try:
        cart = get_object_or_404(BookCart, user=request.user)
    except: 
        cart = None
    if cart is not None:
        cart_items = BookCartItem.objects.filter(cart=cart)
    else:
        cart_items = None
    saved_podcasts = SavedPodcast.objects.filter(user=request.user).select_related('podcast')
    
    try:
        tutorials = SavedTutorial.objects.filter(user = request.user).select_related('tutorial')
    except:
        tutorials = None

    context = {'saved_topics':saved_topics, 'saved_books':cart_items, 'saved_podcasts':saved_podcasts, 'saved_tutorials':tutorials}
    return render(request, 'topics/saved_items.html', context)



def search_results(request):
    query = request.GET.get('q', '')
    if query:
        topic_results = Topic.objects.filter(Q(topic_title__icontains=query) | Q(topic_body__icontains=query)).distinct()
        book_results = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        tutorial_results = Tutoring.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        podcast_results = Podcast.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        
        test_results = Test.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| Q(question__question_text__icontains=query)).distinct()
        job_results = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        user_results = UserProfile.objects.filter(Q(user__username__icontains=query) | Q(bio__icontains=query)).distinct()
    else:
        topic_results = Podcast.results = user_results = tutorial_results = test_results = job_results = book_results = []
    
    context = {
        'query': query,
        'topic_results': topic_results,
        'podcast_results': podcast_results,
        'user_results': user_results,
        "test_results":test_results,
        "book_results":book_results,
        "tutorial_results":tutorial_results,
        'job_results':job_results
    }
    return render(request, 'topics/search_results.html', context)




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
                Q(topic_category__icontains=query)
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
    if request.user.is_authenticated:
        topic.is_upvoted = Upvoter.objects.filter(user=request.user, topic=topic, vote_type=1).exists()

    for answer in answers:
        if request.user.is_authenticated:
            answer.is_upvoted = UpvoterAnswer.objects.filter(user=request.user, answer=answer, vote_type=1).exists()


    
        
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
    }
    return render(request, 'topics/topic_detail.html', context)


def upvote_topic(request, topic_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    topic = get_object_or_404(Topic, pk=topic_id)
    vote, created = Upvoter.objects.get_or_create(
        topic=topic, 
        user=request.user,
        defaults={'vote_type': 1}
    )

    if not created:
        if vote.vote_type == 1:
            vote.delete()
            is_upvoted = False
        else:
            vote.vote_type = 1
            vote.save()
            is_upvoted = True
    else:
        is_upvoted = True

    upvotes = Upvoter.objects.filter(topic=topic, vote_type=1).count()
    return JsonResponse({
        'upvotes': upvotes, 
        'upvoted': is_upvoted,
    })

def upvote_answer(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    answer = get_object_or_404(Answer, pk=answer_id)
    vote, created = UpvoterAnswer.objects.get_or_create(
        answer=answer, 
        user=request.user,
        defaults={'vote_type': 1}  # Default vote_type when creating a new vote
    )

    if not created:
        if vote.vote_type == 1:
            # If already upvoted, remove the vote
            vote.delete()
            is_upvoted = False
        else:
            # Change from downvote to upvote
            vote.vote_type = 1
            vote.save()
            is_upvoted = True
    else:
        # When creating a new vote, it's already set to upvote by `defaults`
        is_upvoted = True

    answer_upvotes = UpvoterAnswer.objects.filter(answer=answer, vote_type=1).count()
    return JsonResponse({
        'answer_upvotes': answer_upvotes,
        'answer_upvoted': is_upvoted
    })


@login_required
def createTopic(request): 
    
    if request.method =='POST':
        form = TopicForm(request.POST)
        if form.is_valid:
            topic = form.save(commit=False)
            
            topic.topic_author = request.user
            
            
            topic.save() 
            form.save_m2m()
            if not topic.hashtag.exists():
                topic.hashtag.add('general') 
            messages.success(request, 'Topic created successfully')

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

def unauthorized_vote(request):
    
    return redirect('login')


def topic_tag_list(request, tag_slug = None):
    topics = Topic.objects.all().order_by('-topic_pub_date', 'topic_title')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        topic = topics.filter(hashtag__in = [tag])
    context = {'topics':topic}
    return render(request, 'topics/tags.html', context)