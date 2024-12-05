import React, { useState, useEffect } from "react";

const Report = () => {
    const [fontSize, setFontSize] = useState(16);
    const [reportContent, setReportContent] = useState("Loading...");

    // Fetch report content from Flask backend
    useEffect(() => {
        const fetchReport = async () => {
            try {
                console.log("Fetching report from Flask...");
                const response = await fetch("http://127.0.0.1:5000/api/report");
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                console.log("Fetched data:", data);
                setReportContent(data.report);
            } catch (error) {
                console.error("Error fetching report:", error);
                setReportContent("Error loading report.");
            }
        };

        fetchReport();
    }, []);

    // Adjust font size dynamically
    useEffect(() => {
        const adjustFontSize = () => {
            const parentHeight = window.innerHeight * 0.9;
            const parentWidth = window.innerWidth * 0.8;
            setFontSize(Math.min(parentHeight, parentWidth) * 0.02);
        };

        adjustFontSize();
        window.addEventListener("resize", adjustFontSize);
        return () => window.removeEventListener("resize", adjustFontSize);
    }, []);

    return (
        <div
            style={{
                width: "80%",
                height: "90%",
                overflowY: "auto",
                margin: "20px auto",
                padding: "20px",
                border: "1px solid #ccc",
                backgroundColor: "white",
                boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                fontSize: `${fontSize}px`,
                lineHeight: 1.5,
            }}
        >
            {reportContent}
        </div>
    );
};

export default function App() {
    return (
        <div>
            <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
                Weekly AI Report
            </h1>
            <Report />
        </div>
    );
}