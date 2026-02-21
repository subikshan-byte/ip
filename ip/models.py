from django.db import models

# ===================== FOUND ITEM MODEL =====================

class FoundItem(models.Model):
    ITEM_TYPES = [
        ('mobile', 'Mobile Phone'),
        ('headset', 'Headset'),
        ('waterbottle', 'Water Bottle'),
        ('idcard', 'ID Card'),
        ('books', 'Books'),
        ('laptop', 'Laptop'),
        ('charger', 'Charger'),
        ('wallet', 'Wallet'),
        ('keys', 'Keys'),
        ('bag', 'Bag'),
        ('jewelry', 'Jewelry'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Like New'),
        ('good', 'Good'),
        ('worn', 'Worn'),
        ('damaged', 'Damaged'),
    ]

    STORAGE_CHOICES = [
        ('with-me', 'With Finder'),
        ('security-desk', 'Security Desk'),
        ('lost-found-office', 'Lost & Found Office'),
        ('reception', 'Reception'),
        ('police-station', 'Police Station'),
        ('other-location', 'Other'),
    ]

    # Item Info
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    brand = models.CharField(max_length=100, blank=True, null=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField()

    found_location = models.CharField(max_length=255)
    found_date = models.DateTimeField()

    storage_location = models.CharField(max_length=50, choices=STORAGE_CHOICES)
    specific_storage_location = models.CharField(max_length=255, blank=True, null=True)

    # Image Upload
    photo = models.ImageField(upload_to="found_items/")

    # Finder Contact
    finder_name = models.CharField(max_length=100)
    finder_email = models.EmailField()
    finder_phone = models.CharField(max_length=20, blank=True, null=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type} found at {self.found_location}"
from django.db import models

class LostItem(models.Model):
    
    ITEM_TYPES = [
        ('mobile', 'Mobile Phone'),
        ('headset', 'Headset'),
        ('waterbottle', 'Water Bottle'),
        ('idcard', 'ID Card'),
        ('books', 'Books'),
        ('laptop', 'Laptop'),
        ('charger', 'Charger'),
        ('wallet', 'Wallet'),
        ('keys', 'Keys'),
        ('bag', 'Bag'),
        ('jewelry', 'Jewelry'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ]

    # Item Details
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    brand = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField()

    lost_location = models.CharField(max_length=255)
    lost_date = models.DateTimeField()

    # Photo (optional)
    photo = models.ImageField(upload_to="lost_items/", blank=True, null=True)

    # Owner Contact Info
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    owner_phone = models.CharField(max_length=20, blank=True, null=True)

    # Meta Data
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type} lost by {self.owner_name}"