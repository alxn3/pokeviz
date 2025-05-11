<script lang="ts">
  import PokeQuery, { type PokeData } from '$lib/components/PokeQuery.svelte';
  import { type_colors } from '$lib/const';

  import { type Pokemon } from 'pokeapi-js-wrapper';

  let data: PokeData = $state({
    pokedex: {},
    pokemon: {},
    pokemon_species: {},
    generations: {},
    regions: {},
    types: {},
  });

  const getFallbackSprite = (pokemon: Pokemon) => {
    const sprite = pokemon.sprites.front_default;
    if (sprite) return sprite;

    const species = data.pokemon_species[pokemon.species.name];

    if (!species) {
      return null;
    }

    for (const v of species.varieties) {
      const fallback = data.pokemon[v.pokemon.name].sprites.front_default;
      if (fallback) {
        return fallback;
      }
    }

    return null;
  };

  let queried_pokemon: { [key: string]: Pokemon } = $state({});
</script>

<div
  class="bg-base-50 border-base-300 mx-auto flex w-fit max-w-full flex-col gap-6 rounded-xl border p-4"
>
  <PokeQuery bind:pokemon={queried_pokemon} bind:data />
  <div class="text-base-400 flex flex-wrap gap-2">
    {#each Object.entries(queried_pokemon) as [key, pokemon]}
      <div class="flex gap-2 rounded-xl border-1 p-1">
        <img
          class="bg-base-100 h-16 w-16 rounded-xl border"
          src={getFallbackSprite(pokemon)}
          alt={pokemon.name}
        />
        <div class="flex flex-col">
          <p class="text-base-700 text-lg font-light tracking-widest uppercase">{key}</p>
          <p class="text-base-600 text-sm font-light tracking-widest">{pokemon.name}</p>
        </div>
      </div>
    {/each}
  </div>

  {#if Object.keys(queried_pokemon).length === 0}
    <p class="text-accent-700 text-lg font-light tracking-widest uppercase">No Pokemon found</p>
  {/if}
</div>

<div
  class="bg-base-50 border-base-300 mx-auto flex w-fit max-w-full flex-col gap-6 rounded-xl border p-4"
>
  <div>
    <p class="text-base-700 text-xl font-light tracking-widest uppercase">base</p>
    <div class="flex gap-2">
      <div class="border-base-300 bg-base-50 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-100 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-200 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-300 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-400 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-500 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-600 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-700 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-800 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-900 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-950 h-16 w-16 rounded-xl border"></div>
    </div>
  </div>
  <div>
    <p class="text-base-700 text-xl font-light tracking-widest uppercase">accent</p>
    <div class="flex gap-2">
      <div class="border-base-300 bg-accent-50 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-100 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-200 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-300 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-400 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-500 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-600 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-700 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-800 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-900 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-950 h-16 w-16 rounded-xl border"></div>
    </div>
  </div>
  <div class="grid grid-cols-[repeat(auto-fit,minmax(20em,1fr))] gap-x-4 gap-y-2">
    {#each Object.values(type_colors) as type}
      <div>
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">{type.slice(5)}</p>
        <div class="*:border-base-500/30 flex gap-1 *:h-8 *:grow *:rounded-lg *:border">
          <div class="{type} bg-type-50"></div>
          <div class="{type} bg-type-100"></div>
          <div class="{type} bg-type-200"></div>
          <div class="{type} bg-type-300"></div>
          <div class="{type} bg-type-400"></div>
          <div class="{type} bg-type-500"></div>
          <div class="{type} bg-type-600"></div>
          <div class="{type} bg-type-700"></div>
          <div class="{type} bg-type-800"></div>
          <div class="{type} bg-type-900"></div>
          <div class="{type} bg-type-950"></div>
        </div>
      </div>
    {/each}
  </div>
</div>
