import { useState } from "react";
import API from "../api";

export default function TodoForm({ onTodoAdded }) {
  const [title, setTitle] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      const res = await API.post("/todos/", { title, completed: false });
      onTodoAdded(res.data);
      setTitle("");
    } catch (err) {
      console.error("Failed to add todo:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex space-x-2">
      <input
        type="text"
        placeholder="New todo"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="flex-grow px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        Add
      </button>
    </form>
  );
}
