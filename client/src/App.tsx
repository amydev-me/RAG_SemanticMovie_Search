import React, { useState } from "react";
import axios from "axios";
interface Movie {
  title: string;
  plot: string;
  poster: string;
}
function App() {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post<{ data: Movie[] }>("http://127.0.0.1:5000/search", { query });
      
      setMovies(response.data.data);
    } catch (error) {
      console.error("Error searching movies:", error);
    }
    setLoading(false);
  };

  const onImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    e.currentTarget.src = 'img/notfound.png';
  };

 

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-center mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for movies"
          className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSearch}
          className="ml-4 px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-center text-gray-500">Loading...</p>}

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        {movies.map((movie, index) => (
          <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
             <div className="w-full h-72">
             <img
                src={movie.poster || 'img/notfound.png'}
                alt={movie.title} 
                onError={onImageError}
                className="w-full h-full object-cover" 
              />
             </div>
            <div className="p-4">
              <h2 className="text-xl font-semibold text-gray-800">{movie.title}</h2>
              <p className="text-sm text-gray-600 mt-2">{movie.plot}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
