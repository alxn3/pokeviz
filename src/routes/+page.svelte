<script lang="ts">
  import PokeQuery, { type PokeData } from '$lib/components/PokeQuery.svelte';
  import { type_colors } from '$lib/const';
  import Scatter from '$lib/viz/Scatter.svelte';
  import PCA from '$lib/components/PCA.svelte';
  import NetworkGraph from '$lib/components/NetworkGraph.svelte';

  import { type Pokemon } from 'pokeapi-js-wrapper';
  import { onMount } from 'svelte';

  let poke_data: PokeData = $state({
    pokedex: {},
    pokemon: {},
    pokemon_species: {},
    generations: {},
    regions: {},
    types: {},
  });

  let queried_pokemon: { [key: string]: Pokemon } = $state({});

  let tab_index: number = $state(0);
  let tabs = [
    { name: 'Scatter', value: 0 },
    { name: 'PCA', value: 1 },
    { name: 'Network', value: 2 },
    { name: 'Colors', value: 3 },
  ];

  $effect(() => {
    if (Object.keys(queried_pokemon).length === 0) {
      return;
    }
    localStorage.setItem('tab_index', tab_index.toString());
  });

  onMount(() => {
    tab_index = parseInt(localStorage.getItem('tab_index') ?? '0');
  });
</script>

<div
  class="bg-base-50 border-base-300 mx-auto flex w-fit max-w-full flex-col gap-6 rounded-xl border p-4"
>
  <PokeQuery bind:pokemon={queried_pokemon} bind:data={poke_data} />
  <div class="flex gap-2">
    {#each tabs as { name, value }}
      <div class="flex select-none">
        <input
          type="radio"
          name="select_tab"
          class="peer hidden"
          id={name + 'tab'}
          bind:group={tab_index}
          {value}
        />
        <label
          for={name + 'tab'}
          class="border-base-300 bg-base-100 text-base-600 peer-checked:border-base-900 peer-checked:bg-base-900 peer-checked:text-base-50 cursor-pointer rounded-lg border-2 px-2 py-0.5"
        >
          {name}
        </label>
      </div>
    {/each}
  </div>

  {#if Object.keys(queried_pokemon).length === 0}
    <p class="text-accent-700 text-lg font-light tracking-widest uppercase">
      ERROR: No Pokemon found
    </p>
  {/if}
  <div>
    <div class="border-base-500 aspect-[7/5] min-h-[40em] w-full rounded-lg border p-4">
      {#if tab_index === 0}
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">Scatter Chart</p>
        <Scatter {poke_data} {queried_pokemon} />
      {:else if tab_index === 1}
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">PCA Chart</p>
        <PCA {queried_pokemon} />
      {:else if tab_index === 2}
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">Type Network</p>
        <NetworkGraph {queried_pokemon} />
      {:else}
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
                <p class="text-base-700 text-lg font-light tracking-widest uppercase">
                  {type.slice(5)}
                </p>
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
      {/if}
    </div>
  </div>
</div>
