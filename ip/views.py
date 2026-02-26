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
        brand = request.POST.get("brand") or "Unknown"
       
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
        matches = []

        found_items = FoundItem.objects.all()

        for item in found_items:
            score = 0

            # 1️⃣ item type match
            if item.item_type == item_type:
                score += 1

            # 2️⃣ brand match
            if item.brand and item.brand.lower() == brand.lower():
                score += 1

            # 3️⃣ description keyword match
            lost_words = set(description.split())
            found_words = set(item.description.lower().split())

            common_words = lost_words.intersection(found_words)

            if len(common_words) >= 2:  # adjustable sensitivity
                score += 1

            # only keep meaningful matches
            if score > 0:
                matches.append({
                    "item": item,
                    "score": score
                })

        # sort best matches first
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)

        # Send results to template
        return render(request, "match_results.html", {
            "lost_item": lost_item,
            "matches": matches,"l":"1"
        })

    return render(request, "lost.html")
from django.shortcuts import render, redirect
from .models import FoundItem

def found(request):
    if request.method == "POST":
        brand = request.POST.get("brand") or "Unknown"
        
        FoundItem.objects.create(
            item_type=request.POST.get("item_type"),
            brand=brand,
      
            condition = request.POST.get("condition") or "unknown",
            description=request.POST.get("description"),
            found_location=request.POST.get("found_location"),
            found_date=request.POST.get("found_date"),
            storage_location=request.POST.get("storage_location"),
            finder_name=request.POST.get("finder_name"),
            finder_email=request.POST.get("finder_email"),
            finder_phone=request.POST.get("finder_phone"),
            photo=request.FILES.get("photo"),
        )
        matches = []

        found_items = LostItem.objects.all()

        for item in found_items:
            score = 0

            # 1️⃣ item type match
            if item.item_type == item_type:
                score += 1

            # 2️⃣ brand match
            if item.brand and item.brand.lower() == brand.lower():
                score += 1

            # 3️⃣ description keyword match
            lost_words = set(description.split())
            found_words = set(item.description.lower().split())

            common_words = lost_words.intersection(found_words)

            if len(common_words) >= 2:  # adjustable sensitivity
                score += 1

            # only keep meaningful matches
            if score > 0:
                matches.append({
                    "item": item,
                    "score": score
                })

        # sort best matches first
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)

        return render(request, "match_results.html", {
            "lost_item": lost_item,
            "matches": matches,"l":"0"
        })
   

    return render(request, "found.html")
