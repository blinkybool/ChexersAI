from game_details import *

NUM_PIECES = "NUM_PIECES"
NUM_EXITED = "NUM_EXITED"
NUM_CAN_EXIT = "NUM_CAN_EXIT"
NUM_THREATS = "NUM_THREATS"
NUM_PROTECTS = "NUM_PROTECTS"
NUM_DANGERED = "NUM_DANGERED"
TOTAL_DIST = "TOTAL_DIST"

STANDARD = "STANDARD" 
EXITING = "EXITING"
NEED_MORE = "NEED_MORE"
LAST_AND_NEED_MORE = "LAST_AND_NEED_MORE"
HAVE_1_EXTRA = "HAVE_1_EXTRA"
HAVE_SOME_EXTRA = "HAVE_SOME_EXTRA"
HAVE_LOTS_EXTRA = "HAVE_LOTS_EXTRA"

WEIGHTS = { NUM_PIECES: 4,
            NUM_EXITED: 5.5,
            NUM_CAN_EXIT: 1,
            NUM_THREATS: 0.1,
            NUM_DANGERED: -0.1,
            TOTAL_DIST: -1,
            NUM_PROTECTS: 0.05}


##### mode multipliers #####

STRATEGIES = {
STANDARD: {NUM_PIECES: 1,
            NUM_EXITED: 1,
            NUM_CAN_EXIT: 1,
            NUM_THREATS: 1,
            NUM_DANGERED: 1,
            TOTAL_DIST: 1,
            NUM_PROTECTS: 1},

EXITING: { NUM_PIECES: 1,
            NUM_EXITED: 1.2,
            NUM_CAN_EXIT: 1.2,
            NUM_THREATS: 0.5,
            NUM_DANGERED: 1,
            TOTAL_DIST: 1.2,
            NUM_PROTECTS: 0},

NEED_MORE: { NUM_PIECES: 3,
              NUM_EXITED: 0,
              NUM_CAN_EXIT: 0,
              NUM_THREATS: 1,
              NUM_DANGERED: 2,
              TOTAL_DIST: 0.5,
              NUM_PROTECTS: 1},

LAST_AND_NEED_MORE: { NUM_PIECES: 4,
                       NUM_EXITED: 0,
                       NUM_CAN_EXIT: 0,
                       NUM_THREATS: 2,
                       NUM_DANGERED: 10,
                       TOTAL_DIST: 0.05,
                       NUM_PROTECTS: 1},

HAVE_1_EXTRA: { NUM_PIECES: 0.9,
                 NUM_EXITED: 1.1,
                 NUM_CAN_EXIT: 1.1,
                 NUM_THREATS: 0.9,
                 NUM_DANGERED: 0.9,
                 TOTAL_DIST: 1.1,
                 NUM_PROTECTS: 1},

HAVE_SOME_EXTRA: { NUM_PIECES: 0.8,
                 NUM_EXITED: 1.2,
                 NUM_CAN_EXIT: 1.2,
                 NUM_THREATS: 0.8,
                 NUM_DANGERED: 0.8,
                 TOTAL_DIST: 1.2,
                 NUM_PROTECTS: 1},

HAVE_LOTS_EXTRA: { NUM_PIECES: 0.7,
                    NUM_EXITED: 1.3,
                    NUM_CAN_EXIT: 1.3,
                    NUM_THREATS: 0.7,
                    NUM_DANGERED: 0.7,
                    TOTAL_DIST: 1.5,
                    NUM_PROTECTS: 1}

}


'''
BEST_POSSIBLE_EVAL: len(COORDINATES) * WEIGHTS[NUM_PIECES] \
                        + NUM_TO_WIN * WEIGHTS[NUM_EXITED]  \
                        + NUM_STARTING_PIECES * WEIGHTS[NUM_CAN_EXIT]  \
                        + len(COORDINATES) * WEIGHTS[NUM_THREATS]

WORST_POSSIBLE_EVAL = len(COORDINATES) * WEIGHTS[NUM_DANGERED] \
                        + sum(EXIT_DIST[RED].values()) * WEIGHTS[TOTAL_DIST]
'''