import datetime
from finance.models import User
from finance.models import Share
User.objects.create_user(username="user1", password="user1", email="user1@email.com", is_superuser=True, is_staff=True)
user1 = User.objects.get(username="user1")
User.objects.create_user(username="user2", password="user2", email="user2@email.com")
Share.objects.create(user=user1, ticker="MSFT", value=1000, amount=5, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="AAPL", value=220, amount=2.5, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="MSFT", value=1000, amount=5, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="AAPL", value=300, amount=1, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="PPE.JO", value=1000, amount=10, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="PPE.JO", value=2000, amount=12, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="MC.PA", value=1200, amount=2, timestamp=datetime.datetime.now())
Share.objects.create(user=user1, ticker="MC.PA", value=1250, amount=1.5, timestamp=datetime.datetime.now())