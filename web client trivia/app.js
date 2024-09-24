    
let baseServerUrl = 'http://127.0.0.1'
document.addEventListener('DOMContentLoaded', function() {
    const app = document.getElementById('app');
    // Initial screen is Port input screen
    showPortInputScreen();

    // Screen 1: Port Input
    function showPortInputScreen() {
        app.innerHTML = `
            <h2>Enter Port Number</h2>
            <input type="number" id="portInput" placeholder="Enter port number" />
            <button id="nextToLogin">Next</button>
        `;

        document.getElementById('nextToLogin').addEventListener('click', () => {
            let port = document.getElementById('portInput').value;
            console.log(port);
            baseServerUrl = baseServerUrl + ':' + port;
            console.log(baseServerUrl);
            showLoginScreen();
        });
    }

    // Screen 2: Sign Up / Login
    function showLoginScreen() {
        app.innerHTML = `
            <h2>Sign Up or Login</h2>
            <input type="text" id="username" placeholder="Username" />
            <input type="email" id="email" placeholder="Email (for Sign Up)" />
            <input type="password" id="password" placeholder="Password" />
            <button id="login">Login</button>
            <button id="signUp">Sign Up</button>
        `;

        document.getElementById('login').addEventListener('click', async () => {
            let username =  document.getElementById('username').value;
            let password =  document.getElementById('password').value;
            if(username && password) {
                let response = await axios.post(baseServerUrl + '/Log-In', {
                    username, password
                });
                if(response.data[1] === 100)
                {
                    showMenuScreen();
                }
            }
        });

        document.getElementById('signUp').addEventListener('click', async() => {
            let username =  document.getElementById('username').value;
            let password =  document.getElementById('password').value;
            let email = document.getElementById('email').value;
            if(username && password && email) {
                let response = await axios.post(baseServerUrl + '/Sign-In', {
                    username, password, email
                });
                if(response.data[1] === 101)
                {
                    showMenuScreen();
                }
            }
        });
    }

    // Screen 3: Menu
    function showMenuScreen() {
        app.innerHTML = `
            <h2>Menu</h2>
            <button id="getRooms">Get Rooms</button>
            <button id="getStats">Get Personal Stats</button>
            <button id="getHighScores">Get High Scores</button>
            <button id="createRoom">Create Room</button>
            <button id="logout">Log Out</button>
            <br>
            <div id="data"></div>
        `;

        document.getElementById('getRooms').addEventListener('click', async() => {
            let {data} = await axios.get(baseServerUrl + '/Get-Rooms');
            console.log(data);
            const [json, status] = data;
            const dataContainer = document.querySelector('#data');
            dataContainer.innerHTML = ''; // Clear previous data
            let rooms = JSON.parse(json).Rooms
            rooms.forEach(room => {
                const roomInfo = `
                    <div class="room">
                        <p>Room Name: ${room.roomName}</p>
                        <p>Max Players: ${room.maxPlayers}</p>
                        <p>Number of Questions: ${room.numOfQuestions}</p>
                        <p>Question Timeout: ${room.qTimeout} seconds</p>
                        <p>Room Status: ${room.isActive ? "Active" : "Inactive"}</p>
                        <button class="joinRoomBtn" data-room-id="${room.roomId}">Join Room</button>
                        <button class="getPlayersBtn" data-room-id="${room.roomId}">Get Players in Room</button>
                    </div>
                `;
                dataContainer.innerHTML += roomInfo;
            });

            // Add event listeners for dynamically created buttons
            document.querySelectorAll('.joinRoomBtn').forEach(button => {
                button.addEventListener('click', (event) => {
                    const roomId = event.target.getAttribute('data-room-id');
                    joinRoom(roomId);
                });
            });

            document.querySelectorAll('.getPlayersBtn').forEach(button => {
                button.addEventListener('click', async (event) => {
                    const roomId = event.target.getAttribute('data-room-id');
                    getPlayersInRoom(roomId);
                });
            });
        });

        document.getElementById('getStats').addEventListener('click', async() => {
            let {data} = await axios.get(baseServerUrl + '/Get-Personal-Stats');
            console.log(data);
            const [json, status] = data;
            document.querySelector('#data').textContent = json;
        });

        document.getElementById('getHighScores').addEventListener('click', async() => {
            let {data} = await axios.get(baseServerUrl + '/Get-High-Scores');
            console.log(data);
            const [json, status] = data;
            document.querySelector('#data').textContent = json;
        });

        document.getElementById('createRoom').addEventListener('click', showCreateRoomForm);
        // document.getElementById('joinRoom').addEventListener('click', showRoomScreen);
        document.getElementById('logout').addEventListener('click', async() => {
            let {data} = await axios.get(baseServerUrl + '/Logout');
            const [json, status] = data;
            if(status === 101)
            {
                showLoginScreen();
            }
        });
    }

    // Screen 4: Create Room Form
    function showCreateRoomForm() {
        app.innerHTML = `
            <h2>Create Room</h2>
            <input type="text" id="roomName" placeholder="Room Name" />
            <input type="number" id="maxPlayers" placeholder="Max Players" />
            <input type="number" id="numQuestions" placeholder="Number of Questions" />
            <input type="number" id="timePerQuestion" placeholder="Time per Question (seconds)" />
            <button id="createRoomBtn">Create and Join Room</button>
        `;

        document.getElementById('createRoomBtn').addEventListener('click', async() => {
            let roomName = document.getElementById('roomName').value;
            let maxUsers = Number(document.getElementById('maxPlayers').value);
            let questionCount = Number(document.getElementById('numQuestions').value);
            let answerTimeout = Number(document.getElementById('timePerQuestion').value);
            if(roomName && maxPlayers && numQuestions && timePerQuestion) {
                let {data} = await axios.post(baseServerUrl + '/Create-Room', {
                    maxUsers, roomName, questionCount, answerTimeout
                });
                const [json, status] = data;
                if(status === 70) {
                    showRoomScreen();
                } else {
                    console.log(data);
                }
            }
        });
    }

    // Screen 5: Room Screen
    function showRoomScreen() {
        app.innerHTML = `
            <h2>Room Name</h2>
            <ul id="playerList">
                <li>Player 1</li>
                <li>Player 2</li>
                <!-- Add dynamically -->
            </ul>
            <button id="startGame">Start Game (Admin Only)</button>
            <button id="leaveRoom">Leave Room</button>
            <button id="closeRoom">Close Room (Admin Only)</button>
        `;

        document.getElementById('startGame').addEventListener('click', showTriviaScreen);
        document.getElementById('leaveRoom').addEventListener('click', showMenuScreen);
        document.getElementById('closeRoom').addEventListener('click', showMenuScreen);
    }

    // Screen 6: Trivia Screen
    function showTriviaScreen() {
        app.innerHTML = `
            <h2>Trivia Question</h2>
            <p id="question">Question text goes here...</p>
            <button class="answerBtn">Answer 1</button>
            <button class="answerBtn">Answer 2</button>
            <button class="answerBtn">Answer 3</button>
            <button class="answerBtn">Answer 4</button>
            <button id="submitAnswer">Submit Answer</button>
            <button id="leaveGame">Leave Game</button>
        `;

        document.getElementById('submitAnswer').addEventListener('click', showNextQuestion);
        document.getElementById('leaveGame').addEventListener('click', showMenuScreen);
    }

    // Function to show next question (or results)
    function showNextQuestion() {
        // Logic to get the next question or show results
        // This is just placeholder for now
        app.innerHTML = `
            <h2>Results</h2>
            <p>Results go here...</p>
            <button id="backToMenu">Back to Menu</button>
        `;

        document.getElementById('backToMenu').addEventListener('click', showMenuScreen);
    }
});

// Join room function
async function joinRoom(roomId) {
    // Logic to handle joining the room
    console.log(`Joining room with ID: ${roomId}`);
    // Call the API or transition to the room screen
    let {data} = await axios.get(baseServerUrl + '/Join-Room', {params: {roomId}})
    const [json, status] = data;
    console.log(data);
    
    showRoomScreen(roomId);
}

// Get players in room function
async function getPlayersInRoom(roomId) {
    try {
        let { data } = await axios.get(`${baseServerUrl}/Get-Players-In-Room?roomId=${roomId}`);
        console.log(data); // You can display the players in a similar way to how rooms are displayed

        // // Example display
        // const playersList = data.Players.map(player => `<li>${player.username}</li>`).join('');
        // document.querySelector('#data').innerHTML = `
        //     <h3>Players in Room ${roomId}</h3>
        //     <ul>${playersList}</ul>
        // `;

    } catch (error) {
        console.error('Error fetching players:', error);
    }
}
