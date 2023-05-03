from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import resolve, reverse
from test_plus import TestCase

from .forms import CustomUserCreationForm
from .models import *
from .views import *


class UrlTest(TestCase):

    # CREATE THE TEST USER
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='12345'
        )
    

    """ 
    ----------------
    HOME PAGE TESTS
    -----------------
    """
    def testHomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
      
    def testHomePageUrl(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home_view)  
    
    def testHomePageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def testHomePageContainsCorrectHtml(self):
        response = self.client.get('/')
        self.assertContains(response, 'Top 10 CryptoCurrency Rankings')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
        
    
    """ 
    ----------------
    LOGIN PAGE TESTS
    -----------------
    """
    def testLoginPage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
    
    def testLoginPageUrl(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)
        
    def testLoginPageTemplate(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')
         
    def testLoginPageContainsCorrectHtml(self):
        response = self.client.get('/login/')
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
    
    def testLoginPageRedirectsToPortfolioPage(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/login/')
        self.assertRedirects(response, '/portfolio/')
    
    def testLoginPageRedirectIfAlreadyLoggedIn(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/login/')
        self.assertRedirects(response, '/portfolio/')
  
    def testLoginPageFormCorrect(self):
        response = self.client.get('/login/')
        form = response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)
        self.assertContains(response, 'csrfmiddlewaretoken')
         
    
    """ 
    ----------------
    SIGNUP PAGE TESTS
    -----------------
    """
    def testSignupPage(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        
    
    def testSignupPageUrl(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup_view)
        
    def testSignupPageTemplate(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, 'signup.html')
         
    def testSignupPageContainsCorrectHtml(self):
        response = self.client.get('/signup/')
        self.assertContains(response, 'Signup')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
    
    def testSignupPageRedirectIfAlreadyLoggedIn(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/signup/')
        self.assertRedirects(response, '/portfolio/')

    def testSignupPageFormCorrect(self):
        response = self.client.get('/signup/')
        form = response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
        self.assertContains(response, 'csrfmiddlewaretoken')

    """ 
    ----------------
    PORTFOLIO PAGE TESTS
    -----------------
    """
    def testPortfolioPageNoLogin(self):    
        # check if logged out user can access portfolio page
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 302)
        
    
    def testPortfolioPageLogin(self):
        # check if logged in user can access portfolio page
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
    
    
    def testPortfolioPageUrl(self):
        url = reverse('portfolio')
        self.assertEqual(resolve(url).func, portfolio_view)
        
    def testPortfolioPageTemplate(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/portfolio/')
        self.assertTemplateUsed(response, 'portfolio.html')
    
    def testPortfolioPageContainsCorrectHtml(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/portfolio/')
        self.assertContains(response, 'Wallet')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
    
 

    
    """    
    ----------------
    RESET PAGE TESTS
    -----------------
    """
    
    def testResetPasswordPageUrl(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)
         
    def testResetPasswordPageTemplate(self):
        response = self.client.get('/password_reset/')
        self.assertTemplateUsed(response, 'reset/password_reset.html')
    
    def testResetPasswordPageContainsCorrectHtml(self):
        response = self.client.get('/password_reset/')
        self.assertContains(response, 'Reset Password')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
        
    def testResetPasswordDonePageUrl(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)
         
    def testResetPasswordDonePageTemplate(self):
        response = self.client.get('/password_reset_done/')
        self.assertTemplateUsed(response, 'reset/password_reset_done.html')
        
    def testResetPasswordDonePageContainsCorrectHtml(self):
        response = self.client.get('/password_reset_done/')
        self.assertContains(response, 'An email has been sent with instructions to reset your password')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
    
    def testResetPasswordCompletePageUrl(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)
        
    def testResetPasswordCompletePageTemplate(self):
        response = self.client.get('/password_reset_complete/')
        self.assertTemplateUsed(response, 'reset/password_reset_complete.html')
        
    def testResetPasswordCompletePageContainsCorrectHtml(self):
        response = self.client.get('/password_reset_complete/')
        self.assertContains(response, 'Your password has been set.')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
        
    """    
    ----------------
    SEARCH PAGE TESTS
    -----------------
    """
         
    def testSearchPageNoLogin(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 302)
    
    def testSearchPageUrl(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search_view)
    
    # check if search page can only be accessed by POST request
    def testSearchPagePostOnly(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 405)
        
        response = self.client.post('/search/')
        self.assertEqual(response.status_code, 200)
        
    
class ModelTest(TestCase):
    # CREATE THE TEST USER
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='12345'
        )

        self.referral = User.objects.create_user(
            username='referraluser',
            email='referreduser@example.com',
            password='12345'
        )
       
    """
    ----------------
    USER MODEL TESTS
    -----------------
    """
    
    def testUserModelCorrectData(self):
        test_user = self.user
        self.assertEqual(test_user.username, 'testuser2')
        self.assertEqual(test_user.email, 'testuser2@example.com')
        self.assertTrue(isinstance(test_user, User))
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
    
    def testErrorOnDuplicateUsername(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='testuser2',
                email='testuser2@example.com',
                password='12345'
        )
                
    
    """ 
    ----------------
    CRYPTOCURRENCY MODEL TESTS
    -----------------
    """
    
    def testCryptocurrencyModel(self):
        cryptocurrency = Cryptocurrency.objects.create(
            user = User.objects.create(username='testuser'),
            id_from_api = 'bitcoin',
            name = 'Bitcoin', 
            symbol = 'BTC',
            current_price = 10000,
            quantity = 1
        )
        self.assertEqual(cryptocurrency.name, 'Bitcoin')
        self.assertEqual(cryptocurrency.symbol, 'BTC')
        self.assertEqual(cryptocurrency.current_price, 10000)
        self.assertEqual(cryptocurrency.quantity, 1)
        self.assertEqual(cryptocurrency.user.username, 'testuser')
        self.assertTrue(isinstance(cryptocurrency, Cryptocurrency))
        
    def testCryptocurrencyModelErrorOnDuplicate(self):
        Cryptocurrency.objects.create(
            user = User.objects.create(username='testuser'),
            id_from_api = 'bitcoin',
            name = 'Bitcoin', 
            symbol = 'BTC',
            current_price = 10000,
            quantity = 1
        )
        with self.assertRaises(IntegrityError):
            Cryptocurrency.objects.create(
                user = User.objects.create(username='testuser'),
                id_from_api = 'bitcoin',
                name = 'Bitcoin', 
                symbol = 'BTC',
                current_price = 10000,
                quantity = 1
            )
            self.fail('Cryptocurrency model should not allow duplicate cryptocurrencies')
            
    def testCryptocurrencyCurrentPrice(self):
        crypto = Cryptocurrency.objects.create(
            user=self.user,
            id_from_api='bitcoin',
            name='Bitcoin', 
            symbol='BTC',
            current_price=10000,
            quantity=1
        )
        self.assertEqual(crypto.current_price, 10000)
        
    def testCryptocurrencyStr(self):
        crypto = Cryptocurrency.objects.create(
            user=self.user,
            id_from_api='bitcoin',
            name='Bitcoin', 
            symbol='BTC',
            current_price=10000,
            quantity=1
        )
        self.assertEqual(str(crypto), 'Bitcoin (BTC)')
        
    def testCryptocurrencyQuantityDefaultValue(self):
        crypto = Cryptocurrency.objects.create(
            user=self.user,
            id_from_api='bitcoin',
            name='Bitcoin', 
            symbol='BTC',
            current_price=10000
        )
        self.assertEqual(crypto.quantity, 1)
        
        
    """
    ----------------
    REFERRAL MODEL TESTS
    -----------------
    """
    
    # make a referral and check if it is created correctly
    def testReferralModel(self):
        referral = Referal.objects.create(
            user=self.user,
            referrer=self.referral
        )
        self.assertEqual(referral.user.username, 'testuser2')
        self.assertEqual(referral.referrer.username, 'referraluser')
        self.assertTrue(isinstance(referral, Referal))
        
    
    
    """ 
    ----------------
    PORTFOLIO MODEL TESTS
    -----------------
    """
      
    def testPortfolioModel(self):
        portfolio = Portfolio.objects.create(
            user=self.user,
            total_value=10000
        )
        self.assertEqual(portfolio.user.username, 'testuser2')
        self.assertEqual(portfolio.total_value, 10000)
        self.assertTrue(isinstance(portfolio, Portfolio))
    

    """ 
    ----------------
    PROFILE MODEL TESTS
    -----------------
    """
    def testProfileModel(self):
        # referral code should be generated automatically using small uuid
        import shortuuid
        shortuuid.ShortUUID().random(length=10)
          
        referral_code = shortuuid.uuid()
        
        # make a dummy user
        dummy_user = User.objects.create_user(
            username='dummyprofile',
            email = 'dummyemail@example.com',
            password='12345'
        )

        
        profile = Profile.objects.create(
            user=dummy_user,
            referral_code=referral_code
        )
        
        self.assertEqual(profile.user.username, 'dummyprofile')
        self.assertEqual(profile.referral_code, referral_code)
        self.assertTrue(isinstance(profile, Profile))
        
        
""" 
MAKING SEPERATE TEST CLASSES FOR VIEWS
"""
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email="example@example.com", password='testpass')

    def test_login_view_with_valid_credentials(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('portfolio'))

    def test_login_view_with_invalid_credentials(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'invaliduser', 'password': 'invalidpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        
        
class TestAddToPortfolioView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_to_portfolio_view_success(self):
        with patch('mainapp.views.requests.get') as mock_get:
            mock_data = {
                'name': 'Bitcoin',
                'id': 'bitcoin',
                'symbol': 'BTC',
                'market_data': {
                    'current_price': {
                        'usd': 50000.00
                    }
                }
            }
            mock_get.return_value.json.return_value = mock_data

            data = {
                'id': 'bitcoin',
                'quantity': 10
            }
            response = self.client.post(
                reverse('add_to_portfolio'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('portfolio'))

        crypto_currency = Cryptocurrency.objects.get(
            user=self.user, id_from_api='bitcoin')
        self.assertEqual(crypto_currency.name, 'Bitcoin')
        self.assertEqual(crypto_currency.symbol, 'BTC')
        self.assertEqual(crypto_currency.quantity, 10)
        self.assertEqual(crypto_currency.current_price, 50000.00)

        portfolio = Portfolio.objects.get(user=self.user)
        self.assertEqual(portfolio.total_value, 500000.00)

    def test_add_to_portfolio_view_get_request(self):
        response = self.client.get(reverse('add_to_portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Need a crypto currency to add to your portfolio. Go back to the home page and search for a crypto currency.')

from django.contrib.auth.models import User
from django.test import Client, TestCase


class SearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        
    def test_valid_search(self):
        response = self.client.post('/search/', {'search_query': 'bitcoin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BTC')
        
    def test_invalid_search(self):
        response = self.client.post('/search/', {'search_query': 'invalid_crypto_currency'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No crypto currency found based on your search query.')


class DeleteFromPortfolioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.crypto_currency = Cryptocurrency.objects.create(user=self.user, id_from_api='bitcoin', name='Bitcoin', symbol='BTC', current_price=Decimal('10000'), quantity=Decimal('2'))
        self.portfolio = Portfolio.objects.create(user=self.user, total_value=Decimal('20000'))

    def test_delete_from_portfolio_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('delete_from_portfolio', args=[self.crypto_currency.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('portfolio'))
        self.assertFalse(Cryptocurrency.objects.filter(pk=self.crypto_currency.pk).exists())
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.total_value, Decimal('0'))

    def test_delete_from_portfolio_view_with_unauthenticated_user(self):
        url = reverse('delete_from_portfolio', args=[self.crypto_currency.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        self.assertTrue(Cryptocurrency.objects.filter(pk=self.crypto_currency.pk).exists())
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.total_value, Decimal('20000'))



class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.top_10_crypto_url_global = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=true'
        self.top_10_crypto_data_global = requests.get(self.top_10_crypto_url_global).json()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.crypto = Cryptocurrency.objects.create(name='Bitcoin', symbol='BTC', id_from_api='bitcoin', user=self.user, current_price=Decimal('10000'), quantity=Decimal('2'))
        self.portfolio = Portfolio.objects.create(user=self.user, total_value=Decimal('20000'))
        self.url = reverse('home')

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue('top_10_crypto_data_global' in response.context)
        self.assertTrue('user_cryptocurrencies' in response.context)
        self.assertTrue('user_portfolio' in response.context)
        self.assertTrue('crypto_price_changes' in response.context)

    def test_home_view_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue('top_10_crypto_data_global' in response.context)
        self.assertFalse('user_cryptocurrencies' in response.context)
        self.assertFalse('user_portfolio' in response.context)
        self.assertFalse('crypto_price_changes' in response.context)
        
class SignupWithReferrerViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.referrer = User.objects.create_user(
            username='test_referrer', email='test_referrer@example.com', password='testpassword')
        self.referrer_profile = Profile.objects.get(user=self.referrer)
        self.referral_code = self.referrer_profile.referral_code

    def test_signup_with_referrer_view_GET(self):
        response = self.client.get(reverse('signup_with_referrer_view', args=[self.referral_code]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_with_referrer_view_POST(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('signup_with_referrer_view', args=[self.referral_code]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)
        # get the user object from the database
    
        self.assertEqual(Referal.objects.get(user__username='testuser').referrer, self.referrer)
        self.assertEqual(Profile.objects.get(user__username='test_referrer').bonus, 100)
        self.assertRedirects(response, reverse('login'))
        
class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.valid_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'passw0rd',
            'password2': 'passw0rd'
        }
        
    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
        
    def test_signup_view_post_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'different_password'
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
        self.assertEqual(User.objects.count(), 0)
        
class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        
    def test_logout_view(self):
        # make sure user is logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # this is only visible to logged in users below the Top 10 Cryptocurrencies table
        self.assertTrue('24H SUMMARY' in str(response.content))

        # logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        # check if user is logged out
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('testuser' in str(response.content))
        
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertRedirects(response, reverse('portfolio'))
        user = authenticate(username='testuser', password='testpass')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
        self.assertTrue(user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Invalid username or password.")

    def tearDown(self):
        self.user.delete()