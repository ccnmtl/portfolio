import portfolio


def published_entries_by_date():
    # Get list of project Entries
    entries = portfolio.main.models.Entry.objects.live().public()
    # sort here, return only six cards
    entries = entries.order_by('-release_date')[:6]

    return entries


def featured_entries_by_slot():
    entries = portfolio.main.models.Entry.objects.live().public()

    # Get list of featured project Entries
    featured_entries = entries.filter(feature_on_homepage=True)
    # sort here, return only 3 cards
    featured_entries = featured_entries.order_by('feature_slot')[:3]

    return featured_entries
