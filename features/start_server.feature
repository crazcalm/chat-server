Feature: Startig the Chat Server
    The chat server should have a one of more customizable options.

    1. I should be able to pass in the port number
    2. Give the chatroom a name

    Scenario Outline: Starting the server with different ports
        Given I want to use port <port_number>
        When I start the chat server
        Then running the server should have <result> in its output

    Examples: Open ports
        | port_number | result   |
        | 3333        | "success"|

