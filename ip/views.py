from django.shortcuts import render

# Create your views here.
def index(request):
    lost_items = LostItem.objects.all().order_by("-created_at")
    found_items = FoundItem.objects.all().order_by("-created_at")
    return render(request, 'index.html',{"lost_items": lost_items, "found_items": found_items})
from django.shortcuts import render
from .models import LostItem, FoundItem

def lost(request):
    if request.method == "POST":
        # Get Lost Form Data
        item_type = request.POST.get("itemType")
        brand = request.POST.get("brand")
       
        description = request.POST.get("description")
        lost_location = request.POST.get("lostLocation")
        lost_date = request.POST.get("lostDate")

        owner_name = request.POST.get("name")
        owner_email = request.POST.get("email")
        owner_phone = request.POST.get("phone")
        photo = request.FILES.get("photo")

        # Save Lost Item
        lost_item = LostItem.objects.create(
            item_type=item_type,
            brand=brand,
            
            description=description,
            lost_location=lost_location,
            lost_date=lost_date,
            photo=photo,
            owner_name=owner_name,
            owner_email=owner_email,
            owner_phone=owner_phone,
        )

        # 🔥 AUTO MATCH FOUND ITEMS
        matches = FoundItem.objects.filter(
            item_type=item_type,
        )

        # Send results to template
        return render(request, "match_results.html", {
            "lost_item": lost_item,
            "matches": matches
        })

    return render(request, "lost.html")
from django.shortcuts import render, redirect
from .models import FoundItem

def found(request):
    if request.method == "POST":
        FoundItem.objects.create(
            item_type=request.POST.get("item_type"),
            brand=request.POST.get("brand"),
      
            condition=request.POST.get("condition"),
            description=request.POST.get("description"),
            found_location=request.POST.get("found_location"),
            found_date=request.POST.get("found_date"),
            storage_location=request.POST.get("storage_location"),
            finder_name=request.POST.get("finder_name"),
            finder_email=request.POST.get("finder_email"),
            finder_phone=request.POST.get("finder_phone"),
            photo=request.FILES.get("photo"),
        )

        return redirect("index")
   

    return render(request, "found.html")
