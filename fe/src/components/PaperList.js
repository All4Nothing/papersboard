import React, { useEffect, useState } from "react";
import axios from "axios";

const categories = [
  "Computer Vision",
  "Natural Language Processing",
  "Recommendation System",
  "Reinforcement Learning",
];

const PaperList = () => {
  const [papersByCategory, setPapersByCategory] = useState({});
  const [searchQuery, setSearchQuery] = useState("");
  const [lastUpdate, setLastUpdate] = useState("");

  // ✅ 최근 논문 업데이트 날짜 가져오기
  useEffect(() => {
    const fetchLastUpdate = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/last_update");
        setLastUpdate(response.data.last_update);
      } catch (error) {
        console.error("❌ Error fetching last update:", error);
      }
    };

    fetchLastUpdate();
  }, []);

  // ✅ 모든 카테고리의 논문을 한 번에 가져오기
  useEffect(() => {
    const fetchAllPapers = async () => {
      try {
        console.log("🔍 Fetching all category papers...");
        const response = await axios.get("http://127.0.0.1:5000/api/all_papers");

        console.log("📄 Received papers:", response.data);
        setPapersByCategory(response.data); // 카테고리별로 데이터 저장
      } catch (error) {
        console.error("❌ Error fetching papers:", error);
      }
    };

    fetchAllPapers();
  }, []);

  return (
    <div className="paper-list-container">
      <h1>Papers Board</h1>

      {/* 🕒 최근 업데이트 날짜 표시 */}
      <p>📅 Latest update: {lastUpdate ? lastUpdate : "Loading..."}</p>

      {/* 🔍 검색창 */}
      <input
        type="text"
        placeholder="Search papers..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      {/* 📄 카테고리별 논문 리스트 (가로 정렬) */}
      <div className="category-grid">
        {categories.map((category) => (
          <div key={category} className="category-column">
            <h2>{category}</h2>
            <div className="papers">
              {papersByCategory[category]?.length > 0 ? (
                papersByCategory[category]
                  .filter((paper) =>
                    paper.title.toLowerCase().includes(searchQuery.toLowerCase())
                  )
                  .map((paper, index) => (
                    <div key={index} className="paper-card">
                      <h3>{paper.title}</h3>
                      <p>{paper.authors}</p>
                      <p>{paper.published_date}</p>
                      <p><strong>Keywords:</strong> {paper.keywords}</p>
                      <p><strong>Summary:</strong> {paper.summary ? paper.summary : "No summary available"}</p>
                      <a href={paper.url} target="_blank" rel="noopener noreferrer">
                        PDF
                      </a>
                    </div>
                  ))
              ) : (
                <p>📌 해당 카테고리에 논문이 없습니다.</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PaperList;