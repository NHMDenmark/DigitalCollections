# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022
@authors: Jan K. Legind, NHMD;
Copyright 2022 Natural History Museum of Denmark (NHMD)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
- Code for monitoring and renaming new csv files coming into the N:\SCI-SNM-DigitalCollections\DaSSCo\DigiApp\Data\0.ForChecking shared directory.
- Required a Windows machine to work due to the win32file and win32con dependencies.
"""

import os
import threading
import re
import time
import win32file
import win32con

ACTIONS = {
    1 : "Created"
    # 2 : "Deleted",
    # 3 : "Updated",
    # 4 : "Renamed from something",
    # 5 : "Renamed to something"
}

# Thanks to Claudio Grondi for the correct set of numbers
FILE_LIST_DIRECTORY = 0x0001


def watch(path, fn, excludes):
    # print("monitoring: %s" % path)
    hdir = win32file.CreateFile (
        path,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
        )
    while True:
        #
        # readdirectorychangesw takes a previously-created
        # handle to a directory, a buffer size for results,
        # a flag to indicate whether to watch subtrees and
        # a filter of what changes to notify.
        #
        # nb tim juchcinski reports that he needed to up
        # the buffer size to be sure of picking up all
        # events when a large number of files were
        # deleted at once.
        #
        results = win32file.ReadDirectoryChangesW (
            hdir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )

        excluded = True

        for action, file in results:
            full_filename = os.path.realpath(os.path.join (path, file))
            doneAction = ACTIONS.get(action, "unknown")
            print(full_filename, doneAction)
            if doneAction == 'Created':
                # Should rename the file to name[_original].csv
                tokenName = full_filename.split('\\')
                print(tokenName)
                fileName = tokenName.pop()
                pathName = '\\'.join(tokenName) # path to file minus the file name itself
                print('pathname=', pathName)
                splitName = fileName.split('.')
                renamed = f"{splitName[0]}_original.csv"
                completeRename = f"{pathName}\{renamed}"
                print('renamed name:', completeRename)
                # completeRename = f"{}"
                os.rename(full_filename, completeRename)

            # find if file and is not excluded by any excludes
            if not os.path.isdir(full_filename):
                if excluded:
                    excluded = any([re.search(e, full_filename) for e in excludes])

        if not excluded:
            fn()

def onchange(path, fn, excludes=[]):
# def onchange(path, excludes=[]):
    """ Calls 'fn' when there is any change in the path """
    thread = threading.Thread(target = lambda: watch(path, fn, excludes))
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    path = r'N:\SCI-SNM-DigitalCollections\DaSSCo\DigiApp\Data\0.ForChecking'
    while True:
        ch = onchange(path, lambda: print('i see a change'), ['pyc$', '.log$'])
        time.sleep(2)