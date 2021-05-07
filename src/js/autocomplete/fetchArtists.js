// fetch all artists that match the query (user's input)
export async function fetchArtists(query) {
  const response = await fetch("get_artists", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query }),
  });
  const artists = await response.json();
  return artists;
}
