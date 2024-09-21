import React, { useState } from 'react';

const App = () => {
    const [userInput, setUserInput] = useState('');
    const [response, setResponse] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();  // Prevent default form submission
        setError('');  // Clear previous errors

        try {
            const res = await fetch("http://127.0.0.1:8000/ask/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: userInput }),  // Send as JSON
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail[0].msg || 'Something went wrong');
            }

            const data = await res.json();
            setResponse(data.answer);  // Assuming your backend returns { "answer": ... }
        } catch (error) {
            setError(error.message);  // Update the error state
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    value={userInput} 
                    onChange={(e) => setUserInput(e.target.value)} 
                    placeholder="Ask a question" 
                    required 
                />
                <button type="submit">Ask</button>
            </form>
            {response && <div><strong>Answer:</strong> {response}</div>}
            {error && <div style={{ color: 'red' }}><strong>Error:</strong> {error}</div>}
        </div>
    );
};

export default App;
