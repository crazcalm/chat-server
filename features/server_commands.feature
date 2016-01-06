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
        | /whoami             | No Name              |
        | /help               | Command List |
        | /help whoami        | /whoami  |
        | /help whois         | /whois |
        | /help disconnect    | /disconnect  |
        | /help msg           | /msg [name]    |
        | /help help          | help [command]              |
        | /help people        | /people      |
        | /help chatroom      | /chatroom     |
        | /help set           | /set [property] [value]  |
        | set name Marcus     | Marcus |
        | set description LOVE| LOVE   |

    Scenario Outline: Commands that involve other clients
        Given person2 is in the chatroom
        When the client sends <command>
        Then the client should receive <response>

    Examples: Commands with proper arguements
        | command                 | response            |
        | /whois person2          | Player2     | 
        | /msg person2            | I got you msg!      |
        | /people                 | person2             |

    Examples: Commands with wrong arguements
        | command      | response                     |
        | /who unknown | That person does not exist...| 
        | /msg unknown | That person does not exist...|
