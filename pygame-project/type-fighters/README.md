[YT Demo](https://youtu.be/c47-Zr_X_3s)

# How to use:

Run `python3 server.py` in a terminal, then run `python3 client.py` in a different terminal. A game window should pop up. Like this

![A video game window. In the window there is a grid of letters and the top leftmost letter is highlighted](https://user-images.githubusercontent.com/74327187/176988663-75eb02e1-2aad-423c-93ad-7612b3f7a9c2.png)

Your current position is indicated by the blue square, and you can type the letters that are adjacent to the square in order to move the square. So it's a typing game.

![The same video game. The original letter is not highglighted, but a different letter is highlighted.](https://user-images.githubusercontent.com/74327187/176988668-6efbd3dd-fdea-4cf1-bdba-de530114ad8b.png)
![The highlight moves once again.](https://user-images.githubusercontent.com/74327187/176988675-34b08340-a7b3-4151-8057-99dffb36141a.png)

I attempted to implement multiplayer, but it crashes if you try to open a second client. So there is no game unfortunately. The demo also shows a bug which I just discovered, which is that you can "clip" through diagonals by inputting horizontal and vertical motions simultaneously.

# Other

I may have included unnecessary things in `requirements.txt`
