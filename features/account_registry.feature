Feature: Account registry

Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kazio", last name: "kazowski", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "halina", last name: "haliniak", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filutek"
    Then Account with pesel "95092909876" has "surname" equal to "filutek"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "grzegorz", last name: "grzegorz", pesel: "91010112345"
    When I update "name" of account with pesel: "91010112345" to "grzesiek"
    Then Account with pesel "91010112345" has "name" equal to "grzesiek"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "pawel", last name: "paweleski", pesel: "82020256789"
    Then Account with pesel "82020256789" has "name" equal to "pawel"
    And Account with pesel "82020256789" has "surname" equal to "paweleski"
    And Account with pesel "82020256789" has "pesel" equal to "82020256789"
    And Account with pesel "82020256789" has "balance" equal to "0"

Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "zbyszek", last name: "zbychowski", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"
