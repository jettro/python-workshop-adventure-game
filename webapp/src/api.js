const BASE = "/api";

export async function startGame() {
  const res = await fetch(`${BASE}/start`, { method: "POST" });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function movePlayer(gameId, direction) {
  const res = await fetch(`${BASE}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, direction }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function stopGame(gameId) {
  const res = await fetch(`${BASE}/stop`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
