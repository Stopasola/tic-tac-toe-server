# Tic-tac-toe Server

> Status: Developed ✔️

## Description

The objective of this project is to implement a protocol for the Tic-tac-toe using a hybrid client/server and Peer-to-Peer architecture. Initially, players must
register on a server informing their name and the port number on which they will be
waiting for connections. The server IP address and port are known and entered manually
by the player at the beginning of program execution.

The server must store and make available a list of connected players containing
the name, the IP address (the same one used when connecting to the server) and the
port informed by the player. A player must contact his opponent to start the game
using the server information.

For standardize the application, a text mode protocol was defined, which must be followed by all
implementations. This protocol has the following specifications:

## Protocol

## UDP service

1) Communication between players and server 

* USER port name

UDP message sent periodically (every 10 seconds) by the player to the
server indicating its presence in the system. The name consists of a single string of
characters and can contain letters, numbers and _ (underscore). The port parameter indicates in which player port will accept TCP connections from other players.

The successful registration is confirmed by the USER OK message. Attempts to record
players with invalid parameters are refused with the message USER NOK. Each host
(IP address) can register a single player. Registering a new player from the same host
implies the automatic replacement of the previous one. If the server does not receive the message  announcement after 1 minute, the player is removed by the server from the list of active players.

## LIST

UDP message used by the player to get the updated list of registered players in the
server. 
The return is LIST N <player_1> <player_2> .. <player_n>. 

The parameter N informs the number of players in the list. Each player is identified by

name:IPaddress:port.

## EXIT

UDP message sent from player to server indicating player is leaving
system. The absence of USER messages after 1 (one) minute has the same effect.

## TCP service

## START name

TCP message sent by player A to player B when A wants to communicate
with B. The name parameter refers to player A. The answer must be START OK for
confirm game start or BYE to indicate decline.

## BYE
TCP message sent by player A to player B indicating that player B is refusing
game (after a START message) or leaving the game in progress (at any time).

## PLAY row column
TCP message sent by the player to indicate his move. row and column refer
to the position on the board that the player wants to mark, being 0≤ row, column <3.
A valid move is confirmed with PLAY OK. An indication of incorrect play (outside of
board limits or at an already marked position) must be refused with the PLAY message
NOK, indicating that the player must retake the move. Three consecutive incorrect plays
imply the cancellation of the game with the sending of BYE by the player who is waiting for the
play.
After each valid move (with PLAY OK confirmation from the opponent) the system checks for
winner or tie and informs the local player.  
