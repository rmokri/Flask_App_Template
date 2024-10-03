// DESCRIPTION: the DataModel object is accessible by any other
//scripts linked and loaded on the same page.  It handles all of the
//communications with your API, and the goal is to store state information
//and data in this object as well when possible, in order to minimize
//API calls and to create a single point of access for data in the 
//front-end of your app.

const DataModel = {
    users: [],  // Placeholder for users fetched from the API
    selectedUser: null,  // Store the currently selected user
    baseUrl: `${window.location.protocol}//${window.location.host}/`,  // Base URL dynamically generated for API requests

    /**
     * Helper function for making authenticated API requests with retries.
     * This function sends a request to the given URL using the provided options.
     * It automatically adds the Authorization header with the JWT token from local storage.
     * If the request fails, it retries up to 3 times before throwing an error.
     *
     * IMPORTANT: Use this to make API calls in all of your functions below.
     *            See example of use below.
     * @param {string} url - The API endpoint to send the request to.
     * @param {object} options - Optional fetch options (e.g., method, headers).
     * @returns {Promise<object>} - The JSON response from the API.
     */
    async fetchWithAuth(url, options = {}) {
        const headers = {
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,  // Add JWT token for authentication
            'Content-Type': 'application/json',  // Ensure the request sends and receives JSON
        };
        options.headers = headers;

        // Retry logic: attempt the request up to 3 times
        for (let attempt = 1; attempt <= 3; attempt++) {
            try {
                const response = await fetch(url, options);  // Send the request using fetch
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);  // Throw an error if response is not OK
                }
                return await response.json();  // Parse and return the response JSON if successful
            } catch (error) {
                if (attempt === 3) {
                    // If this is the third and final attempt, rethrow the error
                    throw error;
                }
                // Optional: add a short delay (e.g., 200ms) before retrying
                await new Promise(resolve => setTimeout(resolve, 200));
            }
        }
    },

    /**
     * Function to get all users from the back-end API.
     * This function will fetch all users and store them in the `users` variable within the object.
     */
    async getAllUsers() {
        const url = this.baseUrl + 'users';  // Construct the full API URL for the GET users route
        try {
            const allUsers = await this.fetchWithAuth(url, { method: 'GET' });  // Send GET request to fetch all users
            this.users = allUsers;  // Store the fetched users in the object
            return allUsers;  // Return the list of users
        } catch (error) {
            console.error('Error fetching users:', error);  // Log any errors that occur
            throw error;  // Rethrow the error so it can be handled elsewhere
        }
    },

    /**
     * Function to set the selected user by ID.
     * This function takes a user ID and finds the corresponding user from the `users` array.
     * @param {number} userId - The ID of the user to set as selected.
     */
    setSelectedUser(userId) {
        this.selectedUser = this.users.find(user => user.id === userId);  // Find and set the selected user by ID
        if (!this.selectedUser) {
            console.warn(`User with ID ${userId} not found`);  // Warn if user is not found
        }
    },

    /**
     * Function to get the currently selected user.
     * This function simply returns the `selectedUser` stored in the object.
     * @returns {object|null} - The currently selected user or null if no user is selected.
     */
    getSelectedUser() {
        return this.selectedUser;  // Return the selected user
    },

    /**
     * Function to initialize the data model by fetching all users.
     * This will call `getAllUsers` and store the result in the object.
     */
    async initializeDataModel() {
        try {
            await this.getAllUsers();  // Fetch all users and store them in the object
        } catch (error) {
            console.error('Error initializing data model:', error);  // Log any errors during initialization
        }
    }
};