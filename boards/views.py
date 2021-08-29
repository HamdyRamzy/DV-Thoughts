from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import Board, Topic, Post, Like, Badge, Author, Report_topic, Report_user
from accounts.models import Owner
from django.contrib.auth.models import User
from .forms import NewTopicForm, ReplyForm, BasicProfileForm, UserProfileForm, BadgeForm, BoardForm, EditTopicForm, EditPostForm, ReportTopicForm, ReportUserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from notifications.models import Notification


#Render homepage
def home(request):
    boards = Board.objects.all()
    context = {
        'boards':boards,
    }
    return render(request, 'home.html', context)


##Render about 
def about(request):
    owner = Owner.objects.first()
    return render(request, 'about.html', {'owner':owner})


#Render base for admin only
def base(request):
    if not request.user.is_superuser:
        return redirect('home')

    return render(request, 'base.html', {})


#Context processor for dropdow-menu view all boards in navbar
def menu_boards(request):
    boards = Board.objects.all()
    context = {
        'boards':boards,
    }
    return context


#Add new board by admin
def add_board(request):

    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = BoardForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            board = form.save()    
            return redirect('home')

        else:
            return render(request, 'add_board.html',{'form': form})


    else:
        form = BoardForm()
        return render(request, 'add_board.html',{'form': form})    


#Add new badge by admin
def add_badge(request):

    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = BadgeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            badge = form.save()    
            return redirect('badges')

        else:
            return render(request, 'add_board.html',{'form': form})

    else:
        form = BadgeForm()
        return render(request, 'add_badge.html',{'form': form})    


#Delete board by admin
@login_required
def delete_board(request, board_id):
    if not request.user.is_superuser:
        return redirect('home')
    board = get_object_or_404(Board, pk = board_id)
    board.delete()
    return redirect('home')    


#Delete badge by admin
@login_required
def delete_badge(request, badge_id):
    if not request.user.is_superuser:
        return redirect('home')
    badge = get_object_or_404(Badge, pk = badge_id)
    badge.delete()
    return redirect('badges')   


#Edit board by admin
@login_required
def edit_board(request, board_id):
    if not request.user.is_superuser:
        return redirect('home')
    board = get_object_or_404(Board, pk = board_id)
    if request.method == 'POST':
        form = BoardForm(data=request.POST, files=request.FILES, instance=board)
        if form.is_valid():
            form.save()
            return redirect('home')    
        else:
            return render(request, 'edit_board.html', {'form':form})

    else:
        form = BoardForm(instance=board)
            
        return render(request, 'edit_board.html', {'form':form})    
    
