"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    """

    print ('')
    print('Started custom score....')
    print ('')
    print(game)
    print(player)
    print ('')
    print('Ended custom score....')
    """

    # TODO: finish this function!
    #raise NotImplementedError

    # there is a better way.. but I don't know it!!!

    return float(len(game.get_legal_moves(player)))

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        #=======>  start


        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # if there are no legal moves, return
        if not legal_moves:
            return (-1, -1)

        # let us start with iterative deepening - first move    
        move = legal_moves[0]    

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if not self.iterative:

                # if not iterative deepening defined, go for level 1
                (score, selected_move) = self.alphabeta(game, 1)
            
            else:

                # if iterative deepening defined, keep lowereing till quiesce or run out of time

                targetlevel = 1
 
                selected_move = (-1,-1)

                (score, newmove) = self.alphabeta(game, depth=targetlevel)

                while newmove != selected_move: # if moves are the same, achieved quiescence
                    selected_move = newmove # save move
                    (score, newmove ) = self.alphabeta(game, depth=targetlevel)

                # if newmove == move:
                    # print ('quiesced at: ' + str(score) + ' move ' + str(move))

        except Timeout:
            # Handle any actions required at timeout, if necessary

            print(' ===> I have timed out with move ' + str(selected_move) + " in level " + str(targetlevel))
            if selected_move:
                return selected_move
            
        # Return the best move from the last completed search iteration
        return move

        # raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):

        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # raise NotImplementedError

        
        try:

            available_moves = game.get_legal_moves()

            # if no more moves left
            if not available_moves or self.search_depth < depth :

                if maximizing_player:
                    # I win
                   return (float("inf"), (-1,-1) )
                else:
                    # I lose
                   return (float("-inf"), (-1,-1) )


            if  game.move_count  <= depth and depth > 1:

                move = (float("-inf"), available_moves[0])  #  initializing it...
                for m in available_moves:

                    score,_ = self.minimax(game.forecast_move(m), depth, not(maximizing_player))

                    if score > move[0]:
                        move = (score, m)                       

            else: 

                move = (float("-inf"), available_moves[0])  #  initializing it...
                for m in available_moves:
                    score = self.score(game.forecast_move(m),self)
                    if score > move[0]:
                        move = (score, m) 

            return move

        except Timeout:

            # Handle any actions required at timeout, if necessary
            if move:
                return move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """
        Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # raise NotImplementedError


        try:


            available_moves = game.get_legal_moves()

            # if no more moves left
            if not available_moves:
                return ( game.utility, (-1,-1) )

            if depth == 0:
                return (self.score(game,self), available_moves[0])

            if  maximizing_player:

                move = (float("-inf"), available_moves[0])  #  initializing it...

                for m in available_moves:

                    score,_ = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, not(maximizing_player))

                    if score > move[0]:
                        move = (score, m)                       
                    
                    alpha = max(alpha,score)

                    if beta <= alpha: 
                       break


            else: 

                move = (float("inf"), available_moves[0])  #  initializing it...

                for m in available_moves:
                    score,_ = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, not(maximizing_player))

                    if score < move[0]:
                        move = (score, m)                       
                    
                    beta = min(beta,score)

                    if beta <= alpha: 
                       break

            return move

        except Timeout:

            # Handle any actions required at timeout, if necessary
            if move:
                return move


    def old_alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """
        Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # raise NotImplementedError


        try:

            available_moves = game.get_legal_moves()

            # if no more moves left
            if not available_moves or self.search_depth < depth :
                if maximizing_player:
                    # I win
                   return (float("inf"), (-1,-1) )
                else:
                    # I lose
                   return (float("-inf"), (-1,-1) )


            if  game.move_count  <= depth and depth > 1:

                move = (alpha, available_moves[0])  #  initializing it...
                for m in available_moves:
                    score,_ = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, not(maximizing_player))

                    if score > alpha:
                        alpha = score


                    if score > move[0]:
                        move = (score, m)                       
                    else:
                        if score < alpha:
                             print( '... will prune ' + str(alpha) + ' : ' + str(score) + ' ' + str(m))
                             break






            else: 

                move = (alpha, available_moves[0])  #  initializing it...

                # if game.move_count == 4:
                    #print('check game')
                    #print(game.to_string())
                    #print('available moves' + str(available_moves))

                for m in available_moves:
                    score = self.score(game.forecast_move(m),self)

                    if score > alpha:
                        alpha = score

                    if score > move[0]:
                        move = (score, m) 
                        # print( 'My best move is ' + str(move))
                    else:
                        if score < alpha and depth > 1:
                            print( '... will prune ' + str(alpha) + ' : ' + str(score) + ' ' + str(m))
                            break

            return move

        except Timeout:

            # Handle any actions required at timeout, if necessary
            if move:
                return move

      
