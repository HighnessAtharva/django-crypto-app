import requests
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_decode

from .forms import CustomUserCreationForm
from .models import Cryptocurrency, Portfolio, Profile, Referal


def login_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('portfolio')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('portfolio')
        else:
            messages.error(request, "Invalid username or password.", extra_tags='danger')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('home')

def signup_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('portfolio')
    
    if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            
            if form.is_valid():
                user = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password1'])
                user.email = form.cleaned_data['email']
                user.save()
                messages.success(request, 'You have successfully signed up!', extra_tags='success')
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# block access to signup page if user is already logged in
def signup_with_referrer_view(request, referral_code):
    
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('portfolio')
            
    try:
        # get the User Profile of the referrer
        referrer = User.objects.get(profile__referral_code=referral_code)
    except User.DoesNotExist:
        # show error message if referrer does not exist
        return HttpResponse("Referrer does not exist")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.save()
            # create a referral instance
            referral = Referal.objects.create(user=user, referrer=referrer)
            referral.save()

            if referrer is not None:
                referrer.profile.bonus += 100  # add referral bonus to referrer
                referrer.profile.save()
                messages.success(request, f'{referrer.username} recieved a bonus of 100 points from you because you signed up using their referral link!')

            
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form, 'referrer': referrer})



@login_required(login_url="login")
def portfolio_view(request):
    # get the current logged in user
    current_user = request.user

    # get the referal code of the current user
    referral_code = current_user.profile.referral_code

    # get a list of all users who have the current user as their referrer
    referrals = Referal.objects.filter(referrer=current_user)

    # get total bonus earned by the current user
    total_bonus = current_user.profile.bonus

    # get the list of cryptocurrencies owned by the current user
    user_cryptocurrencies = Cryptocurrency.objects.filter(user=current_user)

    if user_portfolio := Portfolio.objects.filter(user=current_user).first():
        portfolio = Portfolio.objects.get(user=current_user)

        # get all the crypto currencies in the portfolio and recalculate the total value of the portfolio
        new_portfolio_value = 0

        user_cryptocurrencies = Cryptocurrency.objects.filter(user=current_user)
        for cryptocurrency in user_cryptocurrencies:
            total_value = cryptocurrency.quantity * cryptocurrency.current_price
            new_portfolio_value += total_value

        portfolio.total_value = new_portfolio_value
        portfolio.save()

        context = {
            'current_user': current_user,
            'referral_code': referral_code,
            'user_cryptocurrencies': user_cryptocurrencies,
            'user_portfolio': user_portfolio,
            'referrals': referrals, 
            'total_bonus': total_bonus,
            'new_portfolio_value': new_portfolio_value,
        }
    else:
        context = {
            'current_user': current_user,
            'referral_code': referral_code,
            'user_cryptocurrencies': user_cryptocurrencies,
            'user_portfolio': user_portfolio,
            'referrals': referrals, 
            'total_bonus': total_bonus,
        }
    return render(request, 'portfolio.html', context)


def home_view(request):
    # get the top 10 crypto currencies by market cap
    top_10_crypto_url_global = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=true'
    top_10_crypto_data_global = requests.get(top_10_crypto_url_global).json()

    # check if user is logged in    
    if request.user.is_authenticated:
        
        # get user's crypto currencies
        user_cryptocurrencies = Cryptocurrency.objects.filter(user=request.user)
        user_portfolio = Portfolio.objects.filter(user=request.user).first()
        
        # get the prices and price changes for user's cryptocurrencies
        names = [crypto.name for crypto in user_cryptocurrencies]
        symbols = [crypto.symbol for crypto in user_cryptocurrencies]
        ids = [crypto.id_from_api for crypto in user_cryptocurrencies]
        prices=[]
        
        # NOTE: Only showing the price change for the last 24 hours for now and not the percentage change to reduce the number of api calls. Only 10-20 api calls per minute are allowed for free users. Otherwise, I could have used the /coins/{id}/market_chart?vs_currency=usd&days=1 endpoint to get the price change for the last 24 hours and calculate the percentage change from that.
        for crytpo_id in ids:  
            prices_url = f'https://api.coingecko.com/api/v3/simple/price?ids={crytpo_id}&vs_currencies=usd&include_24hr_change=true'
            prices_data = requests.get(prices_url).json()

            price_change = prices_data[crytpo_id]['usd_24h_change']
            prices.append(price_change)
            
        # make a dictionary out of the names and prices
        crypto_price_changes = dict(zip(names, prices))
            
        context = {
            'top_10_crypto_data_global': top_10_crypto_data_global,
            'user_cryptocurrencies': user_cryptocurrencies,
            'user_portfolio': user_portfolio,
            'crypto_price_changes': crypto_price_changes,
        }
        
    else:
        context = {'top_10_crypto_data_global': top_10_crypto_data_global}    
    return render(request, 'home.html', context)


