Feature: User API Testing

  Scenario: Create an user with POST
    Given I set request headers to
      """
      {
        "Content-Type": "application/json"
      }
      """
    When I send a POST request to "/users" with payload
      """
      {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com"
      }
      """
    Then the response status code should be 201
    And I store the value of "id" as "user_id"
    And the response should contain "name" with value "John Doe"

  Scenario: Get a single user
    When I send a GET request to "/users/{user_id}"
    Then the response status code should be 200
    And the response should match JSON schema "user_schema.json"
    And the response should contain "id" with value "{user_id}"
    And the response should contain "name" with value "John Doe"
    And the response should contain "username" with value "johndoe"
    And the response should contain "email" with value "john@example.com"

 Scenario: Update a user's name
  When I send a PATCH request to "/users/{user_id}" with payload
    """
    {
      "name": "UpdateJohn Doe"
    }
    """
  Then the response status code should be 200
  And the response should contain "id" with value "{user_id}"
  And the response should contain "name" with value "UpdateJohn Doe"

    