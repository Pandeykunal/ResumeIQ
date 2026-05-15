export default function ScoreCard({ placement_chance, rf_confidence }) {
  const placementColor =
    placement_chance >= 70 ? "text-green-600" :
    placement_chance >= 40 ? "text-yellow-500" : "text-red-500";

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-2xl shadow p-6 text-center">
        <p className="text-gray-500 text-sm mb-1">Placement Chance</p>
        <p className={`text-5xl font-bold ${placementColor}`}>{placement_chance}%</p>
        <p className="text-gray-400 text-xs mt-2">Based on your profile</p>
      </div>
      <div className="bg-white rounded-2xl shadow p-6 text-center">
        <p className="text-gray-500 text-sm mb-1">Role Match Confidence</p>
        <p className="text-5xl font-bold text-indigo-600">{rf_confidence}%</p>
        <p className="text-gray-400 text-xs mt-2">Random Forest prediction</p>
      </div>
    </div>
  );
}