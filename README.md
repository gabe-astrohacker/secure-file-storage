This is an A-level project that has been refactored in Oct/Nov 2024. 

Due to that, there are several shortcomings in the design and implementation of this project that I have attempted to minimise.

This project is a secure file sharing system concept where the backend is split into a "public server" (Server.py and ./server_folder) and its "private" counterpart (database).

Conceptually, the public server stores files that have already been encrypted by the user and allows the user to communicate with the private server. Any communication between these two would be end-to-end encrypted. 
The result is to ensure file security, even if the public server is breached. 
In practice this end-to-end encryption has not been implemented so the backend looks like a Server python class with unrestricted access to all information. 


To Run:
Start backend: 
1. Install MariaDB and ensure database created correctly (spec in Backend/Database.py)
2. python3 Backend/Server.py

Start frontend: 
1. Change IP address of Client.py to backend host ip (printed in command line)
2. python3 Frontend/LogInPage.py

Possible security improvements:
1. Use TLS to secure connection 
2. Use AES encryption instead of vernam cypher
3. Host database in a separate VM to isolate from public server
4. Hash passwords
5. Ensure SQL injection resilience
6. 2-step authentication

Other improvements:
1. Deletion of files and users features
2. Improve UI
3. Change personal details feature
4. Deploy publicly
5. Folder upload
6. File/folder sharing and permission management

