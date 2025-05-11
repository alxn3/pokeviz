<script lang="ts">
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
  import Filter, { type FilterOptions, type FilterValues } from './Filter.svelte';
  import { type_colors } from '$lib/const';

  export type PokeData = {
    pokedex: { [key: string]: PokedexObject };
    pokemon: { [key: string]: Pokemon };
    pokemon_species: { [key: string]: PokemonSpecies };
    generations: { [key: string]: Generation };
    regions: { [key: string]: Region };
    types: { [key: string]: Type };
  };

  let {
    pokemon = $bindable(),
    data = $bindable(),
  }: {
    pokemon: { [key: string]: Pokemon };
    data: PokeData;
  } = $props();

  let filterOptions: FilterOptions = $state({
    types: [],
    regions: [],
    generations: [],
  });
  let filterValues: FilterValues = $state({
    types: [],
    regions: [],
    generations: [],
  });

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

  const updatePokemon = async () => {
    const P = new Pokedex();

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

    await Promise.all(fetchUnloaded(data.pokemon_species, species_list, P.getPokemonSpeciesByName));

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
    pokemon = getFiltered(data.pokemon, pokemon_list);
  };

  $effect(() => {
    if (filterOptions.types.length === 0 || !filterValues) return;
    localStorage.setItem('filter', JSON.stringify(filterValues));

    const timeout = setTimeout(() => {
      updatePokemon();
    }, 200);
    return () => {
      clearTimeout(timeout);
    };
  });

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

<Filter {filterOptions} bind:values={filterValues} />
