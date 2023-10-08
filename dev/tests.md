## Tests

### Where to find them
In every application, there is a folder "tests". Inside, there is one or more scripts, depending on what is tested. Usually, there is one for models, urls, and views.
The one that takes the more time is views, I would say.

### Concrete example: Users

Let's take a concrete example : the User application.

#### models
First, we tests the model User, in test_models.py.
Each test is written to test the functionnalities of the models.py helpers methods. So get_full_name, get_year_pg, etc.
Usually, for such tests, you would want to make a test for each small use case a theses methods. In our case, they are all regrouped into each method. This may be improved later on.

#### urls
Very simple, just to test that the url are resolving properly. If adding a new url, adding it here is the way to go.

### views
This one is the one that would ask for the more work, and the one that we can almost endlessly extend.
For now, the logic behind is simple enough : We try to access each page of the application, and see if the result correspond to the expected.

Actual Example: I try to create a new user. For that, I create the class UserCreateViewTestCase. I extend on BaseGeneralUserViewsTestCase for common usefull tests, but I'll extend on that below.
For the creation of user, I need to be connected to Borgia. And while being connected, I can have a few permissions through many groups (president, treasurers, shop managers, ...) :
- We test that the creation is aborted and user redirected to login page if disconnected (super().offline_user_redirection()).
- We test that the creation is refused if the player does not have the permission. (super().not_allowed_user_get()).
- We test that it can be successfully created if I have every necessary rights. (super().allowed_user_get()).

We then do that for every view.

#### Usefull common tests and fixtures

Borgia was set up so that a user needs to be connected for almost any action. As such, there was a need to differentiate between connected / not connected users, and also depending on which permission the user had.
For simplicity in the test creation (and after I realized there was a lot of redundancy), I created a base class containing these common tests.
This base class is called BaseBorgiaViewsTestCase.
Also, every time this base class is used, it automatically start a bare database, that is then populated by the initial and tests_data fixtures. (see the class). This fixture allows to do the tests on actual data.

I've done the same type of Base class for the shops (BaseShopsViewsTest). As above, there was a common need of testing if the user trying to access a page was a connected user, with the right to manage the specific shop, and so on...
In the base shops test class, I also add a few objects in the database. I believe these could be added as a fixture (to do later?).
