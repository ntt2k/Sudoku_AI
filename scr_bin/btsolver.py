import filereader
import gameboard
import variable
import domain
import trail
import constraint
import constraintnetwork
import time
import functools
# import math

class VariableSelectionException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def handleError(e):
    print(e)


VariableSelectionHeuristic = {'None': 0, 'MinimumRemainingValue': 1,
                              'Degree': 2,
                              'MRVandDH': 3}
ValueSelectionHeuristic = {'None': 0, 'LeastConstrainingValue': 1}
ConsistencyCheck = {'None': 0, 'ForwardChecking': 1, 'ArcConsistency': 2}


class BTSolver:
    "Backtracking solver"

    # Constructors Method #
    def __init__(self, gb):
        self.network = filereader.GameBoardToConstraintNetwork(gb)
        self.trail = trail.masterTrailVariable
        self.hassolution = False
        self.gameboard = gb

        self.numAssignments = 0
        self.numBacktracks = 0
        self.preprocessing_startTime = 0
        self.preprocessing_endTime = 0
        self.startTime = None
        self.endTime = None

        self.varHeuristics = 0
        self.valHeuristics = 0
        self.cChecks = 0
        # self.runCheckOnce = False

    # Modifiers Method #
    def setVariableSelectionHeuristic(self, vsh):
        self.varHeuristics = vsh

    def setValueSelectionHeuristic(self, vsh):
        self.valHeuristics = vsh

    def setConsistencyChecks(self, cc):
        self.cChecks = cc

    # Accessors Method #
    def getSolution(self):
        return self.gameboard

    # @return time required for the solver to attain in seconds
    def getTimeTaken(self):
        return self.endTime-self.startTime

    # Helper Method #
    def checkConsistency(self):
        if self.cChecks == 0:
            return self.assignmentsCheck()
        elif self.cChecks == 1:
            return self.forwardChecking()
        elif self.cChecks == 2:
            return self.arcConsistency()
        else:
            return self.assignmentsCheck()

    def assignmentsCheck(self):
        """
            default consistency check. Ensures no two variables are assigned to the same value.
            @return true if consistent, false otherwise.
        """
        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == vOther.getAssignment():
                        return False
        return True

    def forwardChecking(self):
        """
            TODO: Implement forward checking.
        """
        # print("---------------------------------")
        # print("FORWARDCHECKING BEGIN TO CALL ...")

        # print("self.network.variables:")
        # for i in self.network.variables:
        #     print(i)
        # print("----------")

        for v in self.network.variables:
            if v.isAssigned():
                # print("v.isAssigned() in check process --> " + str(v))

                # print("self.network.getNeighborsOfVariable(v) in check process : ")
                # for i in self.network.getNeighborsOfVariable(v):
                    # print(i)
                # print("~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.")

                for vOther in self.network.getNeighborsOfVariable(v):
                    # print("vOther in check process --> " + str(vOther))

                    if v.getAssignment() == vOther.getAssignment():
                        # print("return False because v.getAssignment() == vOther.getAssignment()")
                        return False

                    # print("-->CALL vOther.removeValueFromDomain(v.getAssignment())")
                    vOther.removeValueFromDomain(v.getAssignment())
                    # print("Updated vOther after remove progress: " + str(vOther))

                    if vOther.domain.size() == 0:
                        # print("return False because vOther.domain.size() == 0")
                        return False

        # print("end loop return True")
        return True


    def arcConsistency(self):
        """
            TODO: Implement Maintaining Arc Consistency.
        """

        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == vOther.getAssignment():
                        return False
                    vOther.removeValueFromDomain(v.getAssignment())
                    if vOther.domain.size() == 0:
                        return False

                for v2 in self.network.variables:
                    if v2.isAssigned():
                        for vOther2 in self.network.getNeighborsOfVariable(v2):
                            if v2.getAssignment() == vOther2.getAssignment():
                                return False
                            vOther2.removeValueFromDomain(v2.getAssignment())
                            if vOther2.domain.size() == 0:
                                return False
        return True


    def selectNextVariable(self):
        """
            Selects the next variable to check.
            @return next variable to check. null if there are no more variables to check.
        """
        if self.varHeuristics == 0:
            return self.getfirstUnassignedVariable()
        elif self.varHeuristics == 1:
            return self.getMRV()
        elif self.varHeuristics == 2:
            return self.getDegree()
        elif self.varHeuristics == 3:
            return self.getMRVandDH()
        else:
            return self.getfirstUnassignedVariable()

    def getfirstUnassignedVariable(self):
        """
            default next variable selection heuristic. Selects the first unassigned variable.
            @return first unassigned variable. null if no variables are unassigned.
        """
        for v in self.network.variables:
            if not v.isAssigned():
                return v
        return None

    def getMRV(self):
        """
            TODO: Implement MRV heuristic
            @return variable with minimum remaining values that isn't assigned, None if all variables are assigned.
        """
        returnVar = None
        minRemainingValues = float('inf')
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() < minRemainingValues:
                    returnVar = v
                    minRemainingValues = v.domain.size()

        return returnVar

    def getDegree(self):
        """
            TODO: Implement Degree heuristic
            @return variable constrained by the most unassigned variables, null if all variables are assigned.
        """
        returnVar = None
        maxUnassignedNeighbors = float('-inf')
        for v in self.network.variables:
            if not v.isAssigned():
                variableNeighbors = self.network.getNeighborsOfVariable(v)

                # Only include variables that have not been assigned
                numUnassignedNeighbors = 0
                for i in variableNeighbors:
                    if not i.isAssigned():
                        numUnassignedNeighbors += 1

                if numUnassignedNeighbors > maxUnassignedNeighbors:
                    returnVar = v
                    maxUnassignedNeighbors = numUnassignedNeighbors

        return returnVar

    def getMRVandDH(self):
        """
            Both MRV and DH
        """
        returnVar = None
        minRemainingValues = float('inf')
        unassignedVariablesList = []
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() < minRemainingValues:
                    returnVar = v
                    minRemainingValues = v.domain.size()

        # add all the tie MRV into unassignedVariablesList
        unassignedVariablesList.append(returnVar)
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() == minRemainingValues:
                    unassignedVariablesList.append(v)

        # using Degree Heuristics to do tie breaking
        if len(unassignedVariablesList) > 1:
            returnVar = None
            maxUnassignedNeighbors = float('-inf')
            for v in unassignedVariablesList:
                variableNeighbors = self.network.getNeighborsOfVariable(v)

                # Only include variables that have not been assigned
                numUnassignedNeighbors = 0
                for i in variableNeighbors:
                    if not i.isAssigned():
                        numUnassignedNeighbors += 1

                if numUnassignedNeighbors > maxUnassignedNeighbors:
                    returnVar = v
                    maxUnassignedNeighbors = numUnassignedNeighbors

        return returnVar

    def getNextValues(self,v):
        """
            Value Selection Heuristics. Orders the values in the domain of the variable
            passed as a parameter and returns them as a list.
            @return List of values in the domain of a variable in a specified order.
        """
        if self.valHeuristics == 0:
            return self.getValuesInOrder(v)
        elif self.valHeuristics == 1:
            return self.getValuesLCVOrder(v)
        else:
            return self.getValuesInOrder(v)

    def getValuesInOrder(self, v):
        """
            Default value ordering.
            @param v Variable whose values need to be ordered
            @return values ordered by lowest to highest.
        """
        values = v.domain.values
        # print("DEBUG normal ValuesInOrder:",values)
        return sorted(values)

    # def compareLCV(self,v1, v2):
    #     """
    #         Support utility function to compare LCV
    #     """
        # listConstraintV1 = self.network.getConstraintsContainingVariable(v1)
        # print("DEBUG listConstraintV1:",listConstraintV1)
        # listConstraintV2 = self.network.getConstraintsContainingVariable(v2)
        # print("DEBUG listConstraintV2:",listConstraintV2)
        # return len(listConstraintV1) - len(listConstraintV2)

    def getValuesLCVOrder(self, v):
        """
            TODO: LCV heuristic
        """
        values = v.domain.values
        # print("DEBUG normal ValuesInOrder:",values)
        # result = sorted(values, key=functools.cmp_to_key(self.compareLCV))
        def compareLCV(v1,v2):
            """
                Support utility function to compare LCV
            """
            numConstraintV1 = 0
            numConstraintV2 = 0
            for i in self.network.getNeighborsOfVariable(v):
                if i.domain.contains(v1):
                    numConstraintV1 += 1
                if i.domain.contains(v2):
                    numConstraintV2 += 1
            return numConstraintV1 - numConstraintV2

        result = sorted(values, key=functools.cmp_to_key(compareLCV))
        # print("DEBUG sorted LCV:",result)
        return result


    def success(self):
        """ Called when solver finds a solution """
        self.hassolution = True
        self.gameboard = filereader.ConstraintNetworkToGameBoard(self.network,
                                                                 self.gameboard.N,
                                                                 self.gameboard.p,
                                                                 self.gameboard.q)

    # Solver Method #
    def solve(self):
        """ Method to start the solver """
        self.startTime = time.time()
        try:
            self.solveLevel(0)
        except VariableSelectionException:
            print("Error with variable selection heuristic.")
        self.endTime = time.time()
        self.trail.trailStack = []

    def solveLevel(self, level):
        """
            Solver Level
            @param level How deep the solver is in its recursion.
            @throws VariableSelectionException
        """
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")
        # print("BEFORE ANY SOLVE LEVEL START")
        # print(self.network)
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

        if self.hassolution:
            return

        # Select unassigned variable
        v = self.selectNextVariable()
        # print("V SELECTED --> " + str(v))

        # check if the assigment is complete
        if(v == None):
            # print("!!! GETTING IN V == NONE !!!")
            for var in self.network.variables:
                if not var.isAssigned():
                    raise VariableSelectionException("Something happened with the variable selection heuristic")
                    # print("Something happened with the variable selection heuristic")
            self.success()
            return

        # loop through the values of the variable being checked LCV
        # print("getNextValues(v): " + str(self.getNextValues(v)))
        for i in self.getNextValues(v):
            # print("next value to test --> " + str(i))
            self.trail.placeTrailMarker()

            # check a value
            # print("-->CALL v.updateDomain(domain.Domain(i)) to start to test next value.")
            v.updateDomain(domain.Domain(i))
            self.numAssignments += 1

            # move to the next assignment
            if self.checkConsistency():
                self.solveLevel(level + 1)

            # if this assignment failed at any stage, backtrack
            if not self.hassolution:
                # print("=======================================")
                # print("AFTER PROCESSED:")
                # print(self.network)
                # print("================ ")
                # print("self.trail before revert change: ")
                # for i in self.trail.trailStack:
                #     print("variable --> " + str(i[0]))
                #     print("domain backup --> " + str(i[1]))
                # print("================= ")

                self.trail.undo()
                self.numBacktracks += 1
                # print("REVERT CHANGES:")
                # print(self.network)
                # print("================ ")
                # print("self.trail after revert change: ")
                # for i in self.trail.trailStack:
                #     print("variable --> " + str(i[0]))
                #     print("domain backup --> " + str(i[1]))
                # print("================= ")

            else:
                return
