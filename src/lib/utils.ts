import type { Pokemon } from "pokeapi-js-wrapper";
import type { PokeData } from "./components/PokeQuery.svelte";

export const getFallbackSprite = (pokemon: Pokemon, poke_data: PokeData) => {
  const sprite = pokemon.sprites.front_default;
  if (sprite) return sprite;

  const species = poke_data.pokemon_species[pokemon.species.name];

  if (!species) {
    return null;
  }

  for (const v of species.varieties) {
    const fallback = poke_data.pokemon[v.pokemon.name].sprites.front_default;
    if (fallback) {
      return fallback;
    }
  }

  return null;
};
