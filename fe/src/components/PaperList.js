import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = process.env.REACT_APP_BASE_URL||"http://localhost:5000"; 

const categories = [
  "Artificial Intelligence",
  "Machine Learning",
  "Computer Vision",
  "Natural Language Processing",
  "Robotics",
  "Neural Networks",
  "Information Retrieval",
  "Multi-Agent Systems",
  "Statistical Machine Learning",
];

const PaperList = () => {
  const [papersByCategory, setPapersByCategory] = useState({});
  const [searchQuery, setSearchQuery] = useState("");
  const [lastUpdate, setLastUpdate] = useState("");
  const [selectedCategories, setSelectedCategories] = useState([]); 

  useEffect(() => {
    const fetchLastUpdate = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/last_update`);
        setLastUpdate(response.data.last_update);
      } catch (error) {
        console.error("❌ Error fetching last update:", error);
      }
    };
    fetchLastUpdate();
  }, []);

  useEffect(() => {
    const fetchAllPapers = async () => {
      try {
        console.log("🔍 Fetching all category papers...");
        const response = await axios.get(`${BASE_URL}/api/all_papers`);
        console.log("📄 Received papers:", response.data);
        setPapersByCategory(response.data);
      } catch (error) {
        console.error("❌ Error fetching papers:", error);
      }
    };
    fetchAllPapers();
  }, []);

  const toggleCategory = (category) => {
    setSelectedCategories((prevCategories) =>
      prevCategories.includes(category)
        ? prevCategories.filter((c) => c !== category) 
        : [...prevCategories, category]
    );
  };

  return (
    <div className="paper-list-container">
      <h1>Papers Board</h1>

      <p>📅 Latest update: {lastUpdate ? lastUpdate : "Loading..."}</p>

      
      <h3>Summary was generated using the Flan-T5-Base model. </h3>
      <p>Using quantization and LoRA techniques, the learning speed was improved by 25%.</p>

      <input
        type="text"
        placeholder="Search papers..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="search-input"
      /> 

      <div className="category-list">
        {categories.map((category) => (
          <button
            key={category}
            className={`category-button ${selectedCategories.includes(category) ? "active" : ""}`}
            onClick={() => toggleCategory(category)}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="papers-container">
        {selectedCategories.length > 0 ? (
          selectedCategories.map((category) => (
            <div key={category} className="category-container">
              <h2>📂 {category}</h2>
              <div className="papers">
                {papersByCategory[category]?.filter((paper) =>
                  paper.title.toLowerCase().includes(searchQuery.toLowerCase())
                ).length > 0 ? (
                  papersByCategory[category]
                    .filter((paper) =>
                      paper.title.toLowerCase().includes(searchQuery.toLowerCase())
                    )
                    .map((paper, index) => (
                      <div key={index} className="paper-card">
                        <h3>{paper.title}</h3>
                        <p>{paper.authors}</p>
                        <p>{paper.published_date}</p>
                        <p>
                          <span className="summary-section">
                            <strong>Summary:</strong> 
                          </span>
                          <span className="summary-text">
                            {paper.summary ? paper.summary : "No summary available"}
                          </span>
                        </p>
                        <a href={paper.url} target="_blank" rel="noopener noreferrer">
                          PDF
                        </a>
                      </div>
                    ))
                ) : (
                  <p>📌 No papers...</p>
                )}
              </div>
            </div>
          ))
        ) : (
          <p>📌 Choose at least one category</p>
        )}
      </div>
    </div>
  );
};

export default PaperList;