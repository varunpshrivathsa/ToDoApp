export default function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="text-center px-6">
        <h1 className="text-5xl font-extrabold text-gray-800 mb-4">
          Welcome to <span className="text-blue-600">TodoApp</span>
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Organize your tasks, stay productive, and never miss a deadline.
        </p>

        {/* CTA Buttons */}
        <div className="flex justify-center gap-4">
          <a
            href="/register"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
          >
            Get Started
          </a>
          <a
            href="/login"
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg shadow hover:bg-gray-300 transition"
          >
            Login
          </a>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-6 mt-16 max-w-5xl w-full px-6">
        <div className="p-6 bg-white rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">✅ Easy to Use</h3>
          <p className="text-gray-600">
            Quickly add, edit, and manage your todos with a clean interface.
          </p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">🔒 Secure</h3>
          <p className="text-gray-600">
            Your tasks are stored safely with authentication and authorization.
          </p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">📱 Responsive</h3>
          <p className="text-gray-600">
            Manage your tasks seamlessly on desktop, tablet, or mobile.
          </p>
        </div>
      </div>
    </div>
  );
}
