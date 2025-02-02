import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('home');
    const [inputText, setInputText] = useState('');
    const [displayType, setDisplayType] = useState('cards');
    const [cards, setCards] = useState(() => {
        const savedCards = localStorage.getItem('cards');
        return savedCards ? JSON.parse(savedCards) : [];
    });
    const [error, setError] = useState('');
    const [selectedCard, setSelectedCard] = useState(null);

    const toggleFavorite = (cardName) => {
        setCards((prevCards) =>
            prevCards.map((card) =>
                card.name === cardName ? { ...card, isFavorite: !card.isFavorite } : card
            )
        );
    };

    useEffect(() => {
        localStorage.setItem('cards', JSON.stringify(cards));
    }, [cards]);

    const isValidCardData = (data) => {
        return (
            data.name &&
            data.url &&
            data.authors &&
            data.keywords &&
            data.publication_date &&
            data.out_references !== undefined &&
            data.num_out !== undefined &&
            data.in_references !== undefined &&
            data.num_in !== undefined
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        try {
            const inputData = JSON.parse(inputText);

            const existingCards = new Map(cards.map(card => [card.name, card]));

            const processPaper = (paper) => {
                return existingCards.get(paper.name) || {
                    ...paper,
                    isFavourite: false
                };
            };

            if (inputData.papers && Array.isArray(inputData.papers)) {
                const invalidPapers = inputData.papers.filter(
                    (paper) => !isValidCardData(paper)
                );
                if (invalidPapers.length > 0) {
                    throw new Error('Some papers are missing required fields');
                }
                const newCards = inputData.papers.map(processPaper);
                setCards(prev => [
                    ...prev,
                    ...newCards.filter(newCard =>
                        !prev.some(existing => existing.name === newCard.name)
                    )
                ]);
            } else {
                if (!isValidCardData(inputData)) {
                    throw new Error('Invalid JSON structure. Missing required fields.');
                }
                const newCard = processPaper(inputData);
                if (!cards.some(existing => existing.name === newCard.name)) {
                setCards(prev => [
                    ...prev,
                    newCard
                ]);
            }
            }

            setInputText('');
        } catch (err) {
            setError('Invalid JSON format or missing required fields');
            console.error('JSON Parse Error:', err);
        }
    };

    const CardDetail = ({ card, onClose }) => {
        return (
            <div className="card-detail-overlay" onClick={onClose}>
            <div className="card-detail-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={onClose}>
            ×
            </button>
            <h2>{card.name}</h2>
            <div className="detail-section">
            <label>Authors:</label>
            <p>{card.authors.join(', ')}</p>
            </div>
            <div className="detail-section">
            <label>Publication Date:</label>
            <p>{card.publication_date}</p>
            </div>
            <div className="detail-section">
            <label>Keywords:</label>
            <p>{card.keywords.join(', ')}</p>
            </div>
            <div className="detail-section">
            <label>URL:</label>
            <a href={card.url} target="_blank" rel="noopener noreferrer">
            {card.url}
            </a>
            </div>
            <div className="detail-section">
            <label>Outgoing References ({card.num_out}):</label>
            <p>{card.out_references.join(', ') || 'None'}</p>
            </div>
            <div className="detail-section">
            <label>Incoming References ({card.num_in}):</label>
            <p>{card.in_references.join(', ') || 'None'}</p>
            </div>
            </div>
            </div>
        );
    };

    const favoritesCount = cards.filter(card => card.isFavorite).length;

    return (
        <div className="container">
        <div className="header">
        <h1 className="title">InCite</h1>
        <div className="nav-bar">
        {['home', 'gaps', 'collections'].map((tab) => (
            <button
            key={tab}
            className={`nav-button ${activeTab === tab ? 'active-tab' : ''}`}
            onClick={() => setActiveTab(tab)}
            >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
            {tab === 'collections' && ` (${favoritesCount})`}
            </button>
        ))}
        </div>
        </div>

        {activeTab === 'collections' ? (
            // Collections View
            <div className="card-container">
            {[0, 1].map((colIndex) => (
                <div key={colIndex} className="column">
                {cards
                    .filter(card => card.isFavorite)
                    .filter((_, index) => index % 2 === colIndex)
                    .map((card, index) => (
                        <div
                        key={index}
                        className="card"
                        onClick={() => setSelectedCard(card)}
                        >
                        <div className="card-header">
                        <h3 className="card-title">{card.name}</h3>
                        <button
                        className={`favorite-button ${card.isFavorite ? 'favorited' : ''}`}
                        onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(card.name);
                        }}
                        >
                        {card.isFavorite ? '⭐' : '☆'}
                        </button>
                        </div>
                        <div className="card-authors">{card.authors.join(', ')}</div>
                        <div className="card-keywords">{card.keywords.join(', ')}</div>
                        <div className="card-meta">
                        <span>📅 {card.publication_date}</span>
                        <span>🔗 {card.num_out} references</span>
                        </div>
                        </div>
                    ))}
                </div>
            ))}
            </div>
        ) : (
            // Regular View
            <>
            {/* Prompt Input */}
            <form onSubmit={handleSubmit} className="input-container">
            <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter JSON data..."
            className="input-field"
            />
            <button type="submit" className="submit-button">
            Submit
            </button>
            </form>
            {error && <div className="error-message">{error}</div>}

            {/* Display Type Selector */}
            <div className="display-selector">
            <button
            className={`display-button ${displayType === 'cards' ? 'active-display' : ''}`}
            onClick={() => setDisplayType('cards')}
            >
            Cards
            </button>
            <button
            className={`display-button ${displayType === 'graph' ? 'active-display' : ''}`}
            onClick={() => setDisplayType('graph')}
            >
            Graph
            </button>
            </div>

            {/* Content Area */}
            {displayType === 'cards' ? (
                <div className="card-container">
                {[0, 1].map((colIndex) => (
                    <div key={colIndex} className="column">
                    {cards
                        .filter((_, index) => index % 2 === colIndex)
                        .map((card, index) => (
                            <div
                            key={index}
                            className="card"
                            onClick={() => setSelectedCard(card)}
                            >
                            <div className="card-header">
                            <h3 className="card-title">{card.name}</h3>
                            <button
                            className={`favorite-button ${card.isFavorite ? 'favorited' : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                toggleFavorite(card.name);
                            }}
                            >
                            {card.isFavorite ? '⭐' : '☆'}
                            </button>
                            </div>
                            <div className="card-authors">{card.authors.join(', ')}</div>
                            <div className="card-keywords">{card.keywords.join(', ')}</div>
                            <div className="card-meta">
                            <span>📅 {card.publication_date}</span>
                            <span>🔗 {card.num_out} references</span>
                            </div>
                            </div>
                        ))}
                    </div>
                ))}
                </div>
            ) : (
                <div className="graph-placeholder">Graph Display (Placeholder)</div>
            )}
            </>
        )}

        {/* Card Detail Overlay */}
        {selectedCard && (
            <CardDetail card={selectedCard} onClose={() => setSelectedCard(null)} />
        )}
        </div>
    );
}

export default App;