#Edit badge by admin
@login_required
def edit_badge(request, badge_id):
    if not request.user.is_superuser:
        return redirect('home')
    badge = get_object_or_404(Badge, pk = badge_id)
    if request.method == 'POST':
        form = BadgeForm(data=request.POST, files=request.FILES, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('badges')    
        else:
            return render(request, 'edit_badge.html', {'form':form})

    else:
        form = BadgeForm(instance=badge)
            
        return render(request, 'edit_badge.html', {'form':form})
   

   
#Edit comment 
@login_required
def edit_comment(request,board_id, topic_id,  post_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id, is_blocked=False)
    board = get_object_or_404(Board, pk=board_id)
    post = get_object_or_404(Post, topic__pk=topic_id, pk=post_id)  
    if request.method == 'POST':
        form = EditPostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.edit_date = timezone.now()
            post.save()
            
            return redirect('topic_content', board_id=topic.board.pk, topic_id=topic.pk)    
        else:
            return render(request, 'edit_comment.html', {'form':form})

    else:
        form = EditPostForm(instance=post)
            
        return render(request, 'edit_comment.html', {'form':form})


#Edit topic
@login_required
def edit_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id, is_blocked=False)
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = EditTopicForm(data=request.POST, files=request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_content', board.pk, topic.pk)    
        else:
            return render(request, 'edit_topic.html', {'form':form})

    else:
        form = EditTopicForm(instance=topic)
            
        return render(request, 'edit_topic.html', {'form':form, 'topic':topic, 'board':board})


#Settings for users
@login_required
def settings(request):
    user= User.objects.get(username=request.user)
    author = request.user.author
    prog = user.author.get_progress

    if request.method == 'POST':
        form2 = BasicProfileForm(data=request.POST, files=request.FILES, instance=author)
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form2.is_valid() and form.is_valid():            
            basic = form2.save(commit=False)
            basic.user = user
            basic.uploaded_date = timezone.now()
            basic.save()
            

            user.save()
                        
            return redirect('settings')
        else:
            
            return render(request, 'settings.html',{'form': form, 'form2':form2, 'prog':prog,} )
            
    else:
        form = BasicProfileForm(instance=author)
        form2 = UserProfileForm(instance=user)
        
        return render(request, 'settings.html',{'form': form, 'form2':form2, 'prog':prog,} )


#User profile view all information and topics 
def user_profile(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    author = Author.objects.filter(user=user).first()
    topics = Topic.objects.filter(created_by_id=user_id, is_blocked=False).order_by('-created_date').annotate(replies=Count('post'))
    comments = Post.objects.filter(created_by_id=user_id)
    tags = Tag.objects.filter(topic__created_by=user).distinct()
    topics_count = topics.count()
    comments_count = comments.count()
    tags_count = tags.count()
    user.author.get_badge
    context = {'author': author,
               'user': user,
               'topics':topics,
               'topics_count':topics_count,
               'comments_count':comments_count,
               'tags_count':tags_count,
               'comments':comments,
               }
    return render(request, 'user_profile.html', context)


#View all topics in selected board
def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics_count = board.topics.filter(is_blocked=False).count()
    users = User.objects.all().count()
    queryset = board.topics.filter(is_blocked=False).order_by('-created_date').annotate(replies=Count('post'))
    #common_tags = Tag.objects.filter(topic__board=board_id).distinct()[:15]
    #common_tags = Topic.tags.most_common()[:15]
    common_tags = Topic.tags.most_common(extra_filters={'topic__board':board})[:15]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 9)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)


    context = {'board':board,
               'topics':topics,
               'users':users,
               'common_tags':common_tags,
               'topics_count':topics_count,}
    return render(request, 'topics.html', context) 

#Get report request from user 
@login_required
def report_topic(request, board_id, topic_id):
    board = get_object_or_404(Board, pk=board_id)
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id, is_blocked=False)
    user_id = request.user.pk
    sender = User.objects.filter(pk=user_id).first()
    topic_reported = Report_topic.objects.filter(topic=topic, sender=sender, user = topic.created_by)
    if request.method == 'POST':
        form = ReportTopicForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            reported_topic = form.save(commit=False)
            reported_topic.sender = sender
            reported_topic.user = topic.created_by
            reported_topic.topic = topic
            reported_topic.save()
            
            return redirect('board_topics', board_id=board.pk )
        else:


            context = {'board':board,
                       'topic':topic,
                       'form':form,}
            return render(request, 'report_topic.html', context)   
    else:
        form = ReportTopicForm() 
        context = {'board':board,
                   'topic':topic,
                   'form':form,
                   'topic_reported':topic_reported}
        return render(request, 'report_topic.html', context)   


@login_required
def report_user(request, user_id):
    from_user = request.user.pk
    sender = User.objects.filter(pk=from_user).first()
    user = User.objects.filter(pk=user_id).first()
    user_reported = Report_user.objects.filter(sender=sender, user=user)
    if request.method == 'POST':
        form = ReportUserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            reported_user = form.save(commit=False)
            reported_user.sender = sender
            reported_user.user = user
            reported_user.save()
            
            return redirect('home')
        else:


            context = {'user':user,
                       'form':form,}
            return render(request, 'report_user.html', context)   
    else:
        form = ReportUserForm() 
        context = {'user':user,
                   'form':form,
                   'user_reported':user_reported}
        return render(request, 'report_user.html', context)   


#Handle search about topics and users
def topics_search(request):
    if request.method == 'GET':
        search_str = request.GET['searchField']
        topics = Topic.objects.filter(subject__icontains = search_str, is_blocked=False).order_by('-created_date').annotate(replies=Count('post'))|Topic.objects.filter(content__icontains = search_str, is_blocked=False).order_by('-created_date').annotate(replies=Count('post'))
        users = User.objects.filter(username__icontains = search_str)
        users_count = users.count()        
        topics_count = topics.count()
        context = {'topics':topics,
                   'users':users,
                   'users_count':users_count,
                   'topics_count':topics_count,
                   'search_str':search_str}

        return render(request, 'topics_search.html', context)


