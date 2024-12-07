import React, { useEffect, useState } from "react";
import { Bubble } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  LinearScale,
  PointElement,
  Title,
} from "chart.js";

ChartJS.register(Tooltip, Legend, LinearScale, PointElement, Title);

const BubbleChart = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Flask API에서 카테고리별 논문 수 가져오기
    const fetchCategoryCounts = async () => {
      const response = await fetch("/api/category_counts");
      const categoryCounts = await response.json();

      // 데이터셋 생성
      const labels = Object.keys(categoryCounts);
      const counts = Object.values(categoryCounts);

      const bubbleData = labels.map((label, index) => ({
        label, // 카테고리명
        x: Math.random() * 100, // 랜덤 X 좌표
        y: Math.random() * 100, // 랜덤 Y 좌표
        r: counts[index] / 2, // 반지름 크기 (논문 수에 비례)
      }));

      setData({
        datasets: [
          {
            label: "AI 카테고리 논문 수",
            data: bubbleData,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      });
    };

    fetchCategoryCounts();
  }, []);

  if (!data) {
    return <p>Loading...</p>;
  }

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h2>카테고리별 논문 수</h2>
      <Bubble
        data={data}
        options={{
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "랜덤 X 축",
              },
            },
            y: {
              title: {
                display: true,
                text: "랜덤 Y 축",
              },
            },
          },
        }}
      />
    </div>
  );
};

export default BubbleChart;