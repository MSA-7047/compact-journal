# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from journal.models import FriendRequest
# from journal.views import accept_invitation




# class AcceptInvitationTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user1 = get_user_model().objects.create_user(username='test_user1', email='test1_user1@example.com', password='test_password1')
#         self.user2 = get_user_model().objects.create_user(username='test_user2', email='test1_user2@example.com', password='test_password2')        
#         self.friend_request = FriendRequest.objects.create(sender=self.user1, recipient=self.user2)

#     def test_accept_invitation(self):
#         request = self.client.request().wsgi_request  # Create a mock request
#         response = accept_invitation(request, self.friend_request.id)
        
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect

#         # Check if the friend request is marked as accepted
#         updated_friend_request = FriendRequest.objects.get(id=self.friend_request.id)
#         self.assertFalse(updated_friend_request.is_accepted)


# A LITTLE BIT DODGY DEFFO LOOK OVER