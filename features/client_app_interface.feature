Feature: Client app interface
    I need to add set of end points for my gui interface to manage
    things like user list view and any other things I might for my
    gui interface in the feature.

    list:
     - /CLIENT**: TRUE - turns on access to gui commands
     - /CLIENT**: USER LIST - returns a list of current users

    Background: Client app connections to server
        Given I came connected to the chat server as person1
        And I am connected to the server via a client application

    Scenario: Person enters the chatroom
        Given person2 is in the chatroom
        Then the client should receive CLIENT**: No Name,M

    Scenario: Person leave the chatroom
        Given person2 is in the chatroom
        When person2 leaves the chatroom
        Then the client should receive ,MCLIENT**: No Name

    Scenario Outline: Client app commands
        Given the client sends <command>
        Then the client should receive <response>

        |command              | response|
        |/CLIENT**: USER LIST | No Name | 
