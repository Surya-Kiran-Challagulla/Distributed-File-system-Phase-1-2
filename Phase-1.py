######################################################################                    
#   Implementation of the CRUD operations.
######################################################################

        
        def createDirectory():
            global username, dirname
            print("\nPlease enter directory name")
            dirname = input()

            features = []
            features.append("createdir")
            features.append(username)
            features.append(dirname)
            print(features)
            features = pickle.dumps(features)
            client.send(features)
            #client.send(features.encode())
            data = client.recv(client_buffer)
            data = data.decode(encoding_format)

            client.send(features)
            data = client.recv(client_buffer)
            data = data.decode(encoding_format)
            print(data+"\n")


        def createFile():

            global username, dirname
            print("\nPlease enter directory name to create file")
            dirname = input()
            print("Please enter file name")
            filename = input()

            features = []
            features.append("createfile")
            features.append(username)
            features.append(dirname)
            features.append(filename)
            features = pickle.dumps(features)
            client.send(features)
            data = client.recv(client_buffer)
            data = data.decode(encoding_format)
            available_files.append("files/"+username+"/"+dirname+"/"+filename)

            client.send(features)
            print(data+"\n")                    


        def writeFile():

            global username, text
            global dirname
            print("\nPlease enter directory name to write data")
            dirname = input()
            print("Please enter file name")
            filename = input()
            print("Please enter file content")
            filetext = input()

            features = []
            features.append("writefile")
            features.append(username)
            features.append(dirname)
            features.append(filename)
            features.append(filetext)
            features = pickle.dumps(features)
            client.send(features)
            data = client.recv(client_buffer)
            data = data.decode()
            client.send(features)
            print(data+"\n")


        def readFile():
            global username, dirname

            print("\nPlease enter directory name to read file")
            dirname = input()
            print("Please enter file name to read it")
            filename = input()

            features = []
            features.append("readfile")
            features.append(username)
            features.append(dirname)
            features.append(filename)
            features = pickle.dumps(features)
            client.send(features)
            rec = client.recv(client_buffer)
            read_data = rec.decode()
#                 if '@' not in read_data:
            result = json.loads(read_data)
            status = result['status']
#                 request = None
#                 request = read_data[0]
#                 print(read_data[0])
#                 print(read_data[1])
#                 print(read_data[2])
            if status == "correct":
                data = result['data']
                print("File Content Showing in Below lines\n\n")
                print(data)
                print("File Contenet ended here=================================")
            else:
                print("Given file does not exists\n")

        def deleteFile():

            global username, dirname
            print("\nPlease enter directory name to delete a file")
            dirname = input()
            print("Please enter file name to delete it")
            filename = input()

            features = []
            features.append("deletefile")
            features.append(username)
            features.append(dirname+"/"+filename)
            features = pickle.dumps(features)
            client.send(features)
            data = client.recv(client_buffer)
            data = data.decode()
            if data == 'Given file deleted':
                for i in range(len(available_files)):
                    names = available_files[i]
                    names = names.replace("\\","/")
                    arr = names.split("/")
                    if arr[3] == filename:
                        del available_files[i]
            print(data+"\n")


        def renameFile():

            global username, text
            global dirname

            print("\nPlease enter directory name to rename a file")
            dirname = input()
            print("Please enter old file name for renaming")
            oldname = input()
            print("Please enter new file name to rename")
            newname = input()

            features = []
            features.append("renamefile")
            features.append(username)
            features.append(dirname)
            features.append(oldname)
            features.append(newname)
            features = pickle.dumps(features)
            client.send(features)
            data = client.recv(client_buffer)
            data = data.decode()
            for i in range(len(available_files)):
                names = available_files[i]
                names = names.replace("\\","/")
                arr = names.split("/")
                if arr[3] == oldname:
                    del available_files[i]
            available_files.append('files/'+username+"/"+dirname+"/"+newname)        
            print(data+"\n")


        def listFiles():
            print("\nAvailable files for this user: "+username+"\n\n")
            for i in range(len(available_files)):
                print(available_files[i])
            print()

        def readFiles():
            global username, available_files
            if len(available_files) > 0:
                available_files.clear()
            features = []
            features.append("listfiles")
            features.append(username)
            features = pickle.dumps(features)
            client.send(features)
            data = client.recv(10000)
            data = pickle.loads(data)
            for i in range(len(data)):
                available_files.append(data[i])
