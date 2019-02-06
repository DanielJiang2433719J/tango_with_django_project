from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()

    # A HTTP Post?
    if request.method == 'POST':
        form = PageForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)

        else:
            # The supplised form contained errors,
            # Print errors to terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases
    # Will render the form with error messages
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # A bool indicating to the template whether
    # the registration was successful. False by default.
    # True when registration succeeds
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from raw form
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit = False This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit = False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm
        # instances. These will be blank and ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                    'rango/register.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the user/pass provided by the user.
        # This info is from the login form.
        # We use request.POST.get('<variable>') as opposed to
        # request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # User Django's machinery to attempt to see if the user/pass
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a Userobject, the details are correct.
        # If None, no matching user credentials found.
        if user:
            # Is the account active? It could be disabled.
            if user.is_active:
                # If the account is active and valid, log user in.
                # Send user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no login
                return HttpResponse("Your Rango account is disabled.")

        else:
            # Bad login details were provided.
            print("Invalid login details: {0}, {1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST< so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # Not context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

# Use the logins_required() decorator
@login_required
def user_logout(request):
    # We know the user is logged in, so just log out
    logout(request)

    # Return to the homepage
    return HttpResponseRedirect(reverse('index'))
