# Wrapper module for waagent
#
# waagent is not written as a module. This wrapper module is created 
# to use the waagent code as a module.
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import imp as imp
except ImportError:
    import importlib as imp
import os
import os.path

#
# The following code will search and load waagent code and expose
# it as a submodule of current module
#
def searchWAAgent():
    agentPath = os.path.join(os.getcwd(), "./WaagentLib.py")
    if(os.path.isfile(agentPath)):
        return agentPath
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    for user_path in user_paths:
        agentPath = os.path.join(user_path, 'waagent')
        if(os.path.isfile(agentPath)):
            return agentPath
    return None

def searchWAAgentOld():
    agentPath = '/usr/sbin/waagent'
    if(os.path.isfile(agentPath)):
        return agentPath
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    for user_path in user_paths:
        agentPath = os.path.join(user_path, 'waagent')
        if(os.path.isfile(agentPath)):
            return agentPath
    return None

pathUsed = 1 
try:
    agentPath = searchWAAgent()
    if(agentPath):
        waagent = imp.load_source('waagent', agentPath)
    else:
        raise Exception("Can't load new waagent.")
except Exception as e:
    pathUsed = 0 
    agentPath = searchWAAgentOld()
    if(agentPath):
        waagent = imp.load_source('waagent', agentPath)
    else:
        raise Exception("Can't load old waagent.")

if not hasattr(waagent, "AddExtensionEvent"):
    """
    If AddExtensionEvent is not defined, provide a dummy impl.
    """
    def _AddExtensionEvent(*args, **kwargs):
        pass
    waagent.AddExtensionEvent = _AddExtensionEvent

if not hasattr(waagent, "WALAEventOperation"):
    class _WALAEventOperation:
        HeartBeat = "HeartBeat"
        Provision = "Provision"
        Install = "Install"
        UnIsntall = "UnInstall"
        Disable = "Disable"
        Enable = "Enable"
        Download = "Download"
        Upgrade = "Upgrade"
        Update = "Update"           
    waagent.WALAEventOperation = _WALAEventOperation

__ExtensionName__ = None
def InitExtensionEventLog(name):
    __ExtensionName__ = name

def AddExtensionEvent(name=__ExtensionName__,
                      op=waagent.WALAEventOperation.Enable, 
                      isSuccess=False, 
                      message=None):
    if name is not None:
        waagent.AddExtensionEvent(name=name,
                                  op=op,
                                  isSuccess=isSuccess,
                                  message=message)

def GetPathUsed():
    return pathUsed

