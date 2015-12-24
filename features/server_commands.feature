Feature: Server Commands
    I want to list out the different commands that
    I want the server to respond to.

    list:
        /disconnent
        /whoami
        /who [name]
        /msg [name]
        /help [command]
        /people
        /chatroom

    Background: I am connected to the chat server
        Given I came connected to the chat server as person1

    Scenario: Disconnecting from the chat
        When the client sends "/disconnect"
        Then the client should receive "disconnected"
        And the client socket should be disconnected

    Scenario Outline: Commands that do not involve other clients
        When the client sends <command>
        Then the client should receive <response>
        
    Examples: Commands and responses
        | command               | response                            |
        | "/whoami"             | "person1"                           |
        | "/help"               | "The list of commands"              |
        | "/help whoami"        | "/whoami returns your chatroom name"|
        | "/help who"           | "/who [name] returns the ip"        |
        | "/help disconnect"    | "/disconnect disconnects you from"  |
        | "/help msg"           | "/msg [name] allows you to send"    |
        | "/help help"          | "The list of commands"              |
        | "/help people"        | "/people returns the names of"      |
        | "/help chatroom"      | "/chatroom returns the name of"     |
        | "/people"             | "person1"                           |

    Scenario Outline: Commands that involve other clients
        Given person2 is in the chatroom
        When the client sends <command>
        Then the client should receive <response>

    Examples: Commands with proper arguements
        | command        | response          |
        | "/who person2" | "person2's ip is" | 
        | "/msg person2" | "I got you msg!"  |
        | "/people"      | "person2"         |

    Examples: Commands with wrong arguements
        | command        | response                       |
        | "/who unknown" | "That person does not exist..."| 
        | "/msg unknown" | "That person does not exist..."|
