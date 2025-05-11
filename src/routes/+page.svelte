<script lang="ts">
  import Filter, { type FilterOptions, type FilterValues } from '$lib/components/Filter.svelte';

  const type_colors: { [key: string]: string } = {
    normal: 'type-normal',
    fighting: 'type-fighting',
    flying: 'type-flying',
    poison: 'type-poison',
    ground: 'type-ground',
    rock: 'type-rock',
    bug: 'type-bug',
    ghost: 'type-ghost',
    steel: 'type-steel',
    fire: 'type-fire',
    water: 'type-water',
    grass: 'type-grass',
    electric: 'type-electric',
    psychic: 'type-psychic',
    ice: 'type-ice',
    dragon: 'type-dragon',
    dark: 'type-dark',
    fairy: 'type-fairy',
  };

  import {
    Pokedex,
    type Generation,
    type PokedexObject,
    type Pokemon,
    type PokemonSpecies,
    type Region,
    type Type,
  } from 'pokeapi-js-wrapper';
  import { onMount } from 'svelte';

  let filterOptions: FilterOptions | null = $state(null);
  let filterValues: FilterValues = $state({
    types: [],
    regions: [],
    generations: [],
  });

  let data: {
    pokedex: { [key: string]: PokedexObject };
    pokemon: { [key: string]: Pokemon };
    pokemon_species: { [key: string]: PokemonSpecies };
    generations: { [key: string]: Generation };
    regions: { [key: string]: Region };
    types: { [key: string]: Type };
  } = {
    pokedex: {},
    pokemon: {},
    pokemon_species: {},
    generations: {},
    regions: {},
    types: {},
  };

  const fetchUnloaded = <T,>(
    data: { [key: string]: T },
    filter: string[],
    func: (name: string) => Promise<T>,
  ) => {
    return filter
      .filter((k) => !(k in data))
      .map(async (k) => {
        data[k] = await func(k);
      });
  };

  const getFiltered = <T,>(data: { [key: string]: T }, filter: string[]) => {
    return Object.keys(data)
      .filter((k) => filter.includes(k))
      .reduce(
        (acc, k) => {
          acc[k] = data[k];
          return acc;
        },
        {} as { [key: string]: T },
      );
  };

  const getFallbackSprite = (pokemon: Pokemon) => {
    const sprite = pokemon.sprites.front_default;
    if (sprite) return sprite;

    const species = data.pokemon_species[pokemon.species.name];

    for (const v of species.varieties) {
      const fallback = data.pokemon[v.pokemon.name].sprites.front_default;
      if (fallback) {
        return fallback;
      }
    }

    return null;
  };

  $effect(() => {
    if (!filterOptions || !filterValues) return;
    localStorage.setItem('filter', JSON.stringify(filterValues));

    const P = new Pokedex();

    (async () => {
      await Promise.all([
        ...fetchUnloaded(data.types, filterValues.types, P.getTypeByName),
        ...fetchUnloaded(data.regions, filterValues.regions, P.getRegionByName),
        ...fetchUnloaded(data.generations, filterValues.generations, P.getGenerationByName),
      ]);

      // get all generations from filter values and data
      const gens = getFiltered(data.generations, filterValues!.generations);
      const regions = getFiltered(data.regions, filterValues!.regions);
      const types = getFiltered(data.types, filterValues!.types);

      const filter_gen = Object.keys(gens).length !== 0;
      const filter_region = Object.keys(regions).length !== 0;
      const filter_type = Object.keys(types).length !== 0;

      const pokedexes = [
        ...new Set(
          Object.values(regions)
            .map((r) => r.pokedexes.map((p) => p.name))
            .flat(),
        ),
      ];

      await Promise.all(fetchUnloaded(data.pokedex, pokedexes, P.getPokedexByName));

      const pokedex = getFiltered(data.pokedex, pokedexes);

      const gen_s_set = new Set(
        Object.values(gens)
          .map((g) => g.pokemon_species.map((s) => s.name))
          .flat(),
      );
      const pokedex_s_set = new Set(
        Object.values(pokedex)
          .map((p) => p.pokemon_entries.map((e) => e.pokemon_species.name))
          .flat(),
      );

      const species_list = !filter_gen
        ? [...pokedex_s_set]
        : !filter_region
          ? [...gen_s_set]
          : [...gen_s_set.intersection(pokedex_s_set)];

      await Promise.all(
        fetchUnloaded(data.pokemon_species, species_list, P.getPokemonSpeciesByName),
      );

      const type_p_set = new Set(
        Object.values(types)
          .map((t) => t.pokemon.map((p) => p.pokemon.name))
          .flat(),
      );
      const species = getFiltered(data.pokemon_species, species_list);

      const species_p_set = new Set(
        Object.values(species)
          .map((s) => s.varieties.map((v) => v.pokemon.name))
          .flat(),
      );

      const pokemon_list = !filter_type
        ? [...species_p_set]
        : !(filter_gen || filter_region)
          ? [...type_p_set]
          : [...type_p_set.intersection(species_p_set)];

      await Promise.all(fetchUnloaded(data.pokemon, pokemon_list, P.getPokemonByName));
      const pokemon = getFiltered(data.pokemon, pokemon_list);
      queried_pokemon = pokemon;
    })();
  });

  let queried_pokemon: { [key: string]: Pokemon } = $state({});

  onMount(async () => {
    const filter = localStorage.getItem('filter');
    if (filter) {
      filterValues = JSON.parse(filter);
    }

    const P = new Pokedex();

    const types_list = await P.getTypesList();
    const regions_list = await P.getRegionsList();
    const generations_list = await P.getGenerationsList();

    filterOptions = {
      types: types_list.results
        .filter((i) => i.name in type_colors)
        .map((type) => ({
          name: type.name[0].toUpperCase() + type.name.slice(1),
          value: type.name,
          class: `${type_colors[type.name]} peer-checked:bg-type-300/80 peer-checked:border-type-500/80 peer-checked:text-black`,
        })),
      regions: regions_list.results.map((region) => ({
        name: region.name[0].toUpperCase() + region.name.slice(1),
        value: region.name,
      })),
      generations: generations_list.results.map((generation) => ({
        name: generation.name.split('-')[1].toUpperCase(),
        value: generation.name,
      })),
    };
  });
</script>

<div
  class="bg-base-50 border-base-300 mx-auto flex w-fit max-w-full flex-col gap-6 rounded-xl border p-4"
>
  {#if filterOptions}
    <Filter {filterOptions} bind:values={filterValues} />
  {/if}

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
