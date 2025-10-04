import { useEffect, useState } from "react";
import API from "../api";
import TodoForm from "./TodoForm";
import TodoItem from "./TodoItem";

export default function TodoList() {
  const [todos, setTodos] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    API.get("/todos/")
      .then((res) => setTodos(res.data))
      .catch(() => setError("Failed to fetch todos. Are you logged in?"));
  }, []);

  const handleDelete = async (id) => {
    try {
      await API.delete(`/todos/${id}`);
      setTodos(todos.filter((t) => t.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-lg">
        <h2 className="text-2xl font-bold text-center mb-6">Your Todos</h2>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        {/* Todo Form */}
        <TodoForm onTodoAdded={(newTodo) => setTodos([...todos, newTodo])} />

        {/* Todo List */}
        <ul className="mt-6 space-y-3">
          {todos.length === 0 ? (
            <li className="text-gray-500 text-center">No todos yet. Add one!</li>
          ) : (
            todos.map((todo) => (
            <TodoItem
            key={todo.id}
            todo={todo}
            onDelete={handleDelete}
            onUpdate={(updatedTodo) =>
                setTodos(todos.map((t) => (t.id === updatedTodo.id ? updatedTodo : t)))
            }
            />            ))
          )}
        </ul>
      </div>
    </div>
  );
}
