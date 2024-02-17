from django.forms import ModelForm
from .models import User, Category, Auction, Bid, Comment


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = (
            'title',
            )
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-2'


class AuctionForm(ModelForm):

    class Meta:
        model = Auction
        fields = (
            'name',
            'price',
            'description',
            'image',
            'category',
            )
        labels = {
            'name': 'Name',
            'price': 'Initial price',
            'description': 'Description',
            'image': 'Image',
            'category': 'Category',
        }
    
    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BidForm(ModelForm):

    class Meta:
        model = Bid
        fields = (
            'bid',
            )
        labels = {
            'bid': 'Bid',
        }
    
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = (
            'comment',
            )
        labels = {
            'comment': 'Comment',
            }
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'