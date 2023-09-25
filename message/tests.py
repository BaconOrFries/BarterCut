from django.test import TestCase, Client
from .models import Conversation, ConversationMessage
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from listing.models import Item, Category
from .form import ConversationMessageForm

class ConversationModelTest(TestCase):
    def test_create_conversation(self):
        item_category = Category.objects.create(name='Test Category')
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        item = Item.objects.create(category=item_category, name='Test Item', description="Test item description", point='5',listed_by=user1)

        conversation = Conversation.objects.create(item=item)
        conversation.members.add(user1, user2)

        self.assertEqual(conversation.item, item)
        self.assertEqual(conversation.members.count(), 2)

    def test_create_conversation_message(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        item_category = Category.objects.create(name='Test Category')
        conversation_item = Item.objects.create(category=item_category, name='Test Item', description="Test item description", point='5', listed_by=user1)
        
        conversation = Conversation.objects.create(item=conversation_item)
        conversation.members.add(user1, user2)
        
        message = ConversationMessage.objects.create(
            conversation=conversation,
            content='Test message',
            created_by=user1
        )

        self.assertEqual(message.conversation, conversation)
        self.assertEqual(message.created_by, user1)

class ConversationMessageFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'content': 'Test message content'
        }
        form = ConversationMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = ConversationMessageForm(data={})
        self.assertFalse(form.is_valid())

class ConversationViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.item_category = Category.objects.create(name='Test Category')
        self.item = Item.objects.create(name='Test Item', description='Description', listed_by=self.user, point='10', category=self.item_category)
        self.client.force_login(self.user)

    def test_new_conversation_view(self):
        # Create a user who is different from self.user
        other_user = User.objects.create(username='otheruser', password='testpassword2')

        # Create an item listed by other_user
        other_item = Item.objects.create(name='Other Item', description='Description', listed_by=other_user, point='10', category=self.item_category)

        response = self.client.post(reverse('message:message', args=[other_item.pk]), {
            'content': 'Test message content'
        })

        self.assertEqual(response.status_code, 302)  # Check if the view redirects after a POST request

        # Check if a conversation message was created
        self.assertTrue(ConversationMessage.objects.filter(content='Test message content').exists())  # Use ConversationMessage here

    # Add a new test method for the new_conversation view
    def test_new_conversation_view_with_existing_conversation(self):
        # Create an existing conversation for the user and item
        existing_conversation = Conversation.objects.create(item=self.item)
        existing_conversation.members.add(self.user, self.item.listed_by)

        # Create another user who will be the owner of the second item
        other_user = User.objects.create(username='otheruser', password='testpassword2')

        # Create a second item listed by another user
        other_item = Item.objects.create(name='Other Item', description='Description', listed_by=other_user, point='10', category=self.item_category)

        # Simulate a POST request to create a new conversation
        response = self.client.post(reverse('message:message', args=[other_item.pk]), {
            'content': 'Test message content'
        })

        # Check if the view redirects after a POST request
        self.assertEqual(response.status_code, 302)

        # Check if a conversation message was created
        self.assertTrue(ConversationMessage.objects.filter(content='Test message content').exists())


    def test_inbox_view(self):
        response = self.client.get(reverse('message:inbox'))

        self.assertEqual(response.status_code, 200)  # Check if the inbox page returns a 200 status code
        self.assertContains(response, 'Inbox')  # Check if the response contains expected text
    def test_details_view(self):
        # Create a new conversation
        conversation = Conversation.objects.create(item=self.item)
        conversation.members.add(self.user, self.item.listed_by)

        # Simulate a POST request to the details view
        response = self.client.post(reverse('message:details', args=[conversation.pk]), {
            'content': 'Test message content'
        })

        # Check if the view redirects after a POST request
        self.assertEqual(response.status_code, 302)

        # Check if a conversation message was created
        self.assertTrue(ConversationMessage.objects.filter(content='Test message content').exists())