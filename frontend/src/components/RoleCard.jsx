export default function RoleCard({ primary_role, ranked_roles, required_skills, avg_salary }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="text-xl font-bold text-gray-700 mb-4">Job Role Analysis</h2>

      {/* Primary Role */}
      <div className="bg-indigo-50 rounded-xl p-4 mb-4">
        <p className="text-sm text-gray-500">Primary Match</p>
        <p className="text-2xl font-bold text-indigo-700">{primary_role}</p>
        {avg_salary && (
          <p className="text-sm text-gray-500 mt-1">
            Avg Salary: ${avg_salary?.toLocaleString()}
          </p>
        )}
      </div>

      {/* Required Skills */}
      {required_skills?.length > 0 && (
        <div className="mb-4">
          <p className="text-sm font-semibold text-gray-600 mb-2">Required Skills</p>
          <div className="flex flex-wrap gap-2">
            {required_skills.map((skill, i) => (
              <span key={i} className="bg-indigo-100 text-indigo-700 text-xs px-3 py-1 rounded-full">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Ranked Roles */}
      <div>
        <p className="text-sm font-semibold text-gray-600 mb-2">All Suitable Roles</p>
        {ranked_roles?.map((r, i) => (
          <div key={i} className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-700">{i + 1}. {r.role}</span>
            <div className="flex items-center gap-2">
              <div className="w-32 bg-gray-100 rounded-full h-2">
                <div
                  className="bg-indigo-400 h-2 rounded-full"
                  style={{ width: `${Math.min(r.score * 3, 100)}%` }}
                />
              </div>
              <span className="text-xs text-gray-500">{r.score}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}