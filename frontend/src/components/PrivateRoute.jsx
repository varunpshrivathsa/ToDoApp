import { Navigate } from "react-router-dom";

export default function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    // 🚨 No token → redirect to login
    return <Navigate to="/login" replace />;
  }

  // ✅ Token exists → render child component
  return children;
}