#View all badges and description about it
def badges(request):
    badges = Badge.objects.all()
    context = {
        'badges':badges,}
    
    return render(request, 'badges.html', context)


#View badge description and users who awarded it
def badge(request, badge_id):
    badge = Badge.objects.filter(pk = badge_id).first()
    users = User.objects.filter(author__badge=badge_id)
    users_count = users.count()        
    context = {
        'badge':badge,
        'users':users,
        'users_count':users_count}
    
    return render(request, 'badge.html', context)    


#Open selected topic from related topics
def filter_topics(request, board_id, tag_id):
   board = get_object_or_404(Board, pk=board_id)
   users = User.objects.all().count()
   tag = get_object_or_404(Tag, pk=tag_id)
   queryset = Topic.objects.filter(tags=tag, board=board_id, is_blocked=False).order_by('-created_date').annotate(replies=Count('post'))
   topics_count = board.topics.filter(is_blocked=False).count()
   page = request.GET.get('page', 1)
   paginator = Paginator(queryset, 9)
   try:
       topics = paginator.page(page)
   except PageNotAnInteger:
       topics = paginator.page(1)
   except EmptyPage:
       topics = paginator.page(paginator.num_pages)
   #common_tags = Topic.tags.most_common()[:15]
   #common_tags = Tag.objects.filter(topic__board=board_id).distinct()[:15] 
   common_tags = Topic.tags.most_common(extra_filters={'topic__board':board})[:15]
   context = {'users':users,
            'topics_count':topics_count,
                'tag':tag,
                'board':board,
              'topics':topics,
              'common_tags':common_tags,}
   return render(request, 'topics.html', context)



#Add new topics by users
@login_required
def new_topic(request):
    if request.method == 'POST':
        form = NewTopicForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            form.save_m2m()
            return redirect('topic_content', topic.board.pk, topic.pk )
        else:
            context = {
                   'form':form,}
            return render(request, 'new_topic.html', context)   


    else:
        form = NewTopicForm() 
        context = {
                   'form':form,}
        return render(request, 'new_topic.html', context)   


# view all posts on selected board
def topic_content(request, board_id, topic_id):
    board = get_object_or_404(Board, pk=board_id)
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id, is_blocked=False)
    topic_tags = topic.tags.all()
    #common_tags = Tag.objects.filter(topic__board=board_id).distinct()[:15]
    #common_tags = Topic.tags.most_common(extra_filters={'board':board})[:15]
    common_tags = Topic.tags.most_common(extra_filters={'topic__board':board})[:15]
    related_topics = Topic.objects.filter(tags__in=topic_tags, is_blocked=False).exclude(pk=topic.pk).distinct()[:5]
    topic_owner = (topic.created_by)
    more_topics_from_owner = topic_owner.topics.filter(board=board_id, is_blocked=False).exclude(pk=topic.pk).order_by('?')[:5]
    random_users  =  User.objects.all().distinct().order_by('?')[:5]
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, topic=topic, is_seen=False).update(is_seen=True)
    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key,False):
        topic.views +=1
        topic.save()
        request.session[session_key] = True
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.topic = topic
            sender = request.user
            if sender != topic.created_by: 
                post.add_comment_notification(sender, topic)
            post.save()

            return redirect('topic_content', board_id=topic.board.pk, topic_id=topic.pk )


        else:
  
            context =  {'topic':topic,
                        'form':form,
                        }

            return render(request, 'topic_content.html', context)  

        
    else:
        form = ReplyForm()
        context = {'topic':topic,
                   'topic_owner':topic_owner,
                   'more_topics_from_owner':more_topics_from_owner,
                   'form':form,
                   'topic_tags':topic_tags,
                   'board':board,
                   'related_topics':related_topics,
                   'common_tags':common_tags,
                   'random_users':random_users,}
        return render(request, 'topic_content.html', context)  


