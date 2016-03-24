#!/usr/bin/env python3

import sys
import signal
import gameboard
import filereader
import constraint
import constraintnetwork
import btsolver
import time


def signal_handler(signum, frame):
    """ Limit excution time of a function call """
    raise Exception("Timed out!")


def printSolverStats(solverObj, totalStart, isTimeOut):
    output = "TOTAL_START=" + str(time.asctime(time.localtime(totalStart)))

    if solverObj.preprocessing_startTime != 0:
        output += "\nPREPROCESSING_START=" + str(time.asctime(time.localtime(solverObj.preprocessing_startTime)))
        output += "\nPREPROCESSING_DONE=" + str(time.asctime(time.localtime(solverObj.preprocessing_endTime)))
    else:
        output += "\nPREPROCESSING_START=0"
        output += "\nPREPROCESSING_DONE=0"

    output += "\nSEARCH_START=" + str(time.asctime(time.localtime(solverObj.startTime)))
    output += "\nSEARCH_DONE=" + str(time.asctime(time.localtime(solverObj.endTime)))
    output += "\nSOLUTION_TIME=%.7f" % ((solverObj.preprocessing_endTime - solverObj.preprocessing_startTime)
                                            + (solverObj.endTime-solverObj.startTime))

    if isTimeOut:
        output += "\nSTATUS=timeout"
    elif solverObj.hassolution:
        output += "\nSTATUS=success"
    else:
        output += "\nSTATUS=error"

    # print(self.gameboard.board)
    output += "\nSOLUTION=("
    for i in solverObj.gameboard.board:
        for j in i:
            # output += str(j) + ","
            output += gameboard.INTTOODOMETER[j] + ","
    output = output[:-1]
    output += ")"

    output += "\nCOUNT_NODES=" + str(solverObj.numAssignments)
    output += "\nCOUNT_DEADENDS=" + str(solverObj.numBacktracks)
    output += "\n" + str(solverObj.gameboard)

    return output


if __name__ == '__main__':
    # Check command-line arguments.
    print('Python version:', sys.version)

    # GB = gameboard.GameBoard(12,3,4,[[0 for j in range(12)] for i in range(12)])
    # print(GB)

    TOTAL_START = time.time()
    sudokudata = filereader.SudokuFileReader(sys.argv[1])
    print(sudokudata)
    # cn = filereader.GameBoardToConstraintNetwork(sudokudata)
    # print(cn)
    solver = btsolver.BTSolver(sudokudata)

    # solver.setConsistencyChecks(btsolver.ConsistencyCheck['None'])
    # solver.setValueSelectionHeuristic(btsolver.ValueSelectionHeuristic['None'])
    # solver.setVariableSelectionHeuristic(btsolver.VariableSelectionHeuristic['None'])

    if len(sys.argv) < 4:
        raise ValueError("Program did not received enough correct argument.")

    if len(sys.argv) == 4 or 'BT' in sys.argv:
        print("Default option tokens detected: Backtracking Search (BT)")

    if 'FC' in sys.argv:
        print("FC tokens detected:  Forward Checking (FC)")
        solver.setConsistencyChecks(btsolver.ConsistencyCheck['ForwardChecking'])

    if 'MRV' in sys.argv and 'DH' not in sys.argv:
        print("MRV tokens detected:  Minimum Remaining Values (MRV)")
        solver.setVariableSelectionHeuristic(btsolver.VariableSelectionHeuristic['MinimumRemainingValue'])

    if 'DH' in sys.argv and 'MRV' not in sys.argv:
        print("DH tokens detected:  Degree Heuristic (DH)")
        solver.setVariableSelectionHeuristic(btsolver.VariableSelectionHeuristic['Degree'])

    if 'MRV' in sys.argv and 'DH' in sys.argv:
        print("Both MRV and DH tokens detected:  Minimum Remaining Values (MRV) and Degree Heuristic (DH)")
        solver.setVariableSelectionHeuristic(btsolver.VariableSelectionHeuristic['MRVandDH'])

    if 'LCV' in sys.argv:
        print("LCV tokens detected:  Least Constraining Value (LCV)")
        solver.setValueSelectionHeuristic(btsolver.ValueSelectionHeuristic['LeastConstrainingValue'])

    if 'AC' in sys.argv:
        print("AC tokens detected:  Arc Consistency (AC)")
        solver.setConsistencyChecks(btsolver.ConsistencyCheck['ArcConsistency'])


    isTimeOut = False
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(sys.argv[3]))
    try:
        solver.solve()
    except Exception:
        isTimeOut = True
        solver.endTime = time.time()
        print ("Timed out by " + sys.argv[3] + " seconds !!!")

    print(printSolverStats(solver, TOTAL_START, isTimeOut))

    with open(sys.argv[2], "w") as outfile:
        outfile.write(printSolverStats(solver, TOTAL_START, isTimeOut))
