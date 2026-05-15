export default function CareerAdvice({ career_advice, suitable_roles }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50 p-6 shadow-md hover:shadow-xl transition-all duration-300">

      {/* Background Glow */}
      <div className="absolute top-0 right-0 h-32 w-32 bg-purple-200 rounded-full blur-3xl opacity-40"></div>

      <h2 className="text-xl font-bold mb-3 text-zinc-800 flex items-center gap-2 relative z-10">
         AI Career Advice
      </h2>

      <p className="text-zinc-600 text-sm leading-relaxed mb-5 relative z-10">
        {career_advice}
      </p>

      <div className="relative z-10">
        <p className="text-sm font-semibold mb-3 text-zinc-700">
           Top Recommended Roles
        </p>

        <div className="flex flex-wrap gap-3">
          {suitable_roles?.map((role, i) => (
            <span
              key={i}
              className="bg-white/80 backdrop-blur-sm text-purple-700 border border-purple-200 text-xs font-semibold px-4 py-2 rounded-full hover:bg-purple-600 hover:text-white transition-all duration-300 cursor-pointer shadow-sm"
            >
              {role}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}