@login_required(login_url="login")
def search_view(request):
    if request.method != 'POST':
        # return HTTP status code 405 if the request method is not POST along with a message
        return HttpResponseNotAllowed(['POST'], 'Only POST requests are allowed for this view. Go back and search a cryptocurrency.')
    
    if not (search_query := request.POST.get('search_query')):
        return HttpResponse('No crypto currency found based on your search query.')
    
    api_url = f'https://api.coingecko.com/api/v3/search?query={search_query}'
    response = requests.get(api_url)
    search_results = response.json()
    try:
        data = search_results['coins'][0]
    except IndexError:
        return HttpResponse('No crypto currency found based on your search query.')
    coin_id = data['id']
    image = data['large']
    symbol = data['symbol']
    market_cap = data['market_cap_rank']

    # check if the crypto currency is already in the users portfolio and pass that information to the template
    current_user = request.user
    is_already_in_portfolio = False

    user_cryptocurrencies = Cryptocurrency.objects.filter(user=current_user)
    for cryptocurrency in user_cryptocurrencies:
        if cryptocurrency.name.lower() == coin_id.lower():
            is_already_in_portfolio = True    

    context = {
        'data': data,
        'coin_id': coin_id,
        'image': image,
        'symbol': symbol,
        'market_cap': market_cap,
        'is_already_in_portfolio': is_already_in_portfolio,
    }
    return render(request, 'search.html', context)
    
@login_required(login_url="login")
def add_to_portfolio_view(request):
    if request.method != 'POST':
        return HttpResponse('Need a crypto currency to add to your portfolio. Go back to the home page and search for a crypto currency.')
    
    # get values from the form
    coin_id = request.POST.get('id')
    quantity = request.POST.get('quantity')
    print(coin_id)
    
    # get the crypto currency data from the coingecko api based on the coin id
    api_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    response = requests.get(api_url)
    data = response.json()
    print(data)
    # store the name, symbol, current price, and market cap rank of the crypto currency
    user = request.user
    name = data['name']
    id_from_api = data['id']
    symbol = data['symbol']
    current_price = data['market_data']['current_price']['usd']

    try:
        # save the crypto currency to the database
        crypto_currency = Cryptocurrency.objects.create(
            user = user,
            name= name,
            id_from_api= id_from_api,
            symbol= symbol,
            quantity= quantity,
            current_price=current_price,
        )
    except IntegrityError:
        crypto_currency = Cryptocurrency.objects.get(user=user, name=name)
        crypto_currency.quantity += int(quantity)


    crypto_currency.save()

    # calculate the total value of the crypto currency
    total_value = int(quantity) * int(current_price)

    # save the total value of the crypto currency to the database in the portfolio model
    # check if the user already has a portfolio
    if Portfolio.objects.filter(user=user).exists():
        portfolio = Portfolio.objects.get(user=user)
        portfolio.total_value += total_value
    else: 
        portfolio = Portfolio(user=user, total_value=total_value)     

    portfolio.save()
    messages.success(request, f'{name} has been added to your portfolio.')

    # if all the above steps are successful, redirect the user to the portfolio page
    return redirect('portfolio') 
  
@login_required(login_url="login")      
def delete_from_portfolio_view(request, pk):
    # get the current logged in user
    user = request.user
    
    # get the crypto currency object from the database
    crypto_currency = Cryptocurrency.objects.get(pk=pk)
    
    # delete the crypto currency from the database
    crypto_currency.delete()
    
    # update the total value of the portfolio
    portfolio = Portfolio.objects.get(user=user)
    
    # get all the crypto currencies in the portfolio and recalculate the total value of the portfolio
    user_cryptocurrencies = Cryptocurrency.objects.filter(user=user)
    for cryptocurrency in user_cryptocurrencies:
        total_value = cryptocurrency.quantity * cryptocurrency.current_price
        portfolio.total_value += total_value
    
    portfolio.save()    

    # send an alert to the user that the crypto currency has been deleted from the portfolio
    messages.warning(request, f'{crypto_currency.name} has been deleted from your portfolio.')
    
    return redirect('portfolio')
    