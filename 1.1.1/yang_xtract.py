"""
Copyright (c) 2015,  BROCADE COMMUNICATIONS SYSTEMS, INC

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
 are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""

import sys


if __name__ == "__main__":
    nspaces = []
    inSchema = False
    nsFound = False
    dulicate = False
    linesSoFar = ""

    with open('karaf.log') as fp:
        for line in fp:
            line = line.replace("&#13;","")
            if inSchema:

                if not line.strip():
                    continue

                if not moduleName:
                    if "module" in line:
                        moduleInfo = line.split()
                        moduleName = moduleInfo[1] 

                if "</data>" in line:
                    if "}" in line:
                        linesSoFar = linesSoFar + "}"

                    inSchema = False
                    if moduleName not in nspaces:
                        nspaces.append(moduleName)
                        duplicate = False
                    else:
                        print "Duplicate: " + moduleName
                        duplicate = True

                    if moduleName and not duplicate:
                        moduleFileName = moduleName + ".yang"
                        f = open(moduleFileName, 'w')
                        f.write(linesSoFar)
                        f.close()
                        linesSoFar = ""
                        moduleName = ""
                        continue

                if not duplicate:
                    linesSoFar = linesSoFar + line

                # if "namespace " in line:
                #     parts = line.split()
                #     nsFound = True
                #     nameSpace = parts[1]
                #     if nameSpace not in nspaces:
                #         nspaces.append(nameSpace)
                #         duplicate = False
                #     else:
                #         duplicate = True

            elif "<data " in line:
                 inSchema = True
                 nsFound = False
                 duplicate = False
                 moduleName = ""
                 linesSoFar = "" 
                 parts = line.split(">",1)
                 leftover = parts[1]
                 leftover = leftover.lower()
                 print line
                 if "module" in leftover:
                    linesSoFar = parts[1]
                    moduleInfo = leftover.split()
                    moduleName = moduleInfo[1]
                 elif "/*" in parts[1]:
                    linesSoFar = parts[1]

