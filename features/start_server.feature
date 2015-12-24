Feature: Startig the Chat Server
    The chat server should have a one of more customizable options.

    1. I should be able to pass in the port number
    2. Give the chatroom a name

    Scenario Outline: Starting the server with different ports
        Given I want to use port <port_number>
        When I start the chat server
        Then running the server should <result>

    Examples: Open ports
        | port_number | result   |
        | 3333        | "success"|

    Examples: Non-open ports
        | port_number | result   |
        | 80          | "failure"|
