import API from "../api";
import { useState } from "react";

export default function TodoItem({ todo, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [newTitle, setNewTitle] = useState(todo.title);

  const handleUpdate = async () => {
    try {
      const res = await API.put(`/todos/${todo.id}`, {
        title: newTitle,
        completed: todo.completed,
      });
      onUpdate(res.data); // pass updated todo back to parent
      setIsEditing(false);
    } catch (err) {
      console.error("Update failed:", err);
    }
  };

  return (
    <li className="flex justify-between items-center p-2 border-b">
      {isEditing ? (
        <>
          <input
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            className="border p-1"
          />
          <button onClick={handleUpdate} className="ml-2 text-green-600">
            Save
          </button>
          <button onClick={() => setIsEditing(false)} className="ml-2 text-gray-500">
            Cancel
          </button>
        </>
      ) : (
        <>
          <span>{todo.title}</span>
          <div>
            <button onClick={() => setIsEditing(true)} className="mr-2 text-blue-600">
              Edit
            </button>
            <button onClick={() => onDelete(todo.id)} className="text-red-600">
              ❌
            </button>
          </div>
        </>
      )}
    </li>
  );
}
