from django import forms
from .models import Topic, Post, Author, Board, Badge, Report_topic, Report_user
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class NewTopicForm(forms.ModelForm):

    content = forms.CharField(required=True,
         label = 'Add Your Content', 
        widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30})  
        )
    
    class Meta:        
        model=Topic
        fields=['subject', 'topic_picture', 'board', 'content', 'tags', 'time']
        labels = {
            'subject' : 'Add Your Topic',
            'topic_picture' : 'Add picture for topic'
        }
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput', 'name':'tags'})
        }



class EditTopicForm(forms.ModelForm):

    content = forms.CharField(required=True,
         label = 'Add Your Content', 
        widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30})  
        )
    
    class Meta:        
        model=Topic
        fields=['subject', 'topic_picture', 'content', 'time']
        labels = {
            'subject' : 'Add Your Topic',
            'topic_picture' : 'Add picture for topic'
        }






class ReplyForm(forms.ModelForm):
    message = forms.CharField(max_length=400, required=True, label = '',  widget=forms.Textarea(attrs={'style': 'height: 60px;'}))
    class Meta:
        model = Post
        fields=['message']

    

class EditPostForm(forms.ModelForm):
    message = forms.CharField(max_length=400, required=True, label = '',  widget=forms.Textarea(attrs={'style': 'height: 60px;'}))
    class Meta:
        model = Post
        fields=['message']



class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'    


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = '__all__'  
        


class BasicProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=EmojiPickerTextInputAdmin)
    class Meta:
        model = Author
        fields = ['bio','picture', 'skills','work', 'education', 'github', 'facebook']  



class UserProfileForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ['username','email']          


class ReportTopicForm(forms.ModelForm):
    class Meta:
        model = Report_topic
        fields = ['report_type','description']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 60px;'})
        }
                  

class ReportUserForm(forms.ModelForm):
    class Meta:
        model = Report_user
        fields = ['report_type','description']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 60px;'})
        }