import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeResume } from "../api/resumeApi";

export default function Home() {
  const [file, setFile]       = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");
  const navigate              = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
      setError("");
    } else {
      setError("Please upload a PDF file only.");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.type === "application/pdf") {
      setFile(dropped);
      setError("");
    } else {
      setError("Please upload a PDF file only.");
    }
  };

  const handleAnalyze = async () => {
    if (!file) return setError("Please upload a resume first.");
    setLoading(true);
    setError("");
    try {
      const data = await analyzeResume(file);
      navigate("/result", { state: { data } });
    } catch (err) {
      setError("Something went wrong. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-6">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-5xl font-bold text-indigo-700 mb-3">ResumeIQ</h1>
        <p className="text-gray-500 text-lg">AI-Powered Resume Analyzer & Career Advisor</p>
      </div>

      {/* Upload Box */}
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="bg-white rounded-2xl shadow-lg p-10 w-full max-w-lg text-center border-2 border-dashed border-indigo-300 hover:border-indigo-500 transition cursor-pointer"
        onClick={() => document.getElementById("fileInput").click()}
      >
        <div className="text-6xl mb-4">📄</div>
        {file ? (
          <p className="text-indigo-600 font-semibold text-lg">{file.name}</p>
        ) : (
          <>
            <p className="text-gray-500 text-lg mb-1">Drag & drop your resume here</p>
            <p className="text-gray-400 text-sm">or click to browse</p>
          </>
        )}
        <input
          id="fileInput"
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileChange}
        />
      </div>

      {/* Error */}
      {error && <p className="text-red-500 mt-4">{error}</p>}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={!file || loading}
        className="mt-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white font-semibold px-10 py-3 rounded-xl text-lg transition"
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {/* Loading */}
      {loading && (
        <div className="mt-6 text-center">
          <div className="animate-spin text-4xl">⚙️</div>
          <p className="text-gray-500 mt-2">Analyzing your resume with AI...</p>
        </div>
      )}
    </div>
  );
}