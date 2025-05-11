<script lang="ts">
  import { ScatterChart, Tooltip } from 'layerchart';
  import { type Pokemon } from 'pokeapi-js-wrapper';

  import type { PokeData } from '$lib/components/PokeQuery.svelte';
  import PokeTooltip from '../components/PokeTooltip.svelte';
  import Select from '../components/Select.svelte';

  import POPULARITY_DATA from '$lib/data/popularity.csv?url';
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let {
    poke_data,
    queried_pokemon,
  }: {
    poke_data: PokeData;
    queried_pokemon: { [key: string]: Pokemon };
  } = $props();

  const stat_to_name: { [key: string]: string } = {
    hp: 'HP',
    attack: 'Attack',
    defense: 'Defense',
    special_attack: 'Sp.Atk',
    special_defense: 'Sp.Def',
    speed: 'Speed',
  };

  const select_options = Object.keys(stat_to_name).map((s) => ({
    name: stat_to_name[s],
    value: s.replace('_', '-'),
  }));

  let x_axis: string = $state('hp');
  let y_axis: string = $state('attack');

  let use_popularity: boolean = $state(false);

  let popularity_data: { [key: string]: number } = $state({});
  onMount(async () => {
    let data = d3.csvParse(await d3.text(POPULARITY_DATA), d3.autoType) as d3.DSVParsedArray<{
      Name: string;
      Popularity: number;
    }>;
    popularity_data = data.reduce(
      (acc, d) => {
        acc[d.Name.toLowerCase()] = d.Popularity;
        return acc;
      },
      {} as { [key: string]: number },
    );
    console.log(popularity_data);
  });
</script>

<div class="flex h-full flex-col gap-2">
  <div class="border-base-600 h-full rounded-md border p-4">
    <ScatterChart
      series={[
        {
          key: 'default',
          data: (() => {
            x_axis && y_axis && !use_popularity;
            return Object.values(queried_pokemon);
          })(),
          color: 'var(--color-base-700)',
        },
      ]}
      props={{
        points: { tweened: { duration: 200 } },
        xAxis: { tweened: { duration: 200 } },
        yAxis: { tweened: { duration: 200 } },
      }}
      xPadding={[10, 10]}
      yPadding={[10, 10]}
      rRange={use_popularity ? [5, 30] : [5, 5]}
      brush
      r={(p: Pokemon) => (use_popularity ? (popularity_data[p.name] ?? 1) : 0)}
      x={(p: Pokemon) => p?.stats.find((s) => s.stat.name === x_axis)?.base_stat}
      y={(p: Pokemon) => p?.stats.find((s) => s.stat.name === y_axis)?.base_stat}
    >
      <svelte:fragment slot="tooltip" let:x let:y let:padding let:height>
        <Tooltip.Root
          x={padding.left}
          y="data"
          anchor="right"
          contained={false}
          class="text-base-900 border-base-400 mr-[2px] rounded border px-1 py-[2px] text-[10px] font-semibold whitespace-nowrap"
          let:data
        >
          {y(data)}
        </Tooltip.Root>
        <PokeTooltip {poke_data} />

        <Tooltip.Root
          x="data"
          y={height}
          anchor="top"
          class="text-base-900 border-base-400 mr-[2px] rounded border px-1 py-[2px] text-[10px] font-semibold whitespace-nowrap"
          contained={false}
          let:data
        >
          {x(data)}
        </Tooltip.Root>
      </svelte:fragment>
    </ScatterChart>
  </div>
  <div class="space-y-2 p-2 text-xs">
    <div class="flex items-center gap-2">
      <p class="text-base-700 text-base uppercase">X Axis:</p>
      <Select options={select_options} bind:value={x_axis} index="0" />
    </div>
    <div class="flex items-center gap-2">
      <p class="text-base-700 text-base uppercase">Y Axis:</p>
      <Select options={select_options} bind:value={y_axis} index="1" />
    </div>
    <div class="flex items-center gap-2">
      <p class="text-base-700 text-base uppercase">Popularity:</p>
      <div class="select-none">
        <input
          type="checkbox"
          id="use-popularity"
          bind:checked={use_popularity}
          class="peer hidden"
        />
        <label
          for="use-popularity"
          class="text-base-600 border-base-600 peer-checked:text-base-50 peer-checked:bg-base-800 peer-checked:border-base-900 h-7 min-w-7 cursor-pointer rounded-lg border-1 px-2 py-0.5"
        >
          {use_popularity ? 'Yes' : 'No'}
        </label>
      </div>
    </div>
  </div>
</div>
