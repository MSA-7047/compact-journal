from django.test import TestCase, RequestFactory
from django.urls import reverse
from journal.models import GroupRequest, User
from journal.views.group_management import send_group_request
from journal.forms import SendGroupRequestForm
from unittest.mock import patch

class SendGroupRequestViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='@testuser', email='test@example.com', password='password')
        self.other_user = User.objects.create_user(username='@otheruser', email='other@example.com', password='password')

    def test_send_group_request_get(self):
        """
        Test GET request to send_group_request view.
        """
        request = self.factory.get(reverse('send_group_request'))
        request.user = self.user

        with patch('journal.views.SendGroupRequestForm') as mock_form:
            send_group_request(request)
            mock_form.assert_called_once_with(currentUser=self.user)
            
    def test_send_group_request_post_valid(self):
        """
        Test POST request with valid form data to send_group_request view.
        """
        form_data = {'recipient': self.other_user.pk}
        request = self.factory.post(reverse('send_group_request'), form_data)
        request.user = self.user

        with patch('journal.views.SendGroupRequestForm') as mock_form:
            mock_form_instance = mock_form.return_value
            mock_form_instance.is_valid.return_value = True

            response = send_group_request(request)

            # Check if the group request is created
            self.assertEqual(GroupRequest.objects.count(), 1)
            group_request = GroupRequest.objects.first()
            self.assertEqual(group_request.sender, self.user)
            self.assertEqual(group_request.recipient, self.other_user)

            # Check if the view redirects to the home page
            self.assertRedirects(response, reverse('home'))
    
    def test_send_group_request_post_invalid(self):
        """Test POST request with invalid form data to send_group_request view."""
        form_data = {'recipient': self.other_user.pk}
        request = self.factory.post(reverse('send_group_request'), form_data)
        request.user = self.user

        with patch('journal.views.SendGroupRequestForm') as mock_form:
            mock_form_instance = mock_form.return_value
            mock_form_instance.is_valid.return_value = False

            response = send_group_request(request)

            # Check if the view renders the template with the form
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'send_group_request.html')
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], SendGroupRequestForm)
