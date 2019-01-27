from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm

def index(request):
    # Query the DB for a list of all stored categories
    # Order the categories by number of likes in descending Order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    views_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': views_list}
    #print("Context Dictionary:", context_dict )
    return render(request, 'rango/index.html', context_dict)
#    return HttpResponse("<a href = '/rango/about'> About </a>")

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)
#    return HttpResponse("Rango says here is the about page.\
#    <br> <a href = '/rango'> Back home </a>")

def show_category(request, category_name_slug):
    # Context dict to pass to template renderer
    context_dict = {}

    try:
        # Look for category name slug with given name.
        # If not found, raise DoesNotExist exception.
        # So the .get() method returns one model instance or
        # raises an exception.
        category = Category.objects.get(slug = category_name_slug)

        # Retrieve all of the associated pages.
        # filter() will return a list of page objects or empty list
        pages = Page.objects.filter(category = category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages

        # We also add the category object from the DB to the context
        # dictionary. We'll use this in the template to verify that
        # the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        # Template will display "no category" message
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # A HTTP Post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # Bit since he most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)

        else:
            # The supplised form contained errors,
            # Print errors to terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases
    # Will render the form with error messages
    return render(request, 'rango/add_category.html', {'form': form})
