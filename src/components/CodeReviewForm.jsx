import React, { useState } from 'react';

function CodeReviewForm({ setProgress }) {
    const [inputPath, setInputPath] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setProgress('Initiating code review...');

        const response = await fetch('http://localhost:5000/api/review', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: inputPath })
        });

        const result = await response.json();
        setProgress(result.message);
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Upload Codebase</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={inputPath}
                    onChange={(e) => setInputPath(e.target.value)}
                    placeholder="Enter ZIP path, Git URL, or folder path"
                    className="w-full p-2 border rounded mb-4"
                />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded">
                    Start Review
                </button>
            </form>
        </div>
    );
}

export default CodeReviewForm;