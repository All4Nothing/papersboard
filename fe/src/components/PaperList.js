import React, { useEffect, useState } from "react";
import axios from "axios";

const categories = ["Computer Vision", "Natural Language Processing", "Recommendation System", "Reinforcement Learning"];

const PaperList = () => {
  const [papers, setPapers] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(""); // 선택된 카테고리
  const [searchQuery, setSearchQuery] = useState("");

  // ✅ 카테고리에 따라 논문 불러오기
  useEffect(() => {
    const fetchPapers = async () => {
      try {
        console.log(`🔍 Fetching papers for category: ${selectedCategory}`);

        const response = await axios.get(
          `http://127.0.0.1:5000/api/papers?category=${selectedCategory}`
        );

        console.log(`📄 Received ${response.data.length} papers`);
        setPapers(response.data);
      } catch (error) {
        console.error("❌ Error fetching papers:", error);
      }
    };

    if (selectedCategory) {
      fetchPapers();
    }
  }, [selectedCategory]);

  return (
    <div className="paper-list-container">
      <h1>Deep Learning Monitor</h1>
      
      {/* 🔍 검색창 */}
      <input
        type="text"
        placeholder="Search papers..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      {/* 📌 카테고리 버튼 */}
      <div className="category-buttons">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={selectedCategory === category ? "active" : ""}
          >
            {category}
          </button>
        ))}
      </div>

      {/* 📄 논문 리스트 */}
      <div className="papers">
        {papers
          .filter((paper) =>
            paper.title.toLowerCase().includes(searchQuery.toLowerCase())
          )
          .map((paper, index) => (
            <div key={index} className="paper-card">
              <h3>{paper.title}</h3>
              <p>{paper.authors}</p>
              <p>{paper.published_date}</p>
              <a href={paper.url} target="_blank" rel="noopener noreferrer">
                PDF
              </a>
            </div>
          ))}
      </div>
    </div>
  );
};

export default PaperList;