#Like topic
@login_required
def like_topic(request, board_id, topic_id):
    board = get_object_or_404(Board, pk=board_id)
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    topic_id =  topic.pk       
    topic_object = topic       
        
    if request.user in topic_object.liked.all():
        topic_object.liked.remove(request.user)
    else:
        topic_object.liked.add(request.user)

    like, created = Like.objects.get_or_create(user=request.user, topic=topic_object)
    sender = like.user
    if sender != topic.created_by: 
        like.add_like_notification(sender, topic)
   

    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
            like.delete_like_notification(sender, topic)
                
        else:  
            like.value = 'Like'

            
    
    topic.save()
    like.save()      

    data = {
        'value':like.value,
        'likes':topic_object.liked.all().count()
    }
    
    return JsonResponse(data, safe=False)
    return redirect('topic_content', board_id=topic.board.pk, topic_id=topic.pk )  



#view topic content wich selected 
def filter_topic_content(request, board_id, topic_id):
    board = get_object_or_404(Board, pk=board_id)
    
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id, is_blocked=False)
    
    topic_tags = topic.tags.all()
    common_tags = Topic.tags.most_common()[:15]
    related_topics = Topic.objects.filter(tags__in=topic_tags, is_blocked=False).exclude(pk=topic.pk).distinct()[:5]
    topic_owner = (topic.created_by)
    more_topics_from_owner = topic_owner.topics.filter(board=board_id, is_blocked=False).exclude(pk=topic.pk)[0:5]
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, topic=topic, is_seen=False).update(is_seen=True)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.topic = topic
            sender = request.user
            if sender != topic.created_by: 
                post.add_comment_notification(sender, topic)
            post.save()
            return redirect('topic_content', board_id=topic.board.pk, topic_id=topic.pk )
        
        else:
        
            context =  {'topic':topic,
                    'form':form}   
            return render(request, 'topic_content.html', context)  
        
    else:
        form = ReplyForm()
        context = {'topic':topic,
                   'topic_owner':topic_owner,
                   'more_topics_from_owner' : more_topics_from_owner,
                   'form':form,
                   'topic_tags':topic_tags,
                   'board':board,
                   'related_topics':related_topics,
                   'common_tags':common_tags,}
        return render(request, 'topic_content.html', context) 


#Delete Comment
@login_required
def delete_comment(request, board_id, topic_id, post_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    board = get_object_or_404(Board, pk=board_id)
    post = get_object_or_404(Post, topic__pk=topic_id, pk=post_id)
    sender = request.user
    post.delete_comment_notification(sender, topic)
    post.delete()
    return redirect('topic_content', board_id=topic.board.pk, topic_id=topic.pk )


#Delete topic
@login_required
def delete_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    board = get_object_or_404(Board, pk=board_id)
    topic.delete()
    return redirect('board_topics', board_id=topic.board.pk)    


#Delete user in settings page
@login_required
def delete_user(request):
    user = User.objects.get(username = request.user)
    user.delete()
    return redirect('signup')


@login_required
def block_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(pk = user_id)
        user.delete()
        return redirect('reported_users')    
    else:
        return redirect('home')  

#View reported topics
@login_required
def reported_topics(request):
    if request.user.is_superuser:
        queryset = Report_topic.objects.all().order_by('-date')
        reported_topics_count = queryset.count()
        checked_reported_topics = Report_topic.objects.filter(is_seen = True).count()
        unchecked_reported_topics = Report_topic.objects.filter(is_seen = False).count()

        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 9)
        try:
            reported_topics = paginator.page(page)
        except PageNotAnInteger:
            reported_topics = paginator.page(1)
        except EmptyPage:
            reported_topics = paginator.page(paginator.num_pages)

        context = {'reported_topics':reported_topics,
         'reported_topics_count':reported_topics_count,
        'checked_reported_topics':checked_reported_topics,
        'unchecked_reported_topics':unchecked_reported_topics,

        }
        
        return render(request, 'reported_topics.html', context)
    else:
        return redirect('home')  



#View reported topics
@login_required
def reported_users(request):
    if request.user.is_superuser:
        queryset = Report_user.objects.all().order_by('-date')
        reported_users_count = queryset.count()
        checked_reported_users = Report_user.objects.filter(is_seen = True).count()
        unchecked_reported_users = Report_user.objects.filter(is_seen = False).count()

        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 9)
        try:
            reported_users = paginator.page(page)
        except PageNotAnInteger:
            reported_users = paginator.page(1)
        except EmptyPage:
            reported_users = paginator.page(paginator.num_pages)

        context = {'checked_reported_users':checked_reported_users,
                   'unchecked_reported_users':unchecked_reported_users,
                   'reported_users':reported_users,
                   'reported_users_count':reported_users_count,
                }       
        
        return render(request, 'reported_users.html', context)
    else:
        return redirect('home')  




