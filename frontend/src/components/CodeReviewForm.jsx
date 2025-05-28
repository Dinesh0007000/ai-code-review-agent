import { useState } from 'react';

function CodeReviewForm() {
    const [repoUrl, setRepoUrl] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: repoUrl }),
            });
            const data = await response.json();
            setMessage(data.message || data.error);
        } catch (error) {
            setMessage('Error submitting review');
        }
    };

    return (
        <div className="max-w-md mx-auto mt-8">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="repoUrl" className="block text-sm font-medium text-gray-700">
                        Repository URL
                    </label>
                    <input
                        type="text"
                        id="repoUrl"
                        value={repoUrl}
                        onChange={(e) => setRepoUrl(e.target.value)}
                        placeholder="https://github.com/username/repo.git"
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                        required
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
                >
                    Submit for Review
                </button>
            </form>
            {message && <p className="mt-4 text-center">{message}</p>}
        </div>
    );
}

export default CodeReviewForm;