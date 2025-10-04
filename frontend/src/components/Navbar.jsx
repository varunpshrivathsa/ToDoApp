import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");   // redirect to login after logout
  };

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between">
      <span className="font-bold">TodoApp</span>
      <div>
        {!isAuthenticated ? (
          <>
            <Link to="/" className="px-2">Home</Link>
            <Link to="/login" className="px-2">Login</Link>
            <Link to="/register" className="px-2">Register</Link>
          </>
        ) : (
          <>
            <Link to="/todos" className="px-2">Todos</Link>
            <button onClick={handleLogout} className="px-2">Logout</button>
          </>
        )}
      </div>
    </nav>
  );
}