#Filter checked topics by admin
@login_required
def seen_reported_topics(request):
    if request.user.is_superuser:
        queryset = Report_topic.objects.filter(is_seen=True).order_by('-date')
        reported_topics_count = Report_topic.objects.filter(is_seen = True).count()
        checked_reported_topics = Report_topic.objects.filter(is_seen = True).count() 
        unchecked_reported_topics = Report_topic.objects.filter(is_seen = False).count()


        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 9)
        try:
            reported_topics = paginator.page(page)
        except PageNotAnInteger:
            reported_topics = paginator.page(1)
        except EmptyPage:
            reported_topics = paginator.page(paginator.num_pages)

        context = {'reported_topics':reported_topics,
         'reported_topics_count':reported_topics_count,
         'checked_reported_topics':checked_reported_topics,
         'unchecked_reported_topics':unchecked_reported_topics
        }    
        
        return render(request, 'reported_topics.html', context)

    else:
        return redirect('home')  



#Filter unchecked topics by admin
@login_required
def unseen_reported_topics(request):
    if request.user.is_superuser:
        queryset = Report_topic.objects.filter(is_seen=False).order_by('-date')
        reported_topics_count = Report_topic.objects.filter(is_seen = False).count()
        unchecked_reported_topics = Report_topic.objects.filter(is_seen = False).count()
        checked_reported_topics = Report_topic.objects.filter(is_seen = True).count() 



        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 9)
        try:
            reported_topics = paginator.page(page)
        except PageNotAnInteger:
            reported_topics = paginator.page(1)
        except EmptyPage:
            reported_topics = paginator.page(paginator.num_pages)

        context = {'reported_topics':reported_topics,
         'reported_topics_count':reported_topics_count,
         'unchecked_reported_topics':unchecked_reported_topics,
         'checked_reported_topics':checked_reported_topics

        }    
        
        return render(request, 'reported_topics.html', context)

    else:
        return redirect('home')  







#Page to take action on selected reported topic
@login_required
def reported_topic(request, reported_topic_id):
    if request.user.is_superuser:
        reported_topic = get_object_or_404(Report_topic, pk=reported_topic_id)
        Report_topic.objects.filter(user=reported_topic.user, sender = reported_topic.sender, topic=reported_topic.topic, is_seen=False).update(is_seen=True)
        
        
        return render(request, 'reported_topic.html', {'reported_topic':reported_topic})



#Function to block user topics by admin
@login_required
def block_topic(request, reported_topic_id):
    if request.user.is_superuser:
        reported_topic = get_object_or_404(Report_topic, pk=reported_topic_id)
        Topic.objects.filter(created_by=reported_topic.user, pk=reported_topic.topic.pk, is_blocked=False).update(is_blocked=True)
        notification = Notification.objects.create(topic=reported_topic.topic, sender=request.user, user=reported_topic.topic.created_by, notification_type=4)

        
        return redirect('reported_topics')


#Function to unblock user topics by admin
@login_required
def unblock_topic(request, reported_topic_id):
    if request.user.is_superuser:
        reported_topic = get_object_or_404(Report_topic, pk=reported_topic_id)
        Topic.objects.filter(created_by=reported_topic.user, pk=reported_topic.topic.pk, is_blocked=True).update(is_blocked=False)
        notification = Notification.objects.filter(topic=reported_topic.topic, sender=request.user, user=reported_topic.topic.created_by, notification_type=4)
        notification.delete()
        
        return redirect('reported_topics')        



#View all reported topics to admin
@login_required
def view_reported_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, is_blocked=True)
    if request.user == topic.created_by:
        if request.user.is_authenticated:
            Notification.objects.filter(user=request.user, topic=topic, is_seen=False).update(is_seen=True)

        
        return render(request, 'view_reported_topic.html', {'topic':topic})

    else:
        return HttpResponseNotFound("404")    