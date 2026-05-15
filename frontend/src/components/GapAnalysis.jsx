export default function GapAnalysis({ skills_found, gap_analysis }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="text-xl font-bold text-gray-700 mb-4">Gap Analysis</h2>

      {/* Skills Found */}
      <div className="mb-4">
        <p className="text-sm font-semibold text-green-600 mb-2">Skills Found in Resume</p>
        <div className="flex flex-wrap gap-2">
          {skills_found?.map((skill, i) => (
            <span key={i} className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Missing Skills */}
      <div className="mb-4">
        <p className="text-sm font-semibold text-red-500 mb-2">Missing Skills</p>
        <div className="flex flex-wrap gap-2">
          {gap_analysis?.missing_skills?.map((skill, i) => (
            <span key={i} className="bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full">
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Weak Areas */}
      <div>
        <p className="text-sm font-semibold text-yellow-600 mb-2">Weak Areas</p>
        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
          {gap_analysis?.weak_areas?.map((area, i) => (
            <li key={i}>{area}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}