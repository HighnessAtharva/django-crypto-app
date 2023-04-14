from django.contrib.auth.models import User
from django.db import models

# Override the default User model to make the email unique
User._meta.get_field('email')._unique = True

# Make the profile for a user, automatically created when a user is created using Django signals
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=10, unique=True)
    bonus = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} profile'

# Create the referal model
class Referal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')

    def __str__(self):
        return f'{self.user.username} was referred by {self.referrer.username}'

# Create the Cryptocurrency model
class Cryptocurrency(models.Model):
    # here name is also the id of the cryptocurrency, so useful for API calls
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cryptocurrencies', null=True)
    id_from_api = models.CharField(max_length=50)
    name = models.CharField(max_length=50) 
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f'{self.name} ({self.symbol})'

# Create the portfolio linked to a user and store the total value of the portfolio
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    total_value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} - Portfolio: {self.total_value}'


