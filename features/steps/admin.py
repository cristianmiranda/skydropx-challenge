from behave import given, when, then


@given('an anonymous user')
def step_impl(context):
    br = context.browser

    br.get(context.base_url + '/admin/projecttracker')


@when('I submit valid credentials at the login page')
def step_impl(context):
    br = context.browser

    br.find_element_by_id('id_username').send_keys('admin')
    br.find_element_by_id('id_password').send_keys('localUserPasswordHere')

    br.find_element_by_xpath("//input[@value='Log in']").click()


@then('I see the administration dashboard')
def step_impl(context):
    br = context.browser

    assert br.find_element_by_xpath("//h1[contains(text(),'Projecttracker administration')]").is_enabled()


@given("an admin user")
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/admin/projecttracker')


@when("I save a new employee")
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/admin/projecttracker/employee/add/')

    br.find_element_by_id('id_name').send_keys('Julián')
    br.find_element_by_name('_save').click()


@then("I see a success message")
def step_impl(context):
    br = context.browser

    assert br.find_element_by_xpath("//li[contains(@class, 'success')]").is_enabled()


@when('I submit invalid credentials at the login page')
def step_impl(context):
    br = context.browser

    br.find_element_by_id('id_username').send_keys('admin')
    br.find_element_by_id('id_password').send_keys('this-is-the-wrong-password')

    br.find_element_by_xpath("//input[@value='Log in']").click()


@then("I see a login error message")
def step_impl(context):
    br = context.browser

    assert br.find_element_by_xpath("//p[contains(text(), 'Please enter the correct username and password for a staff "
                                    "account. Note that both fields may be case-sensitive')]").is_enabled()
