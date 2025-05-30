import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="w-full bg-gray-800 text-white p-4 fixed top-0 left-0">
    <div className="max-w-7xl mx-auto flex justify-between items-center">
        <h3 className="text-xl font-bold">Weather on Mars</h3>
        <ul className="flex gap-4">
            <Link to="/" className="hover:text-yellow-400">Home</Link>
            <Link to="/about" className="hover:text-yellow-400">About</Link>
        </ul>
    </div>
    </nav>

  );
}