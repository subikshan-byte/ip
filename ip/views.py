from django.shortcuts import render
from django.db.models import Q
from .models import LostItem, FoundItem


def index(request):
    lost_items = LostItem.objects.all().order_by("-created_at")
    found_items = FoundItem.objects.all().order_by("-created_at")
    return render(request, 'index.html', {"lost_items": lost_items, "found_items": found_items})


def search(request):
    query = request.GET.get('q', '').strip()
    item_type = request.GET.get('item_type', '').strip()

    lost_items = LostItem.objects.all().order_by("-created_at")
    found_items = FoundItem.objects.all().order_by("-created_at")

    if query:
        lost_items = lost_items.filter(
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(lost_location__icontains=query) |
            Q(owner_name__icontains=query)
        )
        found_items = found_items.filter(
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(found_location__icontains=query) |
            Q(finder_name__icontains=query)
        )

    if item_type:
        lost_items = lost_items.filter(item_type=item_type)
        found_items = found_items.filter(item_type=item_type)

    return render(request, 'search_results.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'query': query,
        'item_type': item_type,
    })


def lost(request):
    if request.method == "POST":
        item_type = request.POST.get("itemType")
        brand = request.POST.get("brand") or "Unknown"
        description = request.POST.get("description")
        lost_location = request.POST.get("lostLocation")
        lost_date = request.POST.get("lostDate")
        owner_name = request.POST.get("name")
        owner_email = request.POST.get("email")
        owner_phone = request.POST.get("phone")
        photo = request.FILES.get("photo")

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

        matches = []
        found_items = FoundItem.objects.all()
        stop_words = {'a','an','the','and','or','is','it','in','on','at','to','for','of','with'}

        for item in found_items:
            score = 0
            if item.item_type == item_type:
                score += 2
            if item.brand and brand and item.brand.lower() == brand.lower():
                score += 2
            lost_words = set(description.lower().split()) - stop_words
            found_words = set(item.description.lower().split()) - stop_words
            if len(lost_words.intersection(found_words)) >= 2:
                score += 1
            if score > 0:
                matches.append({"item": item, "score": score})

        matches = sorted(matches, key=lambda x: x["score"], reverse=True)
        return render(request, "match_results.html", {
            "submitted_item": lost_item,
            "matches": matches,
            "mode": "lost",
        })

    return render(request, "lost.html")


def found(request):
    if request.method == "POST":
        item_type = request.POST.get("item_type")
        brand = request.POST.get("brand") or "Unknown"
        condition = request.POST.get("condition") or "unknown"
        description = request.POST.get("description", "").lower()
        found_location = request.POST.get("found_location")
        found_date = request.POST.get("found_date")
        storage_location = request.POST.get("storage_location")
        finder_name = request.POST.get("finder_name")
        finder_email = request.POST.get("finder_email")
        finder_phone = request.POST.get("finder_phone")
        photo = request.FILES.get("photo")

        found_item = FoundItem.objects.create(
            item_type=item_type,
            brand=brand,
            condition=condition,
            description=description,
            found_location=found_location,
            found_date=found_date,
            storage_location=storage_location,
            finder_name=finder_name,
            finder_email=finder_email,
            finder_phone=finder_phone,
            photo=photo,
        )

        matches = []
        lost_items = LostItem.objects.all()
        stop_words = {'a','an','the','and','or','is','it','in','on','at','to','for','of','with'}

        for item in lost_items:
            score = 0
            if item.item_type == item_type:
                score += 2
            if item.brand and brand and item.brand.lower() == brand.lower():
                score += 2
            found_words = set(description.split()) - stop_words
            lost_words = set(item.description.lower().split()) - stop_words
            if len(found_words.intersection(lost_words)) >= 2:
                score += 1
            if score > 0:
                matches.append({"item": item, "score": score})

        matches = sorted(matches, key=lambda x: x["score"], reverse=True)
        return render(request, "match_results.html", {
            "submitted_item": found_item,
            "matches": matches,
            "mode": "found",
        })

    return render(request, "found.html")
