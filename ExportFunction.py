import os
import ghidra.program.model.listing.CodeUnitIterator


currentProgram = state.getCurrentProgram()
functions = currentProgram.getFunctionManager().getFunctions(True)

# outputDir = "D:\\testproject\\functionextraction"
outputDir = "D:\\testproject"
outputFileName = currentProgram.getName() + "_mod.txt"
outputFilePath = os.path.join(outputDir, outputFileName)

with open(outputFilePath, "w") as f:
    for function in functions:
        #func name
        f.write("{} ".format(function.getName()))
        #signature info
        signature = function.getSignature()
        if signature:
            arguments = signature.getArguments()
            f.write(str(len(arguments)))
            f.write(" ")
            for argument in arguments:
                paramType = argument.getDataType()
                f.write("{} ".format(paramType))
            # f.write("|")
        #parameter info
        # parameters = function.getParameters()
        # if parameters:
        #     f.write("Parameters:\n")
        #     parameterCount = len(parameters)
        #     f.write("Parameter count: {}\n".format(parameterCount))
        #     for param in parameters:
        #         paramName = param.getName()
        #         paramType = param.getDataType()
        #         f.write("Name: {}\tType: {}\n".format(paramName, paramType))
        #variable info 
        # stackFrame = function.getStackFrame()
        # if stackFrame:
        #     variableCount = stackFrame.getLocalSize()
        #     f.write("Variable count: {}\n".format(variableCount))
        #code unit info
        codeUnits = currentProgram.getListing().getCodeUnits(function.getBody(), True)
        while codeUnits.hasNext():
            codeUnit = codeUnits.next()
            f.write("{} ".format(codeUnit.toString()))
        f.write("\n")

print("finish extracting functions for "+ currentProgram.getName()+" !")