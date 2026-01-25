Feature: Account transfers

Scenario: Incoming transfer increases balance
    Given Account registry is empty
    And I create an account using name: "robert", last name: "lewadnowski", pesel: "60010100001"
    When I make "incoming" transfer of "500" for account with pesel: "60010100001"
    Then Transfer response code equals: "200"
    And Transfer response message equals: "Zlecenie przyjęto do realizacji"
    And Account with pesel "60010100001" has "balance" equal to "500"

Scenario: Outgoing transfer reduces balance
    Given Account registry is empty
    And I create an account using name: "grzegorz", last name: "grzesio", pesel: "60010100002"
    And I make "incoming" transfer of "300" for account with pesel: "60010100002"
    When I make "outgoing" transfer of "120" for account with pesel: "60010100002"
    Then Transfer response code equals: "200"
    And Transfer response message equals: "Zlecenie przyjęto do realizacji"
    And Account with pesel "60010100002" has "balance" equal to "180"

Scenario: Express transfer charges fee
    Given Account registry is empty
    And I create an account using name: "pawel", last name: "paweleski", pesel: "60010100003"
    And I make "incoming" transfer of "100" for account with pesel: "60010100003"
    When I make "express" transfer of "50" for account with pesel: "60010100003"
    Then Transfer response code equals: "200"
    And Transfer response message equals: "Zlecenie przyjęto do realizacji"
    And Account with pesel "60010100003" has "balance" equal to "49"

Scenario: Outgoing transfer with insufficient funds fails
    Given Account registry is empty
    And I create an account using name: "stefan", last name: "stefanowski", pesel: "60010100004"
    When I make "outgoing" transfer of "50" for account with pesel: "60010100004"
    Then Transfer response code equals: "422"
    And Account with pesel "60010100004" has "balance" equal to "0"
