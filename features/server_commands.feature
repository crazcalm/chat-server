Feature: Server Commands
    I want to list out the different commands that
    I want the server to respond to.

    list:
        /disconnent
        /whoami
        /whois [name]
        /msg [name]
        /help [command]
        /people # TODO: Add back to test
        /chatroom
        /set [property] [value]

    properties list:
        - name
        - description

    Background: I am connected to the chat server
        Given I came connected to the chat server as person1

    Scenario: Disconnecting from the chat
        When the client sends "/disconnect"
        Then the client should receive disconnect
        And the client socket should be disconnected

    Scenario Outline: Commands that do not involve other clients
        When the client sends <command>
        Then the client should receive <response>
        
    Examples: Commands and responses
        | command             | response             |
        | /whoami             | person1              |
        | /help               | Command List |
        | /help whoami        | /whoami  |
        | /help whois         | /whois |
        | /help disconnect    | /disconnect  |
        | /help msg           | /msg [name]    |
        | /help help          | help [command]              |
        | /help people        | /people      |
        | /help chatroom      | /chatroom     |
        | /help set           | /set [property] [value]  |


    Scenario Outline: Commands that involve other clients
        Given person2 is in the chatroom
        When the client sends <command>
        Then the client should receive <response>

    Examples: Commands with proper arguements
        | command                 | response            |
        | /whois person2          | person2's ip is     | 
        | /msg person2            | I got you msg!      |
        | /people                 | person2             |
        | /set name marcus        | name: marcus        |
        | /set description I am me| description: I am me|

    Examples: Commands with wrong arguements
        | command      | response                     |
        | /who unknown | That person does not exist...| 
        | /msg unknown | That person does not exist...|
