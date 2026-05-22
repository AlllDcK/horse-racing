# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from django.urls import reverse
#
# from races.models import Horse, Profile, Bet
#
#
# class RaceViewTest(TestCase):
#
#     def setUp(self):
#
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             username="max",
#             password="12345"
#         )
#
#         self.profile = Profile.objects.get(user=self.user)
#         self.profile.balance = 1000
#         self.profile.save()
#
#         self.horse1 = Horse.objects.create(
#             name="Thunder",
#             base_speed=90
#         )
#
#         self.horse2 = Horse.objects.create(
#             name="Rocket",
#             base_speed=80
#         )
#
#     def test_redirect_if_not_logged_in(self):
#
#         response = self.client.get('/')
#
#         self.assertEqual(response.status_code, 302)
#
#     def test_race_page_loads(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.get('/')
#
#         self.assertEqual(response.status_code, 200)
#
#         self.assertContains(response, "Скачки")
#
#     def test_make_bet(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/', {
#             "horse_id": self.horse1.id,
#             "amount": 1000
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.profile.refresh_from_db()
#
#         self.assertTrue(
#             Bet.objects.filter(user=self.user).exists()
#         )
#
#     def test_invalid_bet_amount(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/', {
#             "horse_id": self.horse1.id,
#             "amount": -100
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.assertEqual(
#             Bet.objects.count(),
#             0
#         )
#
#
# class DepositViewTest(TestCase):
#
#     def setUp(self):
#
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             username="max",
#             password="12345"
#         )
#
#         self.profile = Profile.objects.get(user=self.user)
#         self.profile.balance = 1000
#         self.profile.save()
#
#     def test_deposit_money(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/deposit/', {
#             "amount": 500
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.profile.refresh_from_db()
#
#         self.assertEqual(
#             self.profile.balance,
#             1500
#         )
#
#     def test_invalid_deposit(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/deposit/', {
#             "amount": -100
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.profile.refresh_from_db()
#
#         self.assertEqual(
#             self.profile.balance,
#             1000
#         )
#
#
# class WithdrawViewTest(TestCase):
#
#     def setUp(self):
#
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             username="max",
#             password="12345"
#         )
#
#         self.profile = Profile.objects.get(user=self.user)
#         self.profile.balance = 2000
#         self.profile.save()
#
#     def test_withdraw_money(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/withdraw/', {
#             "amount": 500
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.profile.refresh_from_db()
#
#         self.assertEqual(
#             self.profile.balance,
#             1500
#         )
#
#     def test_withdraw_too_much(self):
#
#         self.client.login(
#             username="max",
#             password="12345"
#         )
#
#         response = self.client.post('/withdraw/', {
#             "amount": 10000
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.profile.refresh_from_db()
#
#         self.assertEqual(
#             self.profile.balance,
#             2000
#         )
#
#
# class RegisterViewTest(TestCase):
#
#     def setUp(self):
#
#         self.client = Client()
#
#     def test_register_user(self):
#
#         response = self.client.post('/register/', {
#
#             "username": "newuser",
#             "password1": "StrongPassword123",
#             "password2": "StrongPassword123"
#         })
#
#         self.assertEqual(response.status_code, 302)
#
#         self.assertTrue(
#             User.objects.filter(username="newuser").exists()
#         )
