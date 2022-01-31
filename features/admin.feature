Feature: Admin page

  Scenario: Operate as an admin user

	Given an anonymous user
	When I submit valid credentials at the login page
	Then I see the administration dashboard

	Given an admin user
	When I save a new employee
	Then I see a success message

  Scenario: Login using invalid credentials

    Given an anonymous user
	When I submit invalid credentials at the login page
	Then I see a login error message
