import { useLocation, useNavigate } from "react-router-dom";
import ScoreCard    from "../components/ScoreCard";
import RoleCard     from "../components/RoleCard";
import GapAnalysis  from "../components/GapAnalysis";
import HowToBridge  from "../components/HowToBridge";
import CareerAdvice from "../components/CareerAdvice";

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const data     = location.state?.data;

  if (!data) {
    navigate("/");
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      {/* Header */}
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-indigo-700">ResumeIQ</h1>
            <p className="text-gray-500 text-sm">Your Analysis Results</p>
          </div>
          <button
            onClick={() => navigate("/")}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl text-sm font-semibold transition"
          >
            ← Analyze Another
          </button>
        </div>

        {/* Results Grid */}
        <div className="space-y-5">
          <ScoreCard
            placement_chance={data.placement_chance}
            rf_confidence={data.rf_confidence}
          />
          <RoleCard
            primary_role={data.primary_role}
            ranked_roles={data.ranked_roles}
            required_skills={data.required_skills}
            avg_salary={data.avg_salary}
          />
          <GapAnalysis
            skills_found={data.skills_found}
            gap_analysis={data.gap_analysis}
          />
          <HowToBridge how_to_bridge={data.how_to_bridge} />
          <CareerAdvice
            career_advice={data.career_advice}
            suitable_roles={data.suitable_roles}
          />
        </div>
      </div>
    </div>
  );
}