export default function HowToBridge({ how_to_bridge }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="text-xl font-bold text-gray-700 mb-4">How to Bridge the Gap</h2>
      <ol className="space-y-3">
        {how_to_bridge?.map((step, i) => (
          <li key={i} className="flex gap-3">
            <span className="bg-indigo-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0">
              {i + 1}
            </span>
            <p className="text-sm text-gray-600">{step}</p>
          </li>
        ))}
      </ol>
    </div>
  );
}