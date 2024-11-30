from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from adminpanel.models import Profile, Blog, Comment

# Registration Form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_description', 'phone', 'profile_image', 'id_proof']

# Login Form
class LoginForm(AuthenticationForm):
    pass


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image', 'status']
        
    # Optional customization for form widgets (e.g., textarea for content)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your blog content here...'}))

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

# Reset Password Form
class ResetPasswordForm(PasswordChangeForm):
    pass

class BlogFilterForm(forms.Form):
    status_choices = [
        ('', 'All'),
        ('published', 'Published'),
        ('draft', 'Draft'),
    ]
    
    status = forms.ChoiceField(choices=status_choices, required=False)
class DeleteConfirmationForm(forms.Form):
    confirm = forms.BooleanField(
        label="Are you sure you want to delete this blog?",
        required=True
    )
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image']  # Adjust fields as per your Blog model
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'blog_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
    
    # You can also add custom validation for specific fields if needed
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title