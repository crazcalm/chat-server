Feature: Server Commands
    I want to list out the different commands that
    I want the server to respond to.

    list:
        /disconnent
        /whoami
        /whois [name]
        /msg [name], [msg]
        /help [command]
        /people
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
        | /set name Marcus     | Marcus |
        | /set name Marcus the great!| Marcus the great!|
        | /set description LOVE| LOVE   |
        | /set description Love yourself| Love yourself |
        | /chatroom            | Chat Room |

    Examples: Commands with wrong arguments
        | command     | response               |
        |/set name     | /set [property] [value]|
        |/set hair blue| /set [property] [value]|

    Scenario Outline: Commands that involve other clients
        Given person2 is in the chatroom
        When the client sends <command>
        Then the client should receive <response>

    Examples: Commands with proper arguements
        | command                 | response            |
        | /whois M          | friend     | 
        | /msg M, hi!| msg sent      |
        | /people                 | M             |

    Examples: Commands with wrong arguements
        | command      | response                     |
        | /whois unknown | I don't know|
        | /whois | /whois | 
        | /msg unknown, hi | Could not find|
        | /msg | /msg|
        | /msg M | /msg|
