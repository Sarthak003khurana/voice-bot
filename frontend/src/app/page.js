export default function Home() {
  return (
    <main className="h-screen bg-black text-white flex flex-col items-center justify-center">
      <h1 className="text-6xl font-bold mb-6">
        AI Interview Platform
      </h1>

      <p className="text-gray-400 text-lg mb-10">
        Smart AI-powered interview experience
      </p>

      <a
        href="/upload"
        className="bg-white text-black px-8 py-4 rounded-2xl font-semibold hover:scale-105 transition"
      >
        Start Interview
      </a>
    </main>
  );
}
