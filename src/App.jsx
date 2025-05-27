import React, { useState } from 'react';
import CodeReviewForm from './components/CodeReviewForm';
import './styles/tailwind.css';

function App() {
    const [progress, setProgress] = useState(null);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">AI Code Review Agent</h1>
            <CodeReviewForm setProgress={setProgress} />
            {progress && (
                <div className="mt-4">
                    <p>Processing: {progress}</p>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '50%' }}></div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;