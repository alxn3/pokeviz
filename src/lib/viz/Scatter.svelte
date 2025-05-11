<script lang="ts">
  import { ScatterChart, Tooltip } from 'layerchart';
  import { type Pokemon } from 'pokeapi-js-wrapper';

  import type { PokeData } from '$lib/components/PokeQuery.svelte';
  import PokeTooltip from '../components/PokeTooltip.svelte';
  import Select from '../components/Select.svelte';

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
</script>

<div class="flex h-full flex-col gap-2">
  <div class="h-full rounded-md border p-4">
    <ScatterChart
      series={[
        {
          key: 'default',
          data: (() => {
            console.log(x_axis, y_axis);
            return Object.values(queried_pokemon);
          })(),
          color: 'var(--color-base-500)',
        },
      ]}
      props={{
        points: { tweened: { duration: 200 } },
        xAxis: { tweened: { duration: 200 } },
        yAxis: { tweened: { duration: 200 } },
      }}
      xPadding={[10, 10]}
      yPadding={[10, 10]}
      brush
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
  </div>
</div>
